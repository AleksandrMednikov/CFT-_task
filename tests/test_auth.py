#pytest
import pytest

#SQL
from sqlalchemy import insert, select

#локальное
from src.accounting.models import salary
from src.auth.models import user
from tests.conftest import client, async_session_maker, ac

#прочее
import datetime
from httpx import AsyncClient
import re

#тестируем заход юзера и получение им зарплаты по этим данным
account_employee_email = "bookkeeper@mail.ru"
account_employee_password = "123"
account_employee_name = "Bookkeeper"
#данные которые ожидаем получить
account_employee_name_date_of_increase = datetime.date(2023, 12, 12)
account_employee_salary = 100000


#тест на невозможную повторную регистрацию
async def test_error_registering_existing_employee(ac: AsyncClient):
    for i in range(2):
        response = await ac.post("/auth/register", json={
            "email": "errorRegisteringExistingEmployee@mail.ru",
            "username": "errorRegisteringExistingEmployee",
            "role_id": 1,
            "password": "123",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "is_active": True,
        })

        if i == 1:
            assert response.status_code == 400


#тест на успешную регистрацию
async def test_successful_registration(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": account_employee_email,
        "username": account_employee_name,
        "role_id": 1,
        "password": account_employee_password,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    })

    global account_employee_email_id
    account_employee_email_id = response.json()["id"]

    assert response.status_code == 201


#тест на добавление выплаты для сотрудника
async def test_add_salary_for_employees():
    async with async_session_maker() as session:
        user_for_test = {"user_id":account_employee_email_id,
                         "amount_of_payments":account_employee_salary,
                         "date_of_increase":account_employee_name_date_of_increase}

        statement = insert(salary).values(**user_for_test)
        await session.execute(statement)
        await session.commit()

        query = select(salary).where(salary.c.user_id == account_employee_email_id)
        result = await session.execute(query)
        result = result.one()
        assert result[1:] == (account_employee_email_id,
                              account_employee_salary,
                              account_employee_name_date_of_increase)


#значения super_user, is_superuser и role_id для всех дефолтные, независимо от запроса
async def test_protection_superUser_and_roleId():
    reqistetr_email = "ImProtect@mail.ru"

    response = client.post("/auth/register", json={
        "email": reqistetr_email,
        "username": "ImProtect",
        "role_id": 2,
        "password": "132",
        "is_active": True,
        "is_superuser": True,
        "is_verified": True,
    })

    async with async_session_maker() as session:
        query = select(user).where(user.c.email == reqistetr_email)
        result = await session.execute(query)
        result = result.one()
        role = result[3]
        superuser = result[7]


    assert role==1 and superuser == False


#успешная регистрация
async def test_successful_login(ac: AsyncClient):
    response = client.post("/auth/login", data={
        "grant_type": "",
        "username": account_employee_email,
        "password": account_employee_password,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    })

    global account_employee_сookies
    # получение куки которые ввиду стратегии JWT утверждают нашу авторизованность
    account_employee_сookies = response.cookies
    assert response.status_code == 204


# успешное получение информации о своей зарплате сотрудником
def test_show_salary_for_employees():
    сookies = re.findall(r"bonds=[^ ]+", str(account_employee_сookies))[0]
    response = client.post("/salary/get_salary_for_curent_user", headers={"Cookie":сookies})

    assert response.json() == {'user': account_employee_name,
                               'salaries': account_employee_salary,
                               'date_of_increase': str(account_employee_name_date_of_increase)}


