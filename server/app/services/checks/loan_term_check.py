from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class LoanTermCheck(EvaluationCheck):
    name = "Loan Term"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        term = app_ctx.loan_request.term_months
        policy = policy_ctx.policy

        if term is None:
            return None
        if policy.min_term_months and term < policy.min_term_months:
            return CriterionResult(
                self.name, False,
                f"Requested term {term}mo is below the lender minimum of {policy.min_term_months}mo",
            )
        if policy.max_term_months and term > policy.max_term_months:
            return CriterionResult(
                self.name, False,
                f"Requested term {term}mo exceeds the lender maximum of {policy.max_term_months}mo",
            )
        return CriterionResult(self.name, True, f"Requested term {term}mo is within the allowed range")
