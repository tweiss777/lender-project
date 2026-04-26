from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class YearsInBusinessCheck(EvaluationCheck):
    name = "Time in Business"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        minimum = policy_ctx.policy.min_years_in_business
        if minimum is None:
            return None

        yib = app_ctx.borrower.years_in_business
        if yib is None:
            return CriterionResult(self.name, False, "Years in business not provided")
        if yib >= minimum:
            return CriterionResult(self.name, True, f"{yib} years in business meets the minimum of {minimum}")
        return CriterionResult(
            self.name, False,
            f"{yib} years in business is below the minimum requirement of {minimum}",
        )
