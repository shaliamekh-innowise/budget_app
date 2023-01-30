from adapters.external_api.fake_rate_api import FakeRateApi
from adapters.repositories.sqlalchemy_expense_repository import SQLAlchemyExpenseRepository
from dependencies.database import get_db
from usecases.expense_management import ExpenseManagementUsecase

from fastapi import Depends


def get_expense_management_usecase(db=Depends(get_db)):
    return ExpenseManagementUsecase(FakeRateApi(), SQLAlchemyExpenseRepository(db))
