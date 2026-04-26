from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class JudgmentCheck(EvaluationCheck):
    name = "Judgments"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        # None means the lender has no stated position — skip
        if policy_ctx.policy.allows_judgments is None:
            return None
        if app_ctx.guarantor is None:
            return None

        if app_ctx.guarantor.has_judgments and not policy_ctx.policy.allows_judgments:
            return CriterionResult(
                self.name, False,
                "This lender does not accept applications with outstanding judgments",
            )
        return CriterionResult(self.name, True, "No judgments on record")
