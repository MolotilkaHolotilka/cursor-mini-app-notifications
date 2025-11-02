# Настройка GitHub репозитория

## Шаг 1: Создать репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите "+" → "New repository"
3. Заполните:
   - **Repository name:** `telegram-notification-system` (или любое другое название)
   - **Description:** Telegram Mini App Notification System
   - **Visibility:** Public или Private (на ваше усмотрение)
   - **НЕ** добавляйте README, .gitignore или лицензию (они уже есть)
4. Нажмите "Create repository"

## Шаг 2: Подключить локальный репозиторий к GitHub

После создания репозитория GitHub покажет инструкции. Выполните команды:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

**Или через SSH (если настроен):**
```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Шаг 3: Если нужно обновить URL удалённого репозитория

Если репозиторий уже был подключен, но нужно изменить URL:

```bash
# Посмотреть текущий remote
git remote -v

# Изменить URL
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Или добавить новый
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Шаг 4: Отправить код на GitHub

```bash
git push -u origin main
```

## Если нужно авторизоваться

GitHub больше не принимает пароли. Используйте:

1. **Personal Access Token (PAT):**
   - Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Создайте токен с правами `repo`
   - Используйте токен вместо пароля

2. **Или GitHub CLI:**
   ```bash
   gh auth login
   ```

## Проверка

После успешного push:
- Зайдите на GitHub
- Проверьте что все файлы загружены
- Убедитесь что есть README.md, Dockerfile и все нужные файлы

---

## Дальше: Подключение к Coolify

После того как код на GitHub:

1. В Coolify выберите "New Resource"
2. Выберите "Git Repository"
3. Подключите ваш GitHub репозиторий
4. Coolify автоматически найдет Dockerfile
5. Задеплойте!

