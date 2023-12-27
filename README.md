# Сервис QRkot

## ОПИСАНИЕ
QRkot - это API для благотворительного фонда поддержки котиков.

### ОСОБЕННОСТИ
Реализация API на FastAPI, использование Google API

### ЭНДПОИНТЫ
| Маршрут | HTTP методы | Описание |
|:---|:---|:---|
| `/charity_project/` | `GET`, `POST` | получение списка проектов, создание проекта |
| `/charity_project/{project_id}/` | `DELETE`, `PATCH` | удаление и изменение проекта |
| `/donation/` | `GET`, `POST` | получение списка пожертвований, создание пожертвования |
| `/donation/my/` | `GET` | получения списка пожертвований пользователя |
| `/google/` | `GET` | создание отчета по проектам |
| `/auth/jwt/login/` | `POST` | вход в систему, получение токена |
| `/auth/jwt/register/` | `POST` | регистрация пользователя |
| `/users/{id}/` | `GET`, `DELETE`, `PATCH` | получение, удаление и изменение учетных данных пользователя |
| `/users/me/` | `GET`, `PATCH` | получение и изменение учетных данных пользователем |

## ЗАПУСК ПРОЕКТА
1. Клонировать репозиторий
```
git clone git@github.com:monteg179/QRkot_spreadsheets.git
cd QRkot_spreadsheets
```
2. Создать и настроить виртуальное окружение
```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
3. Создать базу данных
```
alembic upgrade head
```
4. Создать суперпользователя
```
python -m app.manage createsuperuser
```
5. Создать и заполнить файл .env (смотри env.txt)
6. Запустить сервер
```
python -m app.manage runserver
```

После запуска сервис будет доступен по адресу http://localhost:8000

## ИСПОЛЬЗОВАНИЕ

### регистрация пользователя
```
POST http://localhost:8000/auth/register HTTP/1.1
content-type: application/json

{
    "email": "user1@example.com",
    "password": "12345"
}
```
### получение токена
```
POST http://localhost:8000/auth/jwt/login HTTP/1.1
content-type: application/x-www-form-urlencoded

username=user1@example.com&password=12345
```

### получение учетных данных пользователем
```
GET http://localhost:8000/users/me HTTP/1.1
authorization: bearer <token>
```

### изменение учетных данных пользователем
```
PATCH http://localhost:8000/users/me HTTP/1.1
authorization: bearer <token>
content-type: application/json

{
    "email": "user2@example.com"
}
```

### получение списка проектов
```
GET http://localhost:8000/charity_project/ HTTP/1.1
```

### создание проекта
```
POST http://localhost:8000/charity_project/ HTTP/1.1
authorization: bearer <token>
content-type: application/json

{
  "name": "project1",
  "description": "project1 description",
  "full_amount": 100
}
```

### изменение проекта
```
PATCH http://localhost:8000/charity_project/1 HTTP/1.1
authorization: bearer <token>
content-type: application/json

{
    "description": "project1 new description"
}
```

### удаление проекта
```
DELETE http://localhost:8000/charity_project/1 HTTP/1.1
authorization: bearer <token>
```
### получение списка пожертвований
```
GET http://localhost:8000/donation/ HTTP/1.1
authorization: bearer <token>
```

### создание пожертвования
```
POST http://localhost:8000/donation/ HTTP/1.1
authorization: bearer <token>
content-type: application/json

{
    "full_amount": 100,
    "comment": "no commments"
}
```

### получение списка пожертвований пользователя
```
GET http://localhost:8000/donation/my HTTP/1.1
authorization: bearer <token>
```

### получение отчета по проектам
```
GET http://localhost:8000/google HTTP/1.1
authorization: bearer <token>
```


## ТЕХНОЛОГИИ
- Python 3.9
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- FastAPI Users
- Google API

## АВТОРЫ
* Сергей Кузнецов - monteg179@yandex.ru
