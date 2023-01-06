import uuid

import pytest

from src.adapters.external_api.fake_rate_api import FakeRateApi
from src.adapters.repositories.inmemory_expense_repository import (
    InMemoryExpenseRepository,
)
from src.domain.category import Category, Priority
from src.domain.expense import Expense
from src.domain.statistics import Statistics
from src.usecases.expense_management import ExpenseManagementUsecase


@pytest.fixture
def expense_repository():
    return InMemoryExpenseRepository()


@pytest.fixture
def expense_management_usecase(expense_repository):
    return ExpenseManagementUsecase(FakeRateApi(), expense_repository)


@pytest.mark.asyncio
async def test_expense_save_success(expense_management_usecase, expense_repository):
    expense = Expense(
        name="Cat food",
        category=Category(name="Food", priority=Priority.MEDIUM),
        price=17.50,
        user_id=uuid.uuid4(),
    )
    expense_from_db = await expense_management_usecase.add_expense(expense)
    assert expense_from_db.price_usd is not None

@pytest.mark.asyncio
async def test_expense_statistics(expense_management_usecase, expense_repository):
    user_id = uuid.uuid4()
    for i in range(3):
        expense = Expense(
            name=f"Cat food #{i+1}",
            category=Category(name="Food", priority=Priority.MEDIUM),
            price=17.50,
            user_id=user_id,
        )
        await expense_management_usecase.add_expense(expense)

    statistics = await expense_management_usecase.get_statistics(user_id=user_id)
    assert statistics == Statistics(expense_count=3, expense_total_amount=17.5*3)
