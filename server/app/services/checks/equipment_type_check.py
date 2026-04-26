from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class EquipmentTypeCheck(EvaluationCheck):
    name = "Equipment Type"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        if not policy_ctx.equipment_restrictions:
            return None

        equipment = (app_ctx.loan_request.equipment_type or "").strip()
        if not equipment:
            return None

        if equipment.lower() in policy_ctx.equipment_restrictions:
            return CriterionResult(
                self.name, False,
                f"Equipment type '{equipment}' is restricted by this lender",
            )
        return CriterionResult(self.name, True, f"Equipment type '{equipment}' is acceptable")
