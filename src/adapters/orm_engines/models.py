from sqlalchemy import Column, Float, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class CategoryORM(Base):
    __tablename__ = "category"
    name = Column(String, primary_key=True)
    priority = Column(Integer, default=2)


class ExpenseORM(Base):
    __tablename__ = "expense"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    category_name = Column(String, ForeignKey("category.name", ondelete="SET NULL"))
    category = relationship("CategoryORM", uselist=False)
    price = Column(Float, default=0)
    quantity = Column(Integer, default=1)
    price_usd = Column(Float, default=0)
