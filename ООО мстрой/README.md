# TreeStore API (ООО мстрой)

API для работы с деревом объектов (`id`, `parent`): getAll, getItem, getChildren, getAllParents.

## Скриншот

![TreeStore API](screens/Снимок%20экрана%202026-02-07%20в%2003.19.46.png)


## Запросы (curl)

```bash
curl http://127.0.0.1:8000/api/v1/health
curl http://127.0.0.1:8000/api/v1/tree/getAll
curl -X POST http://127.0.0.1:8000/api/v1/tree/getItem -H "Content-Type: application/json" -d '{"id": 7}'
curl -X POST http://127.0.0.1:8000/api/v1/tree/getChildren -H "Content-Type: application/json" -d '{"id": 4}'
curl -X POST http://127.0.0.1:8000/api/v1/tree/getAllParents -H "Content-Type: application/json" -d '{"id": 7}'
```

