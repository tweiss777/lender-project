from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class RevenueCheck(EvaluationCheck):
    name = "Annual Revenue"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        minimum = policy_ctx.policy.min_revenue
        if minimum is None:
            return None

        revenue = app_ctx.borrower.revenue
        if revenue is None:
            return CriterionResult(self.name, False, "Annual revenue not provided")
        if revenue >= minimum:
            return CriterionResult(self.name, True, f"Revenue ${revenue:,.0f} meets the minimum of ${minimum:,.0f}")
        return CriterionResult(
            self.name, False,
            f"Revenue ${revenue:,.0f} is below the minimum requirement of ${minimum:,.0f}",
        )
