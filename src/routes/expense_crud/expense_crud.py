from fastapi import APIRouter, Depends

from dependencies.usecase_dependencies import get_expense_management_usecase
from routes.expense_crud.controllers import CreateExpense
from usecases.expense_management import ExpenseManagementUsecase

router = APIRouter(prefix="/expense")


@router.post("/")
async def create_expense(
        data: CreateExpense,
        expense_usecase: ExpenseManagementUsecase = Depends(get_expense_management_usecase)
):
    expense = await expense_usecase.add_expense(data.to_entity())
    return expense.id