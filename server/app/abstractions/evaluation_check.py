from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.services.matching_engine import ApplicationContext, CriterionResult, PolicyContext


class EvaluationCheck(ABC):
    """
    Base class for a single lender eligibility check.

    Return None  → criterion does not apply to this policy (field not set).
    Return a CriterionResult → criterion was evaluated; result is recorded.
    """

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def evaluate(
        self,
        app_ctx: "ApplicationContext",
        policy_ctx: "PolicyContext",
    ) -> Optional["CriterionResult"]: ...
