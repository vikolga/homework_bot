# Проект Telegram-бот
«Проект Telegram-бот»

![Python](https://img.shields.io/badge/PYTHON-3776AB.svg?&style=flat&logo=python&logoColor=white)&nbsp;

## Оглавление
1. [Описание](#описание)
2. [Технологии](#технологии)
3. [Как запустить проект](#как-запустить-проект)
4. [Автор проекта](#автор-проекта)

## Описание
Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Ключевые возможности сервиса:
- раз в 10 минут опрашивает API сервис Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram;
- логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.

## Технологии
- Python 3.9
- библиотека telegram

## Как запустить проект

- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://git@github.com:vikolga/homework_bot.git
```
- Переходим в директорию проекта:
```
cd homework_bot
```

- Создаем и активируем виртуальное окружение:
```
python3 -m venv venv
```
* Если у вас Linux/macOS:
    ```
    source venv/bin/activate
    ```

* Если у вас windows:
    ```
    source venv/scripts/activate
    ```

- Пример заполнения конфигурационного .env файла
```
TELEGRAM_TOKEN=xxxxxx
PRACTICUM_TOKEN=xxxxxxxxx
TELEGRAM_CHAT_ID=xxxxxxxx
```

TELEGRAM_TOKEN  @BotFather зарегистрировать аккаунт бота в Telegram и получить Token

TELEGRAM_CHAT_ID  @userinfobot - узнать ID своего Telegram-аккаунта



- Обновляем менеджер пакетов pip:
```
pip install --upgrade pip
```

- Устанавливаем зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

- Запустить проект
```
python homework.py
```

- Запустить тесты
```
pytest
```

## Автор проекта
_[Ольга Викторова](https://github.com/vikolga/)_, python-developer
