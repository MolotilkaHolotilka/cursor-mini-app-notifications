# Настройка HTTPS роутера в Traefik (Coolify)

## Проблема:
У вас настроен только HTTP роутер, но нет HTTPS роутера с SSL сертификатом.

## Решение: Добавить HTTPS роутер

В разделе **"Container Labels"** добавьте следующие строки к существующим:

```yaml
traefik.enable=true

# HTTP роутер (существующий)
traefik.http.middlewares.gzip.compress=true
traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.entryPoints=http
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.middlewares=gzip
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.rule=Host(`q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io`) && PathPrefix(`/`)
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.service=http-0-q84oskg0cs044ogwkok0os04
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.middlewares=redirect-to-https
traefik.http.services.http-0-q84oskg0cs044ogwkok0os04.loadbalancer.server.port=8000

# HTTPS роутер (ДОБАВЬТЕ ЭТО!)
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.entryPoints=https
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.rule=Host(`q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io`) && PathPrefix(`/`)
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.service=http-0-q84oskg0cs044ogwkok0os04
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.tls=true
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.tls.certresolver=letsencrypt
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.middlewares=gzip

# Caddy настройки (если используете Caddy)
caddy_0.encode=zstd gzip
caddy_0.handle_path.0_reverse_proxy={{upstreams 8000}}
caddy_0.handle_path=/*
caddy_0.header=-Server
caddy_0.try_files={path} /index.html /index.php
caddy_0=http://q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io
caddy_ingress_network=coolify
```

---

## Важные изменения:

### 1. Добавить редирект на HTTPS для HTTP роутера:
Добавьте в существующий HTTP роутер:
```
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.middlewares=redirect-to-https
```

### 2. Добавить HTTPS роутер:
```
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.entryPoints=https
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.rule=Host(`q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io`) && PathPrefix(`/`)
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.service=http-0-q84oskg0cs044ogwkok0os04
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.tls=true
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.tls.certresolver=letsencrypt
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.middlewares=gzip
```

---

## Полная конфигурация для копирования:

Скопируйте это в "Container Labels":

```
traefik.enable=true
traefik.http.middlewares.gzip.compress=true
traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.entryPoints=http
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.middlewares=redirect-to-https
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.rule=Host(`q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io`) && PathPrefix(`/`)
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.service=http-0-q84oskg0cs044ogwkok0os04
traefik.http.services.http-0-q84oskg0cs044ogwkok0os04.loadbalancer.server.port=8000
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.entryPoints=https
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.rule=Host(`q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io`) && PathPrefix(`/`)
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.service=http-0-q84oskg0cs044ogwkok0os04
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.tls=true
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.tls.certresolver=letsencrypt
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.middlewares=gzip
```

---

## После сохранения:

1. **Сохраните настройки** в Coolify
2. **Перезапустите приложение** (Restart/Redeploy)
3. **Подождите 2-3 минуты** - Let's Encrypt выдаст сертификат
4. **Проверьте:** откройте `https://your-domain` в браузере

---

## Альтернатива: Использовать встроенные настройки Coolify

Если в Coolify есть встроенная настройка SSL:
1. Зайдите в настройки домена
2. Найдите "SSL" или "TLS"
3. Включите "Let's Encrypt" или "Auto SSL"
4. Coolify автоматически добавит нужные labels

---

## Проверка:

После добавления HTTPS роутера:
- `http://` → автоматически редиректит на `https://`
- `https://` → работает с SSL сертификатом
- Можно отправлять HTTPS URL в BotFather!

---

**Добавьте HTTPS роутер и перезапустите приложение! 🚀**



