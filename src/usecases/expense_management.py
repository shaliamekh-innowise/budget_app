from src.domain.expense import Expense
from src.ports.external_api.rate_api import RateAPI
from src.ports.repositories.expense_repository import ExpenseRepository


class ExpenseManagementUsecase:
    def __init__(self, rate_api: RateAPI, expense_repository: ExpenseRepository):
        self.rate_api = rate_api
        self.expense_repository = expense_repository

    async def add_expense(self, expense: Expense) -> Expense:
        rate = await self.rate_api.get_rate()
        expense.convert_usd(rate)
        expense.id = await self.expense_repository.save_expense(expense)
        return expense
