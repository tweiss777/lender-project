from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class FicoCheck(EvaluationCheck):
    name = "FICO Score"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        if policy_ctx.policy.min_fico is None:
            return None
        if app_ctx.guarantor is None or app_ctx.guarantor.fico_score is None:
            return CriterionResult(self.name, False, "No guarantor FICO score on file")

        score = app_ctx.guarantor.fico_score
        minimum = policy_ctx.policy.min_fico

        if score >= minimum:
            return CriterionResult(self.name, True, f"FICO {score} meets the minimum of {minimum}")
        return CriterionResult(self.name, False, f"FICO {score} is below the minimum requirement of {minimum}")
