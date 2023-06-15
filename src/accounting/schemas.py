from pydantic import BaseModel
from typing import Union

class Salary_for_insert(BaseModel):
    amount_of_payments: Union[int, float]
    user_id: int
    year: int
    month: int
    day: int

class Show_salary_for_current_user(BaseModel):
    user: str
    salaries: str
    date_of_increase: Union[str, None]
