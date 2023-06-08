from pydantic import BaseModel

class Salary_for_insert(BaseModel):
    amount_of_payments: int
    user_id: int
    year: int
    month: int
    day: int