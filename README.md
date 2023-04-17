# Сократитель ссылок

Сервис для создания сокращённой формы передаваемых URL и анализа активности их использования.

## Описание

`http`-сервис, который обрабатывает поступающие запросы.

<details>
<summary> Список возможных эндпойнтов </summary>

- Посмотреть все ссылки:
```text
GET /api/v1/shorten
```

- Посмотреть конкретную ссылку:
```text
GET /api/v1/shorten/<shorten-url-id>
```

- Получить сокращённый вариант одного переданного URL:
```text
POST /api/v1/shorten
```

- Получить сокращённый вариант нескольких переданных URL (batch upload):
```text
POST /api/v1/shorten/bulk
```

- Получить статус доступности БД:
```text
POST /api/v1/shorten/ping
```

- Получить статистику переходов по ссылкам:
```text
POST /api/v1/shorten/status?[full-info]&[max-result=10]&[offset=0]
```

- Получить статистику переходов по конкретной ссылке:
```text
POST /api/v1/shorten/<shorten-url-id>/status?[full-info]&[max-result=10]&[offset=0]
```

- Вернуть оригинальный URL:
```text
GET /api/v1/shorten/transfer/<shorten-url-id>
```
</details>
