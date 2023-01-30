from app import app
from routes import healthcheck
from routes.expense_crud import expense_crud

app.include_router(healthcheck.router, tags=["Healthcheck"])

app.include_router(expense_crud.router, tags=["Expense"])
