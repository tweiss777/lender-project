from typing import Optional
from app.abstractions.evaluation_check import EvaluationCheck
from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class IndustryCheck(EvaluationCheck):
    name = "Industry"

    def evaluate(self, app_ctx: ApplicationContext, policy_ctx: PolicyContext) -> Optional[CriterionResult]:
        industry = (app_ctx.borrower.industry or "").strip()
        if not industry:
            return None

        industry_lower = industry.lower()

        # Blacklist takes priority over whitelist
        if industry_lower in policy_ctx.excluded_industries:
            return CriterionResult(
                self.name, False,
                f"Industry '{industry}' is on this lender's exclusion list",
            )
        if policy_ctx.allowed_industries and industry_lower not in policy_ctx.allowed_industries:
            return CriterionResult(
                self.name, False,
                f"Industry '{industry}' is not in this lender's approved industry list",
            )
        return CriterionResult(self.name, True, f"Industry '{industry}' is acceptable")
