# Barter System

Платформа для обмена вещами между пользователями (Django + DRF + Bootstrap)

---

## Быстрый старт (локально)

1. **Клонируйте репозиторий и перейдите в папку проекта:**
   ```sh
   git clone https://github.com/7Lainero7/effective_mobile_test_task.git
   cd effective_mobile_test_task
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   # или
   source venv/bin/activate  # Linux/Mac
   ```

3. **Установите зависимости:**
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Создайте файл `.env` (пример уже есть):**
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=barter
   DB_USER=barter
   DB_PASSWORD=barter
   DB_HOST=localhost
   DB_PORT=5432
   DB_SCHEMA=barter_system
   ```

5. **Выполните миграции:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Создайте суперпользователя:**
   ```sh
   python manage.py createsuperuser
   ```

7. **Запустите сервер:**
   ```sh
   python manage.py runserver
   ```

8. **Откройте в браузере:**
   - [http://localhost:8000/](http://localhost:8000/) — HTML-интерфейс
   - [http://localhost:8000/api/](http://localhost:8000/api/) — REST API

---

## Быстрый старт в Docker

1. **Запустите контейнеры:**
   ```sh
   docker-compose up --build
   ```

2. **Выполните миграции и создайте суперпользователя:**
   ```sh
   docker-compose run web python manage.py migrate
   docker-compose run web python manage.py createsuperuser
   ```

3. **Откройте [http://localhost:8000/](http://localhost:8000/)**

---

## Основные команды

- **Миграции:**  
  `python manage.py makemigrations`  
  `python manage.py migrate`

- **Создать суперпользователя:**  
  `python manage.py createsuperuser`

- **Запуск тестов:**  
  `python manage.py test`

- **Запуск сервера:**  
  `python manage.py runserver`

---

## Функционал

- Регистрация, вход/выход пользователей
- CRUD для объявлений (через HTML и API)
- Поиск и фильтрация объявлений
- Создание и обработка предложений обмена (через API)
- Bootstrap-оформление HTML-интерфейса

---

## Страницы

- `/` — список объявлений, создание/редактирование/удаление (HTML)
- `/register/` — регистрация пользователя
- `/accounts/login/` — вход
- `/accounts/logout/` — выход
- `/api/ads/` — REST API для объявлений
- `/api/proposals/` — REST API для предложений обмена

---

## Проверка стиля кода

```sh
flake8 .
```

---

## Примечания

- Для работы с PostgreSQL требуется установленный сервер БД (или используйте Docker).
- Для локального теста можно временно переключиться на SQLite, изменив настройки в `.env` и `settings.py`.

---
