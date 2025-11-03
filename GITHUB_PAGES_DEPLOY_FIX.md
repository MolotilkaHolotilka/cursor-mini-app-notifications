# Исправление проблемы с деплоем на GitHub Pages

## Проблема

Деплой на GitHub Pages зацикливается на проверке статуса и превышает таймаут.

## Решение

Создан упрощенный workflow файл `.github/workflows/deploy-pages.yml`, который:

1. **Не использует Jekyll** - просто копирует статические файлы
2. **Создает `.nojekyll`** - отключает обработку Jekyll для GitHub Pages
3. **Копирует файлы из корня** - `index.html`, `app.js`, `styles.css`
4. **Устанавливает таймаут** - 5 минут для деплоя

## Что нужно сделать

1. **Закоммитить workflow файл:**
   ```bash
   git add .github/workflows/deploy-pages.yml
   git commit -m "Fix GitHub Pages deployment workflow"
   git push
   ```

2. **Настроить GitHub Pages (если еще не настроено):**
   - Перейдите в Settings → Pages вашего репозитория
   - Source: выберите "GitHub Actions" (не "Deploy from a branch")
   - Сохраните

3. **Проверить деплой:**
   - После push workflow должен запуститься автоматически
   - Проверьте статус в Actions → Deploy to GitHub Pages
   - Если все хорошо, сайт будет доступен по адресу:
     `https://molotilkaholotilka.github.io/cursor-mini-app-notifications/`

## Альтернативный вариант (если workflow не работает)

Можно использовать простой деплой через ветку:

1. **Settings → Pages**
2. **Source:** "Deploy from a branch"
3. **Branch:** `main` → `/` (root)
4. **Save**

GitHub автоматически будет деплоить файлы из корня ветки `main`.

## Проверка

После деплоя проверьте:
- Сайт открывается: `https://molotilkaholotilka.github.io/cursor-mini-app-notifications/`
- Файлы загружаются: `app.js`, `styles.css`
- API запросы работают (проверьте в консоли браузера)

## Устранение проблем

Если деплой все еще не работает:

1. **Проверьте логи Actions:**
   - Перейдите в Actions → выберите последний workflow run
   - Посмотрите логи каждого шага

2. **Убедитесь, что файлы существуют:**
   - `index.html` в корне
   - `app.js` в корне
   - `styles.css` в корне

3. **Проверьте права:**
   - Settings → Actions → General
   - Workflow permissions должны быть: "Read and write permissions"


