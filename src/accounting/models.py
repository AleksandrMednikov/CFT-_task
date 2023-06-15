from sqlalchemy import (Table, Column, Integer, ForeignKey, Date, Float)
from src.auth.models import user
from src.database import metadata

salary = Table(
    "salary",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id), nullable=False, unique=True),
    Column("amount_of_payments", Float, nullable=False),
    Column("date_of_increase", Date, nullable=True)
)