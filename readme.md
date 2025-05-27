# Barter System

Платформа для обмена вещами между пользователями, построенная с использованием Django, Django REST Framework и Bootstrap.

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
   _Примечание:_ Для локального теста можете временно переключиться на SQLite, изменив настройки в `.env` и файле `barter_system/settings.py`.

5. **Выполните миграции:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Загрузите тестовые данные из фикстуры:**
   Файл `initial_data.json` находится в папке `ads/fixtures/`. Для его загрузки выполните:
   ```sh
   python manage.py loaddata initial_data.json
   ```

7. **Запустите тесты:**
   ```sh
   python manage.py test
   ```

8. **Создайте суперпользователя:**
   ```sh
   python manage.py createsuperuser
   ```

9. **Запустите сервер:**
   ```sh
   python manage.py runserver
   ```

10. **Откройте в браузере:**
    - [http://localhost:8000/](http://localhost:8000/) — HTML-интерфейс
    - [http://localhost:8000/api/](http://localhost:8000/api/) — REST API

---

## Быстрый старт в Docker

1. **Запустите контейнеры:**
   ```sh
   docker-compose up --build
   ```

2. **Выполните миграции и создайте суперпользователя:**
   В отдельном терминале выполните:
   ```sh
   docker-compose run web python manage.py migrate
   docker-compose run web python manage.py createsuperuser
   ```

3. **(Опционально) Загрузите тестовые данные из фикстуры:**
   ```sh
   docker-compose run web python manage.py loaddata initial_data.json
   ```

4. **Запустите тесты:**
   ```sh
   docker-compose run web python manage.py test
   ```

5. **Откройте приложение в браузере:**
   Перейдите по адресу [http://localhost:8000/](http://localhost:8000/)

---

## Основные команды

- **Миграции:**
  ```sh
  python manage.py makemigrations
  python manage.py migrate
  ```
  Или в Docker:
  ```sh
  docker-compose run web python manage.py makemigrations
  docker-compose run web python manage.py migrate
  ```

- **Создать суперпользователя:**
  ```sh
  python manage.py createsuperuser
  ```
  В Docker:
  ```sh
  docker-compose run web python manage.py createsuperuser
  ```

- **Запуск тестов:**
  ```sh
  python manage.py test
  ```
  Или в Docker:
  ```sh
  docker-compose run web python manage.py test
  ```

- **Запуск сервера (локально):**
  ```sh
  python manage.py runserver
  ```
  В Docker контейнере сервер уже запускается через команду в docker-compose.

- **Загрузка тестовых данных из фикстуры:**
  ```sh
  python manage.py loaddata initial_data.json
  ```
  Или в Docker:
  ```sh
  docker-compose run web python manage.py loaddata initial_data.json
  ```

---

## Функционал

- Регистрация, вход/выход пользователей.
- CRUD (создание, редактирование, удаление) для объявлений как через HTML-интерфейс, так и через API.
- Поиск и фильтрация объявлений по ключевым словам (title и description), категориям и состоянию.
- Создание и обработка предложений обмена (с разделением на отправленные и полученные) через HTML-интерфейс и REST API.
- Адаптивный дизайн интерфейса с использованием Bootstrap.

---

## Основные страницы

- **HTML‑интерфейс:**
  - `/` — список объявлений с возможностью создания, редактирования и удаления.
  - `/register/` — регистрация пользователя.
  - `/accounts/login/` — страница входа.
  - `/accounts/logout/` — страница выхода.
  - `/proposals/public/` — страница со всеми предложениями обмена (публичная).
  - `/proposals/my/` — страница с предложениями обмена, связанными с текущим пользователем (личная).

- **REST API:**
  - `/api/ads/` — API для работы с объявлениями.
  - `/api/proposals/` — API для работы с предложениями обмена.
  - `/api/users/` — API для получения информации о пользователях.


## Документация API

Для удобного изучения и тестирования API проекта используются интерактивные интерфейсы:

- **Swagger UI:**  
  Перейдите по адресу [http://localhost:8000/api/swagger-ui/](http://localhost:8000/api/swagger-ui/)  
  Здесь вы сможете просмотреть сгенерированную OpenAPI-схему, исследовать доступные эндпоинты и отправлять тестовые запросы.

- **ReDoc:**  
  Перейдите по адресу [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)  
  Этот интерфейс предоставляет подробную и структурированную документацию по API.

Оба интерфейса используют drf-spectacular для генерации схемы и удобной работы с API. Если вы хотите обновить схему, просто перезапустите сервер – изменения в коде будут автоматически отражены в документации.

---

## Проверка стиля кода

Для проверки стиля кода выполните:
```sh
flake8 .
```
Или через Docker:
```sh
docker-compose run web flake8 .
```

---

## Примечания

- Для работы с PostgreSQL требуется установленный или запущенный в Docker сервер БД.
- Для локального тестирования можно временно переключиться на SQLite, изменив настройки в файле `.env` и `barter_system/settings.py`.

---

Эта инструкция охватывает как локальный запуск проекта, так и работу в Docker‑окружении, а также описывает основные функции и страницы системы.