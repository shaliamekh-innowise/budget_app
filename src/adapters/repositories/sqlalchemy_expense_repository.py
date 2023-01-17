from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from adapters.orm_engines import models
from core.exceptions import DatabaseConnectionException, ExpenseNotFoundException
from domain.category import Category, Priority
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

    async def find_by_uuid(self, uuid: UUID) -> Expense:
        try:
            query = select(models.ExpenseORM).where(models.ExpenseORM.id == uuid)
            result = await self.db.execute(query)
            if expense_db := result.scalars().first():
                expense = Expense(
                    user_id=expense_db.user_id,
                    name=expense_db.name,
                    category=Category(name=expense_db.category_name, priority=Priority(expense_db.category.priority)),
                    price=expense_db.price,
                    price_usd=expense_db.price_usd,
                    quantity=expense_db.quantity,
                    id=expense_db.id
                )
                return expense
            raise ExpenseNotFoundException
        except SQLAlchemyError as e:
            raise DatabaseConnectionException
