# Пошаговый гайд по деплою maxhub на Render

> ⚡ **Хотите самый простой способ?** Смотрите файл **[DEPLOY_SIMPLE_RU.md](DEPLOY_SIMPLE_RU.md)** - там детальная инструкция с указанием, куда нажимать и что вводить!

Этот гайд поможет вам развернуть ваш Django-проект maxhub на платформе Render.

## Подготовка проекта ✅

Проект уже подготовлен к деплою:
- ✅ Настроен PostgreSQL вместо SQLite
- ✅ Добавлен WhiteNoise для статических файлов
- ✅ Настроены параметры безопасности для продакшена
- ✅ Создан `render.yaml` для автоматического деплоя
- ✅ Обновлены зависимости (добавлен psycopg2-binary)

## Шаг 1: Создание аккаунта на Render

1. Перейдите на [render.com](https://render.com)
2. Нажмите "Get Started for Free"
3. Зарегистрируйтесь через GitHub, GitLab или email

## Шаг 2: Подготовка репозитория GitHub/GitLab

1. Убедитесь, что ваш проект находится в Git-репозитории (GitHub или GitLab)
2. Проверьте, что все изменения закоммичены:
   ```bash
   git status
   git add .
   git commit -m "Подготовка к деплою на Render"
   ```
3. Отправьте изменения в удаленный репозиторий:
   ```bash
   git push origin main
   ```
   (или `git push origin master`, в зависимости от вашей основной ветки)

## Шаг 3: Деплой через render.yaml (рекомендуемый способ)

### 3.1. Подключение репозитория

1. Войдите в панель Render
2. В Dashboard нажмите "New +" → "Blueprint"
3. Выберите ваш репозиторий (GitHub/GitLab)
4. Укажите ветку (обычно `main` или `master`)
5. Render автоматически обнаружит файл `render.yaml` и предложит развернуть все сервисы

### 3.2. Настройка переменных окружения

После создания Blueprint, Render автоматически:
- Настроит все переменные для подключения к БД
- Установит `DJANGO_ALLOWED_HOSTS` с хостом вашего сервиса

**Важно**: Вам нужно вручную установить `DJANGO_SECRET_KEY`:
1. Перейдите в раздел Environment для вашего веб-сервиса
2. Найдите `DJANGO_SECRET_KEY` (он будет помечен как `sync: false`)
3. Нажмите на поле и сгенерируйте безопасный ключ:
   - Можно использовать команду: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Или нажмите "Generate" в интерфейсе Render (если доступно)
4. Убедитесь, что `DJANGO_DEBUG` установлен в `false`

### 3.3. Автоматический деплой

Render автоматически:
- Создаст PostgreSQL базу данных
- Настроит переменные окружения для подключения к БД
- Выполнит миграции
- Соберет статические файлы
- Запустит приложение с Gunicorn

## Шаг 4: Деплой вручную (альтернативный способ)

Если вы хотите настроить сервисы вручную:

### 4.1. Создание PostgreSQL базы данных

1. В Dashboard нажмите "New +" → "PostgreSQL"
2. Назовите базу: `maxhub-db`
3. Выберите план: **Free** (для начала)
4. Выберите регион: ближайший к вам
5. Нажмите "Create Database"
6. Дождитесь создания БД (1-2 минуты)

### 4.2. Создание веб-сервиса

1. В Dashboard нажмите "New +" → "Web Service"
2. Подключите ваш репозиторий
3. Заполните настройки:
   - **Name**: `maxhub`
   - **Region**: тот же регион, что и БД
   - **Branch**: `main` (или ваша основная ветка)
   - **Root Directory**: оставьте пустым (если проект в корне)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```bash
     gunicorn maxhub.wsgi:application
     ```

### 4.3. Настройка переменных окружения

В разделе "Environment" добавьте следующие переменные:

**Обязательные:**
- `DJANGO_SECRET_KEY` - сгенерируйте безопасный ключ (можно использовать команду: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DJANGO_DEBUG` - установите `false`
- `DJANGO_ALLOWED_HOSTS` - автоматически заполнится после создания сервиса (например: `maxhub.onrender.com`)

**Для подключения к базе данных:**
- `DB_NAME` - скопируйте из Internal Database URL вашей БД (после `@` до `/`)
- `DB_USER` - скопируйте из Internal Database URL (до `:`)
- `DB_PASSWORD` - скопируйте из Internal Database URL (между `:` и `@`)
- `DB_HOST` - скопируйте из Internal Database URL (после `@` до `:`)
- `DB_PORT` - установите `5432`

**Как найти данные БД:**
1. Откройте вашу PostgreSQL базу данных в Render
2. В разделе "Connections" найдите "Internal Database URL"
3. Формат: `postgresql://user:password@host:5432/dbname`
4. Разберите URL и скопируйте нужные части

### 4.4. Создание суперпользователя

После успешного деплоя:

1. Откройте ваш веб-сервис в Render
2. Перейдите во вкладку "Shell"
3. Выполните команду:
   ```bash
   python manage.py createsuperuser
   ```
4. Введите username, email и password

## Шаг 5: Проверка работы

1. Дождитесь завершения деплоя (обычно 5-10 минут)
2. Откройте URL вашего приложения (будет показан в Dashboard)
3. Проверьте:
   - Главная страница загружается
   - Регистрация/вход работают
   - Дашборд доступен после входа
   - Статические файлы загружаются (CSS, изображения)

## Шаг 6: Важные замечания

### Медиа-файлы (важно!)

⚠️ **На Render Free плане медиа-файлы будут удаляться при каждом перезапуске сервиса!**

Рекомендации:
1. **Для продакшена**: Используйте внешнее хранилище (AWS S3, Cloudinary, или Render Disk)
2. **Для тестирования**: Free план подойдет, но помните об ограничениях

Чтобы настроить S3 (пример):
```python
# В settings.py добавьте:
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
```

И добавьте в `requirements.txt`:
```
boto3==1.34.0
django-storages==1.14.2
```

### Регистрация домена (опционально)

1. В настройках веб-сервиса перейдите в "Custom Domains"
2. Добавьте ваш домен
3. Настройте DNS записи согласно инструкциям Render

### Мониторинг и логи

- Логи доступны в реальном времени во вкладке "Logs" вашего сервиса
- Используйте их для отладки проблем

## Решение типичных проблем

### Проблема: "Application failed to respond"

**Решение**: 
- Проверьте логи сервиса
- Убедитесь, что Start Command указан правильно: `gunicorn maxhub.wsgi:application`
- Проверьте, что все переменные окружения настроены

### Проблема: "Static files not loading"

**Решение**:
- Убедитесь, что `collectstatic` выполняется в Build Command
- Проверьте, что WhiteNoise middleware добавлен в `settings.py`
- Проверьте, что `STATIC_ROOT` настроен правильно

### Проблема: "Database connection error"

**Решение**:
- Проверьте, что все переменные окружения БД установлены
- Убедитесь, что используется "Internal Database URL" (не External)
- Проверьте, что БД создана в том же регионе, что и веб-сервис

### Проблема: "Migration error"

**Решение**:
- Убедитесь, что `python manage.py migrate` включен в Build Command
- Проверьте логи на наличие ошибок миграций

## Обновление проекта

После каждого push в репозиторий Render автоматически:
1. Обнаружит изменения
2. Запустит новый build
3. Выполнит миграции (если есть)
4. Перезапустит сервис

Или вы можете вручную запустить "Manual Deploy" в панели Render.

## Полезные команды

Через Shell в Render вы можете выполнить:

```bash
# Создать суперпользователя
python manage.py createsuperuser

# Применить миграции
python manage.py migrate

# Собрать статику
python manage.py collectstatic --noinput

# Проверить конфигурацию
python manage.py check --deploy

# Открыть Django shell
python manage.py shell
```

## Поддержка

Если у вас возникли проблемы:
1. Проверьте логи в Render Dashboard
2. Убедитесь, что все переменные окружения установлены
3. Проверьте документацию Render: https://render.com/docs

---

**Удачи с деплоем! 🚀**

