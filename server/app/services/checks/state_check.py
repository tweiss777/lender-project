from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class StateCheck(EvaluationCheck):
    name = "Business State"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        state = (app_ctx.borrower.state or "").strip().upper()
        if not state:
            return None

        # Blacklist takes priority over whitelist
        if state in policy_ctx.excluded_states:
            return CriterionResult(
                self.name, False,
                f"This lender does not finance businesses located in {state}",
            )
        if policy_ctx.allowed_states and state not in policy_ctx.allowed_states:
            return CriterionResult(
                self.name, False,
                f"State {state} is not in this lender's approved state list",
            )
        return CriterionResult(self.name, True, f"State {state} is acceptable")
