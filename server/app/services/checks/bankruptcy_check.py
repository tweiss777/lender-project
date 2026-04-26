from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class BankruptcyCheck(EvaluationCheck):
    name = "Bankruptcy History"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        policy = policy_ctx.policy
        if policy.no_bankruptcy is None and policy.min_years_since_bankruptcy is None:
            return None
        if app_ctx.guarantor is None:
            return None

        has_bk = app_ctx.guarantor.has_bankruptcy

        if policy.no_bankruptcy:
            if has_bk:
                return CriterionResult(
                    self.name, False,
                    "This lender does not accept applications with any prior bankruptcy",
                )
            return CriterionResult(self.name, True, "No bankruptcy on record")

        if policy.min_years_since_bankruptcy is not None:
            if has_bk:
                return CriterionResult(
                    self.name, False,
                    f"Bankruptcy on record — lender requires it to be discharged "
                    f"{policy.min_years_since_bankruptcy}+ years ago (manual review of discharge date required)",
                )
            return CriterionResult(self.name, True, "No bankruptcy on record")

        return None
