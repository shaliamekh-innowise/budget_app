from uuid import UUID

from pydantic import BaseModel

from domain.expense import Expense


class CreateExpense(BaseModel):
    user_id: UUID
    name: str
    category_id: UUID
    price: float
    quantity: int = 1

    def to_entity(self):
        return Expense(
            user_id=self.user_id,
            name=self.name,
            price=self.price,
            quantity=self.quantity,
        )
