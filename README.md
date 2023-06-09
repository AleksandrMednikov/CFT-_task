# Show Salary
---
**Запуск через Docker** 🐳 
1. Используйте файл .env-for-dep для настройки переменых

DB_HOST = хост вашей postgreSQL базы данных
DB_PORT = порт вашей postgreSQL базы данных
DB_NAME = имя вашей postgreSQL базы данных
DB_USER = пользователь postgreSQL
DB_PASS = пароль пользователя postgreSQL

DB_HOST_TEST = хост вашей postgreSQL базы данных для теста
DB_PORT_TEST = хост вашей postgreSQL базы данных для теста
DB_NAME_TEST = имя вашей postgreSQL базы данных для теста
DB_USER_TEST = пользователь postgreSQL
DB_PASS_TEST = пароль пользователя postgreSQL

POSTGRES_DB = имя вашей postgreSQL базы данных
POSTGRES_USER = пользователь postgreSQL
POSTGRES_PASSWORD = пароль пользователя postgreSQL

SEC_KEY = это время жизни куки для действий требующих авторизаций в секундах
SECRET_AUTH = ключ необходимый для кеширования пользователей.
Я оставил сделанный через SHA256 для случая если бы захотел усилить безопасность,
но должна сработать и любая хаотичная надпись.

2. Запустите проект через докер
    ```
    терминал> docker compose build
    терминал> docker compose up
    ```

    ВАЖНО!🔧
    При первом запуске после docker compose build может возникнуть ошибка связаная с тем что не были пропущены миграции. В таком случае прервите работу CTRL+C и запустите заново
    ```
    терминал> docker compose up
    ```

3. Зайдите на *http://localhost:9999/docs*
4. Обратите внимание на созданый благодаря fastapi-users раздел Auth
5. используйте */auth/register* чтобы создать пользователя
    - "email": любой майл, нет типизации pydantic.EmailStr можете просто ввести любую строку
    - "password": пароль,
    - "username": ник
    остальные значение можете не трогать, они всеравно поменяются на дефолтные в целях безопасности
6. используйте */auth/login* чтобы  войти
    "username": майл при регистрации
    "password": пароль
7. Обратите внимание на раздел Salary.
 Установите зарплату и дату повышения(необязательный параметр если везде = 0) работнику и получите ее за сотрудника. Есть три способа, рекомендую обратить внимание на тот что я ввел последним. К первым двух относитесь
 как к более правдободобной версии при деплое для ознакомления.
	1) Нужно будет вручную установить значениe 2 для колоны role_id на привязаной БД PostgreSQL любому сотруднику в таблице user
	  - Зайдите за этого сотрудника */auth/login*
	  - Используйте */salary/insert_salary* для ввода зарплаты для сотрудника с указаным user_id
	  
	  Быть может важно будет подметить что insert_salary не работает как UPDATE. Ей можно только вводить значения,
	  но не менять существующие.
	2) Нужно будет вручную установить зарплату на привязаной БД PostgreSQL любому сотруднику в таблице salary
	  - Зайдите за этого сотрудника /auth/login
	  - Получите его зарплату */salary/get_salary_for_curent_user*
	  - Зайдите за сотрудника которому вы установили зарплату /auth/login и   получите данные */salary/get_salary_for_curent_user*
	3) Используйте /salary/NOT_FOR_DEPLOY_insert_salary нажав Execute. Выставится значение для пользователся с id=1, первого что вы зарегистрировали, равное 200.80 и дате 2023-12-12
8.  Получите вашу зарплату. Важно подметить что я сделал зарплату типом    string чтобы получать более читаемое значение значение 200.80, а не 200.8. Я уверен на js если необходимо можно
   будет сделать parseFloat("200.80").
    Перейдите */salary/get_salary_for_curent_user* и нажмите Execute. Куки с ключом живущий в количестве SEC_KEY секунд позволит вам получить зарплату. Для создании такой стратегии используется JWT.
---
**Запуск без докера и запуск тестов** 
1. Используйте .env для настройки переменых при запуске без докера.
   Со значением переменых можете ознакомится в первом разделе "Запуск через Docker".
2. Установите библиотеки из requirements.txt либо используйте poetry
3. Проведите миграцию
     ```
     терминал> alembic upgrade head
     ```
4. Запустите тесты. Значение тестов указано в test/test_all.py перед созданиями функций
    ```
    терминал> pytest -v -s tests/
    ```
5. Запустите приложение
     ```
     терминал: uvicorn main>app --reload
     ```
6. Задйдите на *http://127.0.0.1:8000/docs*
7. Обратите внимание на созданый благодаря fastapi-users раздел Auth
8. используйте */auth/register* чтобы создать пользователя
    "email": любой майл, нет типизации pydantic.EmailStr можете просто ввести любую строку
    "password": пароль,
    "username": ник
    остальные значение можете не трогать, они всеравно поменяются на дефолтные в целях безопасности
9. используйте */auth/login* чтобы  войти
    "username": майл при регистрации
    "password": пароль
10. Обратите внимание на раздел Salary.
 Установите зарплату и дату повышения(необязательный параметр если везде = 0) работнику и получите ее за сотрудника.
 Есть три способа, рекомендую обратить внимание на тот что я ввел последним.
	1) Нужно будет вручную установить значени 2 для колоны role_id на привязаной БД PostgreSQL любому сотруднику в таблице user
	  - Зайдите за этого сотрудника */auth/login*
	  - Используйте */salary/insert_salary* для ввода зарплаты для сотрудника с указаным user_id
	 
     Быть может важно будет подметить что insert_salary не работает как UPDATE. Ей можно только вводить значения,
	  но не менять существующие.
	2) Нужно будет вручную установить зарплату на привязаной БД PostgreSQL любому сотруднику в таблице salary
	  - Зайдите за этого сотрудника */auth/login*
	  - Получите его зарплату */salary/get_salary_for_curent_user*
	  - Зайдите за сотрудника которому вы установили зарплату /auth/login и получите данные */salary/get_salary_for_curent_user*
	3) Используйте */salary/NOT_FOR_DEPLOY_insert_salary* нажав Execute. Выставится значение для пользователся с id=1, первого что вы зарегистрировали, равное 200.80 и дате 2023-12-12
11.  Получите вашу зарплату. Важно подметить что я сделал зарплату типом string чтобы получать более читаемое значение значение 200.80, а не 200.8. Я уверен на js если необходимо можно будет сделать `parseFloat("200.80")`.
    Перейдите */salary/get_salary_for_curent_user* и нажмите Execute. Куки с ключом живущий в количестве
    SEC_KEY секунд позволит вам получить зарплату. Для создании такой стратегии используется JWT.
