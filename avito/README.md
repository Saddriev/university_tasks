# URL Shortener API

Сервис сокращения ссылок (аналог Bitly).

![Работа API](screens/screenshot.png)

## Запуск

```bash
cd avito
bash run.sh
```

Сервер: http://127.0.0.1:8000. API-документация: http://127.0.0.1:8000/api/v1/docs

## API

- `POST /api/v1/shorten` — создать короткую ссылку
- `GET /api/v1/health` — проверка работоспособности
- `GET /{short_code}` — редирект на оригинальный URL

## Пример

```bash
curl -X POST http://127.0.0.1:8000/api/v1/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com"}'
```
