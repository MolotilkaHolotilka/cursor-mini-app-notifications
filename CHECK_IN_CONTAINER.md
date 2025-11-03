# Проверка в контейнере

## Вы в контейнере, файлы на месте ✅

Проверим что все работает:

### Шаг 1: Проверьте структуру файлов

```bash
ls -la /app/
ls -la /app/static/
```

### Шаг 2: Проверьте что main.py правильный

```bash
cat /app/main.py | head -20
```

### Шаг 3: Попробуйте запустить Python напрямую

```bash
python -c "from fastapi import FastAPI; print('FastAPI imported OK')"
```

### Шаг 4: Проверьте что static файлы есть

```bash
ls -la /app/static/
cat /app/static/index.html | head -10
```

### Шаг 5: Проверьте порт (если есть netstat)

```bash
netstat -tlnp 2>/dev/null | grep 8000 || ss -tlnp | grep 8000
```

---

## Если нужно установить curl для теста:

```bash
apt-get update && apt-get install -y curl
curl http://localhost:8000
```

---

## Альтернатива: Использовать Python для проверки:

```bash
python -c "import requests; print(requests.get('http://localhost:8000').text[:200])" 2>/dev/null || python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000').read()[:200])"
```

---

## Главное - проверьте логи

Выйдите из контейнера и проверьте логи в Coolify - должно быть:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Если это есть, значит проблема в настройках Coolify (порт или проксирование).




