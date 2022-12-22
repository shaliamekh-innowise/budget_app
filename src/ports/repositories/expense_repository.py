from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.expense import Expense


class ExpenseRepository(ABC):

    @abstractmethod
    async def save_expense(self, expense: Expense) -> UUID:
        pass
