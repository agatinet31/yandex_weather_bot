## Описание проекта:
Сервис онлайн погоды Yandex Weather
## Подготовка окружения для разработки

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
5. Создать базу данных PostgreSQL:
    ```
    DB_NAME=ya_weather
    ```
6. Создать файл .env с переменными окружения для работы с базой данных PostgreSQL:

    ```
    # Ключ доступа Yandex API
    X_Yandex_API_Key=12345678951231545abcdefgh
    # Доступ с хостов
    ALLOWED_HOSTS=127.0.0.1
    # Доменное имя
    PRODUCTION_HOSTS=example.org
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
    ```
7. Применить миграции
    ```
    python ./backend/manage.py migrate --settings=yandex_weather.settings.develop
    ```
8. Запуск проекта с настройками develop:
    ```
    python ./backend/manage.py runserver --settings=yandex_weather.settings.develop
    ```
### Создание Docker контейнеров:
Перейти в директорию infra:
```
cd infra
```

Создаем и запускаем сервисы приложения:

```
docker-compose up
```

Создать базу данных:
```
docker exec -it {имя контейнера БД} /bin/bash
psql -U postgres -c 'create database ya_weather;'
```

Выполнить миграции:

```
docker-compose exec backend python manage.py migrate
```
