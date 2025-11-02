# Примеры запросов для тестирования API

Сервер: `http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io`

## 1. Health Check
```bash
curl http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/health
```

Ожидаемый ответ:
```json
{"status":"ok","message":"App is running"}
```

## 2. Получить статистику
```bash
curl http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/api/stats
```

## 3. Получить все уведомления (первые 10)
```bash
curl "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/api/notifications?limit=10"
```

## 4. Получить уведомления с фильтром по типу
```bash
curl "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/api/notifications?type=file_upload&limit=5"
```

## 5. Получить уведомления с фильтром по пользователю
```bash
curl "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/api/notifications?user_id=manager_a&limit=10"
```

## 6. Получить только непрочитанные
```bash
curl "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/api/notifications?status=unread&limit=20"
```

## 7. Пометить уведомление как прочитанное
```bash
curl -X POST "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/api/notifications/1/read" -H "Content-Type: application/json"
```

## 8. Интерактивная документация

### Swagger UI (рекомендуется)
```
http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/docs
```

### ReDoc
```
http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/redoc
```

## Примеры для PowerShell (Windows)

```powershell
# Health check
Invoke-RestMethod -Uri "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/health"

# Статистика
Invoke-RestMethod -Uri "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/api/stats"

# Уведомления
Invoke-RestMethod -Uri "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io/api/notifications?limit=10"
```

## Примеры для Python

```python
import requests

BASE_URL = "http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Статистика
response = requests.get(f"{BASE_URL}/api/stats")
print(response.json())

# Уведомления
response = requests.get(f"{BASE_URL}/api/notifications", params={"limit": 10})
print(response.json())
```


