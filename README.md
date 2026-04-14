# FastAPI KR4

Контрольная работа №4 — Технологии разработки серверных приложений.

## Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Настройка окружения

```bash
cp .env.example .env
```

Отредактируйте `.env`, указав данные вашей базы PostgreSQL.

## Миграции (Задание 9.1)

```bash
# Инициализация (уже выполнена)
# alembic init alembic

# Применить все миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1
```

## Запуск приложений

```bash
# Основное приложение (задание 11)
uvicorn main:app --reload

# Задание 10.1 — кастомные исключения
uvicorn task_10_1:app --reload --port 8001

# Задание 10.2 — валидация
uvicorn task_10_2:app --reload --port 8002
```

## Проверка функциональности

**Задание 10.1:**
```bash
curl http://localhost:8001/check/-5
curl http://localhost:8001/items/99
```

**Задание 10.2:**
```bash
curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "age": 25, "email": "john@example.com", "password": "secret123"}'
```

**Основное приложение:**
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "age": 25}'

curl http://localhost:8000/users/1
curl -X DELETE http://localhost:8000/users/1
```

## Запуск тестов

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Конкретный файл
pytest tests/test_11_1.py
pytest tests/test_11_2.py
```

## Swagger UI

После запуска: http://localhost:8000/docs
