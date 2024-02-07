# referral

Тестовое задание регистрации по реферальным ключам

Локальный запуск проекта


```
docker compose up
```

При первом запуске нужно выполнить миграции.
```
docker compose exec backend python manage.py migrate
```

Документация:


backend\docs\schema.yaml


Запрос к API hunter.io осуществляется в celery worker контейнере.
Ответ от API можно увидеть там же или в БД.