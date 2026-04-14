## Запуск приложений
bash
# Задание 11 — основное приложение
uvicorn main:app --reload --port 8080

# Задание 10.1 — кастомные исключения
uvicorn task_10_1:app --reload --port 8001

# Задание 10.2 — валидация данных
uvicorn task_10_2:app --reload --port 8002


## Swagger UI

- Основное приложение: http://localhost:8080/docs
- Кастомные исключения: http://localhost:8001/docs
- Валидация: http://localhost:8002/docs

**Задание 10.1 — кастомные исключения:**
bash
# CustomExceptionA (400) — отрицательное значение
curl http://localhost:8001/check/-5

# CustomExceptionB (404) — несуществующий item
curl http://localhost:8001/items/99

**Задание 10.2 — валидация:**
bash
# Успешный запрос
curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "age": 25, "email": "john@example.com", "password": "secret123"}'

# Ошибка валидации (age <= 18)
curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "age": 15, "email": "john@example.com", "password": "secret123"}'


**Основное приложение (задания 11.1 и 11.2):**
bash
# Создать пользователя
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "age": 25}'

# Получить пользователя
curl http://localhost:8080/users/1

# Удалить пользователя
curl -X DELETE http://localhost:8080/users/1

## Запуск тестов
bash
pytest -v
