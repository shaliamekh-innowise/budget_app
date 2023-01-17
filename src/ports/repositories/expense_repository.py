from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.expense import Expense
from src.domain.statistics import Statistics


class ExpenseRepository(ABC):

    @abstractmethod
    async def save_expense(self, expense: Expense) -> UUID:
        pass

    @abstractmethod
    async def get_statistics(self, user_id: UUID) -> Statistics:
        pass

    @abstractmethod
    async def find_by_uuid(self, uuid: UUID) -> Expense:
        pass
