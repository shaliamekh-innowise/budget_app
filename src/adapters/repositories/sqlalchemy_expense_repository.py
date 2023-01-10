from uuid import UUID

from sqlalchemy import select

from adapters.orm_engines import models
from core.exceptions import DatabaseConnectionException
from domain.expense import Expense
from domain.statistics import Statistics
from ports.repositories.expense_repository import ExpenseRepository


class SQLAlchemyExpenseRepository(ExpenseRepository):
    def __init__(self, db):
        self.db = db

    async def save_expense(self, expense: Expense) -> UUID:
        try:
            query = select(models.ExpenseORM).where(models.ExpenseORM.id == expense.id)
            result = await self.db.execute(query)
            expense_db = result.scalars().first()
            if expense_db is None:
                expense_db = models.ExpenseORM()
                self.db.add(expense_db)
            expense_db.price = expense.price
            expense_db.price_usd = expense.price_usd
            expense_db.user_id = expense.user_id
            expense_db.name = expense.name
            expense_db.quantity = expense.quantity
            expense_db.category_name = expense.category.name
            await self.db.commit()
            await self.db.refresh(expense_db)
            return expense_db.id
        except Exception:
            await self.db.rollback()
            raise DatabaseConnectionException

    async def get_statistics(self, user_id: UUID) -> Statistics:
        pass


