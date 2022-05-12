# **ReviewBro**

### _Telegram-бот статуса домашки_

# Описание

Бот-ассистент обращается к API сервиса Практикум.Домашка и узнает статус работы, отправленной на проверку: взята ли работа в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Что делает бот:
- раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью работы;
- при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram-чат;
- логирует свою работу и сообщает о важных проблемах сообщением в Telegram-чат.

# Технологии

- [Python 3.8.8](https://www.python.org/downloads/release/python-388/)
- [python-telegram-bot 13.7](https://python-telegram-bot.readthedocs.io/en/stable/index.html)

# Установка

Клонируйте репозиторий и перейдите в него в командной строке:
```sh
git clone https://github.com/nickolaEO/reviewbro_bot.git
```
```sh
cd reviewbro_bot
```
Создайте и активируйте виртуальное окружение:
```sh
python -m venv venv
```
```sh
source venv/Scripts/activate
```
Установите зависимости из файла _requirements.txt_:
```sh
python -m pip install --upgrade pip
```
```sh
pip install -r requirements.txt
```

## License

MIT

**Free Software**
