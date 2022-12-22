import uuid

from src.domain.expense import Expense
from src.ports.repositories.expense_repository import ExpenseRepository


class InMemoryExpenseRepository(ExpenseRepository):
    def __init__(self):
        self.expenses = {}

    async def save_expense(self, expense: Expense) -> uuid.UUID:
        expense.id = uuid.uuid4()
        self.expenses[expense.id] = expense
        return expense.id
