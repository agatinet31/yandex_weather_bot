## Описание проекта:
Сервис онлайн погоды Yandex Weather
## Подготовка окружения для разработки

### Создание Docker контейнеров:
Создать файл .env с переменными окружения для работы с базой данных PostgreSQL:
```
# Ключ доступа Yandex API
X_YANDEX_API_KEY=12345678951231545abcdefgh
# Токен бота
BOT_TOKEN=fgdjhj1bnng3h2315gh5x2dc1h
# Указываем, что работаем с postgresql
DB_ENGINE=django.db.backends.postgresql
# Имя базы данных
DB_NAME=ya_weather
# Логин для подключения к базе данных
POSTGRES_USER=postgres
# Пароль для подключения к БД (установите свой)
POSTGRES_PASSWORD=postgres
# Название сервиса (контейнера)
DB_HOST=db (localhost для локального подключения к БД)
# Порт для подключения к БД
DB_PORT=5432
# PGAdmin
PGADMIN_DEFAULT_EMAIL=admin@info.ya
PGADMIN_DEFAULT_PASSWORD=12345
```

Перейти в директорию infra:
```
cd infra
```

Создаем и запускаем сервисы приложения:
```
docker-compose up -d --build
```

Создать базу данных в контейнере db:
```
psql -U postgres -c 'create database ya_weather;'
```

Выполнить миграции в контейнере backend:
```
python manage.py migrate
```

Импортировать данные:
```
python manage.py import_json --path ./data/import-russian-cities.json --model YandexWeatherModel
```

Swagger документация проекта:
```
http://127.0.0.1/api/schema/swagger-ui
```

Доступ PGAdmin:
```
http://127.0.0.1/pgadmin4
```

### Предварительные требования(backend):
1. **Poetry** \
Зависимости и пакеты управляются через **poetry**. Убедитесь, что **poetry** [установлен](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) на вашем компьютере и ознакомьтесь с [документацией](https://python-poetry.org/docs/cli/).
```
- Устанавливаем Poetry версия 1.4.0
    curl -sSL https://install.python-poetry.org | python - --version 1.4.0
- Добавляем Poetry в переменную среды PATH
    "$HOME/.local/bin" для Unix.
    "%APPDATA%\Python\Scripts" для Windows.
```
2. **Docker**
3. Файлы **requirements** \
Файлы редактировать вручную не нужно. Обновление происходит автоматически через pre-commit хуки.
4. **pre-commit хуки** \
[Документация](https://pre-commit.com)\
При каждом коммите выполняются хуки перечисленные в **.pre-commit-config.yaml**.
Если при коммите возникает ошибка, можно запустить хуки вручную:
    ```
    pre-commit run --all-files
    ```

### Запуск проекта:
1. Клонировать репозиторий и перейти в него в командной строке:
    ```
    git clone git@github.com:agatinet31/yandex_weather_bot.git
    cd yandex_weather_bot
    ```
2. Убедитесь что poetry установлен. Активируйте виртуальное окружение. Установите зависимости
    ```
    poetry shell
    poetry install
    ```
3. Установите pre-commit хуки
    ```
    pre-commit install --all
    ```
4. Убедитесь, что при запуске используется правильное виртуальное окружение.
Посмотреть путь можно следующей командой:
    ```
    poetry env info --path
    ```
5. Запуск проекта:
    ```
    python ./backend/manage.py runserver
    ```
