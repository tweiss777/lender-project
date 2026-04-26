from datetime import datetime
from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class EquipmentAgeCheck(EvaluationCheck):
    name = "Equipment Age"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        maximum = policy_ctx.policy.max_equipment_age_years
        if maximum is None:
            return None

        equipment_year = app_ctx.loan_request.equipment_year
        if not equipment_year:
            return None  # can't evaluate without a model year

        age = datetime.now().year - equipment_year
        if age <= maximum:
            return CriterionResult(
                self.name, True,
                f"Equipment age {age}yr is within the maximum of {maximum}yr",
            )
        return CriterionResult(
            self.name, False,
            f"Equipment age {age}yr exceeds the maximum allowed age of {maximum}yr",
        )
