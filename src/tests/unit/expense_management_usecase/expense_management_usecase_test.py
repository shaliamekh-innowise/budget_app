import pytest

from src.adapters.external_api.fake_rate_api import FakeRateApi
from src.adapters.repositories.inmemory_expense_repository import InMemoryExpenseRepository
from src.domain.category import Category, Priority
from src.domain.expense import Expense
from src.usecases.expense_management import ExpenseManagementUsecase


@pytest.fixture
def expense_repository():
    return InMemoryExpenseRepository()

@pytest.fixture
def expense_management_usecase(expense_repository):
    return ExpenseManagementUsecase(FakeRateApi(), expense_repository)


@pytest.mark.asyncio
async def test_expense_save_success(expense_management_usecase, expense_repository):
    expense = Expense(name="Cat food", category=Category(name="Food", priority=Priority.MEDIUM), price=17.50)
    expense_from_db = await expense_management_usecase.add_expense(expense)
    assert expense_from_db.price_usd is not None

