from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class LoanAmountCheck(EvaluationCheck):
    name = "Loan Amount"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        amount = app_ctx.loan_request.amount
        policy = policy_ctx.policy

        if amount is None:
            return None
        if policy.min_loan_amount and amount < policy.min_loan_amount:
            return CriterionResult(
                self.name, False,
                f"Requested amount ${amount:,.0f} is below the lender minimum of ${policy.min_loan_amount:,.0f}",
            )
        if policy.max_loan_amount and amount > policy.max_loan_amount:
            return CriterionResult(
                self.name, False,
                f"Requested amount ${amount:,.0f} exceeds the lender maximum of ${policy.max_loan_amount:,.0f}",
            )
        return CriterionResult(self.name, True, f"Requested amount ${amount:,.0f} is within the allowed range")
