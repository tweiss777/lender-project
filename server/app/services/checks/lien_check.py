from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class LienCheck(EvaluationCheck):
    name = "Tax Liens"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        # None means the lender has no stated position — skip
        if policy_ctx.policy.allows_liens is None:
            return None
        if app_ctx.guarantor is None:
            return None

        if app_ctx.guarantor.has_liens and not policy_ctx.policy.allows_liens:
            return CriterionResult(
                self.name, False,
                "This lender does not accept applications with outstanding tax liens",
            )
        return CriterionResult(self.name, True, "No tax liens on record")
