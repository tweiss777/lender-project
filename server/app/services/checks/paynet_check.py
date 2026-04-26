from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class PayNetCheck(EvaluationCheck):
    name = "PayNet Score"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        if policy_ctx.policy.min_paynet_score is None:
            return None
        if app_ctx.business_credit is None or app_ctx.business_credit.paynet_score is None:
            return CriterionResult(self.name, False, "No PayNet score on file")

        score = app_ctx.business_credit.paynet_score
        minimum = policy_ctx.policy.min_paynet_score

        if score >= minimum:
            return CriterionResult(self.name, True, f"PayNet {score} meets the minimum of {minimum}")
        return CriterionResult(self.name, False, f"PayNet {score} is below the minimum requirement of {minimum}")
