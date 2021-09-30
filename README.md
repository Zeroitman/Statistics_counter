### Инструкция по поднятию проекта локально и описание методов api

#### Поднятие проекта локально

1) Установите python на ваш пк [Python](https://www.python.org/downloads/)
2) Установите пакет менеджер [pip](https://pip.pypa.io/en/stable/)

Ссылка на репозиторий проекта [Gitlab](https://github.com/Zeroitman/Statistics_counter)

Установка:
- Склонировать проект из репозитория
- Зайдите в папку проекта и создайте виртуальное окружение c помощью команды 
```bash
sudo pip install virtualenv
```
- В папке проекта пропишите в консоли команду для установки виртуального окружения:
```bash
virtualenv -p python3.7 venv
```
- После установки можно будет активировать виртуальное окружение:
```bash
source venv/bin/activate
```
- Установите все зависимости проекта:
```bash
pip install -r requirements.txt
```
- Проведите миграции:
```bash
./manage.py migrate
```

- Создайте суперпользователя(по желанию):
```bash
./manage.py createsuperuser
```
- Запустите проект:

```bash
./manage.py runserver
```
- Для останоки проекта:
```bash
CTRL + C
```
- Для запуска тестов:
```bash
./manage.py test
```
#### Поднятие проекта локально

В файле docker-compose поменяйте переменные(environment) на свои

```
services:
  statistics-counter-db:
    environment:
        POSTGRES_PASSWORD: 12qwaszx
        POSTGRES_USER: project_db_user
        POSTGRES_DB: project_db

  web:
    environment:
        DB_HOST=statistics-counter-db
        DB_USER=project_db_user
        DB_PASS=12qwaszx
        DB_NAME=project_db
        DB_PORT=5432
        API_SECURE_KEY=ENtqH5i7DP22Mcenu1u6Ok7diyTCVLFmKzT1vlXyOTlirIf4yG
        DEBUG=True
```

Запустите команду 
```bash
 sudo docker-compose build
```

Далее выполните команду 
```bash
 sudo docker-compose up
```

#### Описание методов API

В headers необходимо передавать ключ безопасности во всех api запросах

HEADERS
```
API-SECURE-KEY:       # Ключ безопасности(строка). Например ENtqH5i7DP22Mcenu1u6Ok7diyTCVLFmKzT1vlXyOTlirIf4yG
```

##### POST /save-statistic

Сохранение статистики

Тело запроса: multipart/form-data
```
date        # Дата в формате YYYY-MM-DD (строка, обязательное поле)
views       # Количество показов (число, опциональное поле, по умолчанию 0)
clicks      # Количество откликов (число, опциональное поле, по умолчанию 0)
cost        # Стоимость откликов в рублях (положительное вещественное число с двумя цифрами после запятой, по умолчанию 0,00)
```
Тело ответа при положительном ответе:
```
{
    "result": "SUCCESSFULLY_ADDED_STATISTIC",
    "resultCode": 201
}
```

##### DELETE /delete-statistic

Метод сброса статистики (удаление всей статистики)

Тело ответа после успешного удаления статистики:
```
{
    "result": "STATISTIC_SUCCESSFULLY_DELETED",
    "resultCode": 410
}
```

##### GET /get-statistic

Получение списка пользователей с фильтрами

Передайте в Query Params следующие поля:
```
from            # Дата начала периода, включительно (дата в формате YYYY-MM-DD, обязательное поле)
to              # Дата окончания периода, включительно (дата в формате YYYY-MM-DD, обязательное поле)
sort_by_field   # Поле по которому осуществиться сортировка данных в ответе 
                  (строка, опционально, если не указать значение, сортировка осуществится по дате)
```
Тело ответа при наличии данных:
```
{
    "result": [
        {
            "date": "2021-02-12",
            "views": 0,
            "clicks": 0,
            "cost": 0.03,
            "cpc": 0,
            "cpm": 0
        },
        {
            "date": "2021-09-30",
            "views": 0,
            "clicks": 0,
            "cost": 0.03,
            "cpc": 0,
            "cpm": 0
        }
    ],
    "resultCode": 200
}
```