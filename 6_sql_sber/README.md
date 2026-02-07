# SQL #103 — Сбербанк

**Задача:** Вывести список имён сотрудников, получающих большую зарплату, чем у непосредственного руководителя.

## Решение

```sql
SELECT e.name
FROM employees e
INNER JOIN employees chief ON e.chief_id = chief.id
WHERE e.salary > chief.salary
ORDER BY e.name;
```


## Результат

![Результат выполнения](images/Снимок%20экрана%202026-02-07%20в%2004.04.10.png)
