import uuid

import pytest
import pytest_asyncio
from sqlalchemy import delete

from adapters.orm_engines import models
from adapters.orm_engines.models import CategoryORM
from adapters.repositories.sqlalchemy_expense_repository import SQLAlchemyExpenseRepository
from domain.category import Category, Priority
from domain.expense import Expense


@pytest_asyncio.fixture
async def expense_repository(session):
    repository = SQLAlchemyExpenseRepository(session)
    yield repository
    await repository.db.execute(delete(models.ExpenseORM))
    await repository.db.execute(delete(models.CategoryORM))


@pytest.mark.asyncio
async def test_expense_save_to_db_success(expense_repository, session):
    session.add(CategoryORM(name="Food", priority=2))
    session.commit()
    expense = Expense(
        name="Cat food",
        category=Category(name="Food", priority=Priority.MEDIUM),
        price=17.50,
        price_usd=17.50,
        user_id=uuid.uuid4(),
        quantity=1,
    )
    expense_id = await expense_repository.save_expense(expense)
    assert expense_id is not None


@pytest.mark.asyncio
async def test_expense_find_by_id_success(expense_repository: SQLAlchemyExpenseRepository, session):
    session.add(CategoryORM(name="Food", priority=2))
    session.commit()
    expense = Expense(
        name="Cat food",
        category=Category(name="Food", priority=Priority.MEDIUM),
        price=17.50,
        price_usd=17.50,
        user_id=uuid.uuid4(),
        quantity=1,
    )
    expense.id = await expense_repository.save_expense(expense)
    expense_from_db = await expense_repository.find_by_uuid(expense.id)
    assert expense_from_db == expense
