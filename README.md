# Foodgram

**Foodgram** — это веб-приложение для публикации рецептов, добавления их в избранное и список покупок.

## Оглавление

- [Описание](#описание)
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [Переменные окружения](#переменные-окружения)
- [Использование](#использование)
- [Авторы](#авторы)

## Описание

Foodgram позволяет пользователям публиковать рецепты, добавлять их в избранное, формировать список покупок и подписываться на авторов.

## Технологии

- Python 3.10+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Docker, Docker Compose
- Gunicorn/Nginx (для продакшн)
- drf-spectacular (Swagger/OpenAPI)

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/zitaisan/foodgram-st.git
cd foodgram-st
```

### 2. Создайте и настройте `.env` файл

Создайте файл `.env` в корне проекта и добавьте переменные окружения:

### 3. Запустите проект с помощью Docker


```bash
docker-compose up --build
```

### 4. Примените миграции, создайте суперпользователя

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

### 6. Проект будет доступен по адресу
http://localhost/

## Использование

- Документация API: `http://localhost/api/docs/`
- Админка: `http://localhost/admin/`

## Автор

- [zitaisan](https://github.com/zitaisan)


