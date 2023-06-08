#FastAPI
from fastapi import Depends
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

#SQL
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

#прочее
import datetime
import itertools

#локальные
from src.auth.base_config import fastapi_users
from src.database import get_async_session
from src.auth.models import User
from src.accounting.models import salary
from src.accounting.schemas import Salary_for_insert

#Переменые для разных типов юзеров
current_active_user = fastapi_users.current_user(active=True)
#current_superuser = fastapi_users.current_user(active=True, superuser=True)


router = APIRouter(prefix="/salary", tags=["Salary"])

@router.post("/insert_salary")
async def insert_salary(data_for_insert_in_salary: Salary_for_insert,
                        user: User = Depends(current_active_user),
                        session: AsyncSession = Depends(get_async_session)):

    data_for_insert_in_salary = data_for_insert_in_salary.dict()
    user_data = dict(itertools.islice(data_for_insert_in_salary.items(), 2))
    date_data = ([*data_for_insert_in_salary.values()][2:])


    if int(user.role_id) == 2:
        try:
            if not all(date_data):
                statement = insert(salary).values(**user_data)
                await session.execute(statement)
                await session.commit()
                return {"message": "Операция выполнена",
                        "instruction": "был создан пользователь без даты повышения заработной платы"}
            else:
                date = datetime.date(*date_data)
                statement = insert(salary).values(**user_data, date_of_increase=date)
                await session.execute(statement)
                await session.commit()
                return {"message": "Операция выполнена",
                        "instruction": "был создан пользователь с датой повышения заработной платы"}
        except ValueError:
            raise HTTPException(status_code=400, detail="Неправильно указанная дата")
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Пользователя с таким id не существует в целом,\
                                                        либо уже существует запись на этого пользователя")
    else:
        raise HTTPException(status_code=403, detail="В доступе отказано")


@router.post("/get_salary_for_curent_user")
async def get_salary_for_curent_user(user: User = Depends(current_active_user),
                            session: AsyncSession = Depends(get_async_session)):

    query = select(salary).where(salary.c.user_id == user.id)
    result = await session.execute(query)
    result = result.one()
    return {"user": user.username, "salaries": result[2], "date_of_increase":result[3]}