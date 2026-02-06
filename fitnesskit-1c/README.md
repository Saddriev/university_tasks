# FitnessKit 1C Integration

Django 4 + API: интеграция с 1С, получение списка сотрудников. Стиль кода — PEP8.

## Требования

- Python 3.10+
- Django 4+

## Установка

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd fitnesskit-1c && python manage.py migrate
python manage.py createsuperuser   # для админки
```

## Настройка (переменные окружения)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `ONEC_BASE_URL` | URL API 1С | `http://176.192.70.122:90/.../v1` |
| `ONEC_CLUB_ID` | Идентификатор клуба | из ТЗ |
| `ONEC_LOGIN` | Basic auth логин | `FitnessKit` |
| `ONEC_PASSWORD` | Basic auth пароль | из ТЗ |
| `DJANGO_SECRET_KEY` | Секрет Django | dev-secret |
| `DJANGO_DEBUG` | Режим отладки | `1` |

## Запуск (ASGI для async)

```bash
uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

Или для разработки:

```bash
python manage.py runserver 8000
```

## API

**GET** `/team/get_employees`

Возвращает JSON:

```json
{
  "employees": [
    {
      "id": "...",
      "name": "Имя",
      "last_name": "Фамилия",
      "phone": "+7...",
      "image_url": "https://..."
    }
  ]
}
```

При отсутствии поля в ответе 1С — в JSON уходит пустая строка `""`.

## Тесты

```bash
python manage.py test team
```

Проверяются: разбор ответа 1С, маппинг полей, эндпоинт при успехе и при ошибке (fallback и 502).

## Стиль и линтинг (PEP8)

```bash
pip install flake8
flake8 config team
```

## Админка

- URL: `http://localhost:8000/admin/`
- Логин/пароль: от созданного суперпользователя (`createsuperuser`).
