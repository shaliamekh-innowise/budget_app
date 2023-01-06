import uuid

from src.domain.expense import Expense
from src.domain.statistics import Statistics
from src.ports.repositories.expense_repository import ExpenseRepository


class InMemoryExpenseRepository(ExpenseRepository):
    def __init__(self):
        self.expenses = {}

    async def save_expense(self, expense: Expense) -> uuid.UUID:
        expense.id = uuid.uuid4()
        self.expenses[expense.id] = expense
        return expense.id

    async def get_statistics(self, user_id: uuid.UUID) -> Statistics:
        user_expenses = []
        for expense in self.expenses.values():
            if expense.user_id == user_id:
                user_expenses.append(expense)
        return Statistics(
            expense_count=len(user_expenses),
            expense_total_amount=sum([expense.price for expense in user_expenses]),
        )
