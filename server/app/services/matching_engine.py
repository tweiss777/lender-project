"""
Matching Engine
===============
Evaluates a loan application against every lender policy in the database
and produces a MatchResult per policy.

Usage
-----
    engine = MatchingEngine()
    results = engine.run(loan_request_id=1, db=db)
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional

from sqlalchemy.orm import Session

from app.models.Borrower import Borrower
from app.models.BusinessCredit import BusinessCredit
from app.models.Lender import Lender
from app.models.LenderAllowedIndustry import LenderAllowedIndustry
from app.models.LenderAllowedState import LenderAllowedState
from app.models.LenderExcludedIndustry import LenderExcludedIndustry
from app.models.LenderExcludedState import LenderExcludedState
from app.models.LenderEquipmentRestriction import LenderEquipmentRestriction
from app.models.LenderPolicy import LenderPolicy
from app.models.LoanRequest import LoanRequest
from app.models.MatchResult import MatchResult, MatchStatus
from app.models.PersonalGuarantor import PersonalGuarantor


# ---------------------------------------------------------------------------
# Context dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ApplicationContext:
    """Everything known about the borrower and their loan request."""
    borrower: Borrower
    loan_request: LoanRequest
    guarantor: Optional[PersonalGuarantor]
    business_credit: Optional[BusinessCredit]


@dataclass
class PolicyContext:
    """
    A lender policy plus all of its related join-table rows, pre-loaded
    so individual checks don't need to touch the database.
    """
    policy: LenderPolicy
    lender_name: str
    allowed_industries: set[str]
    excluded_industries: set[str]
    allowed_states: set[str]
    excluded_states: set[str]
    equipment_restrictions: set[str]


# ---------------------------------------------------------------------------
# Criterion result
# ---------------------------------------------------------------------------

@dataclass
class CriterionResult:
    name: str
    passed: bool
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Matching Engine
# ---------------------------------------------------------------------------

class MatchingEngine:
    """
    Orchestrates all EvaluationCheck instances against every policy.

    Adding a new check
    ------------------
    1. Create a file in app/services/checks/
    2. Subclass EvaluationCheck, implement `name` and `evaluate`
    3. Import and append an instance to self.checks in __init__
    """

    def __init__(self):
        # Import here to avoid circular imports
        from app.services.checks.fico_check import FicoCheck
        from app.services.checks.paynet_check import PayNetCheck
        from app.services.checks.loan_amount_check import LoanAmountCheck
        from app.services.checks.loan_term_check import LoanTermCheck
        from app.services.checks.years_in_business_check import YearsInBusinessCheck
        from app.services.checks.revenue_check import RevenueCheck
        from app.services.checks.industry_check import IndustryCheck
        from app.services.checks.state_check import StateCheck
        from app.services.checks.equipment_type_check import EquipmentTypeCheck
        from app.services.checks.equipment_age_check import EquipmentAgeCheck
        from app.services.checks.bankruptcy_check import BankruptcyCheck
        from app.services.checks.judgment_check import JudgmentCheck
        from app.services.checks.lien_check import LienCheck

        self.checks = [
            FicoCheck(),
            PayNetCheck(),
            LoanAmountCheck(),
            LoanTermCheck(),
            YearsInBusinessCheck(),
            RevenueCheck(),
            IndustryCheck(),
            StateCheck(),
            EquipmentTypeCheck(),
            EquipmentAgeCheck(),
            BankruptcyCheck(),
            JudgmentCheck(),
            LienCheck(),
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_policy_context(self, policy: LenderPolicy, lender_name: str, db: Session) -> PolicyContext:
        pid = policy.policy_id
        return PolicyContext(
            policy=policy,
            lender_name=lender_name,
            allowed_industries={
                r.industry.lower()
                for r in db.query(LenderAllowedIndustry).filter_by(policy_id=pid).all()
            },
            excluded_industries={
                r.industry.lower()
                for r in db.query(LenderExcludedIndustry).filter_by(policy_id=pid).all()
            },
            allowed_states={
                r.state.upper()
                for r in db.query(LenderAllowedState).filter_by(policy_id=pid).all()
            },
            excluded_states={
                r.state.upper()
                for r in db.query(LenderExcludedState).filter_by(policy_id=pid).all()
            },
            equipment_restrictions={
                r.equipment_type.lower()
                for r in db.query(LenderEquipmentRestriction).filter_by(policy_id=pid).all()
            },
        )

    def _evaluate_policy(
        self,
        app_ctx: ApplicationContext,
        policy_ctx: PolicyContext,
    ) -> tuple[float, bool, list[CriterionResult]]:
        """
        Run every check against one policy.
        Returns (fit_score 0-100, is_eligible, list of results).
        Checks that return None are skipped (not applicable).
        """
        results: list[CriterionResult] = []
        for check in self.checks:
            result = check.evaluate(app_ctx, policy_ctx)
            if result is not None:
                results.append(result)

        if not results:
            return 0.0, False, results

        passed = sum(1 for r in results if r.passed)
        fit_score = round((passed / len(results)) * 100, 1)
        is_eligible = all(r.passed for r in results)
        return fit_score, is_eligible, results

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, loan_request_id: int, db: Session) -> list[MatchResult]:
        """
        Evaluate a loan request against all policies in the database.
        Clears any prior results for this loan request, then persists
        and returns the new ones sorted best fit first.
        """
        loan_request = db.query(LoanRequest).filter_by(loan_request_id=loan_request_id).first()
        if not loan_request:
            raise ValueError(f"LoanRequest {loan_request_id} not found")

        borrower = db.query(Borrower).filter_by(borrower_id=loan_request.borrower_id).first()
        guarantor = db.query(PersonalGuarantor).filter_by(borrower_id=loan_request.borrower_id).first()
        business_credit = db.query(BusinessCredit).filter_by(borrower_id=loan_request.borrower_id).first()

        app_ctx = ApplicationContext(
            borrower=borrower,
            loan_request=loan_request,
            guarantor=guarantor,
            business_credit=business_credit,
        )

        # Load every policy alongside its lender name
        rows = (
            db.query(LenderPolicy, Lender.lender_name)
            .join(Lender, Lender.lender_id == LenderPolicy.lender_id)
            .all()
        )

        # Clear previous results for this loan request
        db.query(MatchResult).filter_by(loan_request_id=loan_request_id).delete()

        match_results: list[MatchResult] = []
        for policy, lender_name in rows:
            policy_ctx = self._load_policy_context(policy, lender_name, db)
            fit_score, is_eligible, criteria_results = self._evaluate_policy(app_ctx, policy_ctx)

            result = MatchResult(
                loan_request_id=loan_request_id,
                policy_id=policy.policy_id,
                is_eligible=is_eligible,
                match_score=fit_score,
                status=MatchStatus.eligible if is_eligible else MatchStatus.ineligible,
                criteria_results=[r.to_dict() for r in criteria_results],
            )
            db.add(result)
            match_results.append(result)

        db.commit()
        return sorted(match_results, key=lambda r: r.match_score, reverse=True)
