# Настройка своего домена в Coolify

## Используйте свой домен: rybushk.in

### Шаг 1: Настройка DNS

Нужно добавить A-запись или CNAME в настройках вашего домена `rybushk.in`:

**Вариант А: Поддомен (рекомендуется)**
- Используйте поддомен: `notifications.rybushk.in` или `notify.rybushk.in`

**Вариант Б: Корневой домен**
- Используйте `rybushk.in` (но это заменит главный сайт)

---

## Инструкция по настройке:

### 1. Узнайте IP адрес вашего Coolify сервера

В Coolify:
- Settings → General → найдите IP адрес сервера
- Или посмотрите текущий домен: `91.107.212.137` (из sslip.io URL)

### 2. Настройте DNS запись

Зайдите в панель управления вашим доменом (где покупали/регистрировали rybushk.in):

**Если используете поддомен (например: notifications.rybushk.in):**
```
Тип: A
Имя: notifications (или @ для корневого домена)
Значение: 91.107.212.137
TTL: 3600 (или Auto)
```

**Или используйте CNAME:**
```
Тип: CNAME
Имя: notifications
Значение: q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io
TTL: 3600
```

### 3. Добавьте домен в Coolify

1. В настройках приложения найдите **"Domains"** или **"FQDNs"**
2. Нажмите **"Add Domain"** или **"Generate Domain"**
3. Введите ваш домен:
   - `notifications.rybushk.in` (если поддомен)
   - Или `rybushk.in` (если корневой)
4. **ВАЖНО:** Уберите `http://` - должно быть просто домен!
5. Сохраните

### 4. Обновите Container Labels (Traefik)

Замените домен в "Container Labels" на ваш:

**Было:**
```
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.rule=Host(`q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io`) && PathPrefix(`/`)
```

**Должно быть (пример для notifications.rybushk.in):**
```
traefik.http.routers.http-0-q84oskg0cs044ogwkok0os04.rule=Host(`notifications.rybushk.in`) && PathPrefix(`/`)
traefik.http.routers.https-0-q84oskg0cs044ogwkok0os04.rule=Host(`notifications.rybushk.in`) && PathPrefix(`/`)
```

---

## Полная конфигурация для вашего домена:

Замените `notifications.rybushk.in` на нужный поддомен или корневой домен:

```
traefik.enable=true
traefik.http.middlewares.gzip.compress=true
traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https
traefik.http.routers.http-0-notifications.entryPoints=http
traefik.http.routers.http-0-notifications.middlewares=redirect-to-https
traefik.http.routers.http-0-notifications.rule=Host(`notifications.rybushk.in`) && PathPrefix(`/`)
traefik.http.routers.http-0-notifications.service=http-0-notifications
traefik.http.services.http-0-notifications.loadbalancer.server.port=8000
traefik.http.routers.https-0-notifications.entryPoints=https
traefik.http.routers.https-0-notifications.rule=Host(`notifications.rybushk.in`) && PathPrefix(`/`)
traefik.http.routers.https-0-notifications.service=http-0-notifications
traefik.http.routers.https-0-notifications.tls=true
traefik.http.routers.https-0-notifications.tls.certresolver=letsencrypt
traefik.http.routers.https-0-notifications.middlewares=gzip
```

---

## Рекомендуемые варианты поддоменов:

- `notifications.rybushk.in` ✅
- `notify.rybushk.in` ✅
- `app.rybushk.in` ✅
- `telegram.rybushk.in` ✅

---

## После настройки:

1. **Подождите 5-15 минут** - DNS записи распространяются
2. **Проверьте DNS:** Используйте https://dnschecker.org чтобы проверить что A-запись распространилась
3. **Coolify автоматически выдаст SSL** для вашего домена через Let's Encrypt
4. **Проверьте:** откройте `https://notifications.rybushk.in` в браузере

---

## Для Telegram BotFather:

После настройки отправьте:
```
https://notifications.rybushk.in
```

Или какой поддомен вы выберете.

---

## Проверка DNS:

Через командную строку:
```bash
nslookup notifications.rybushk.in
```

Должен вернуть IP: `91.107.212.137`

---

**Выберите поддомен и настроим! 🚀**

