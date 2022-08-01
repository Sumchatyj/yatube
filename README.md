# yatube

## Описание

Проект Yatube — это платформа для публикаций, блог. У пользователей есть возможность публиковать записи, комментировать их и подписываться на других авторов.


## Как запустить проект

### Зависимости

* Python 3.7
* Django 3.2.3
* djangorestframework 3.12.4

### Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Sumchatyj/yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

### Запуск

Запустить проект:

```
python3 manage.py runserver
```
