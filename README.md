# maxhub — электронные визитки и портфолио (MVP)

Минимальный Django-проект для создания публичных визиток `/card/<username>/` и личного кабинета для управления профилем, портфолио и отзывами.

## Стек
- Python 3.10+
- Django 4.2 LTS
- Bootstrap 5 (CDN)
- SQLite (по умолчанию)

## Быстрый старт
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


python manage.py createsuperuser
```


Открыть:
- Публичная визитка: `http://127.0.0.1:8000/card/<username>/`
- Кабинет/логин: `http://127.0.0.1:8000/accounts/login/` или `/dashboard/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Основные сущности
- `User` (кастомная модель, хранит заголовок, био, аватар, тему, акцентный цвет)
- `SocialLink` (контакты/соцсети)
- `PortfolioItem` (проекты)
- `Testimonial` (отзывы)

## Структура интерфейса
- Публичная карточка: аватар, имя, тайтл, блок «Обо мне», сетка портфолио, блок отзывов, кнопки контактов.
- Кабинет: дашборд с метриками, редактор профиля, списки/формы для портфолио, отзывов, ссылок.

## Переменные окружения (опционально)
- `DJANGO_SECRET_KEY` — секретный ключ
- `DJANGO_DEBUG` — `true/false`
- `DJANGO_ALLOWED_HOSTS` — через запятую

## Следующие шаги
- Добавить генерацию vCard/PDF.
- Подключить ограничения на загрузку файлов и reCAPTCHA/ throttle для формы.
- Вынести статику на CDN и переключить БД на PostgreSQL для продакшена.

