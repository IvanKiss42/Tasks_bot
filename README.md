## Tasks_bot
### Tasks bot это простой бот позволяющий создавать список дел, добавлять в него новые записи и удалять старые.

> [!NOTE]
> Бот настроен на работу с PostgreSQL, для использования бота, после клонирования репозитория, в корневой папке создайте файл config.py и заполните его по образцу config.example.py.

Для активации бота последовательно воспользуйтесь командами:
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py Bot.py
```

:left_speech_bubble: Бот обрабатывает команды:
+ /start - приветствие и начало работы
+ /help - помощь с функционалом
+ /add - добавление задачи в БД
+ /tsk - вывод списка задач
+ /delete - удаление задачи из БД

:desktop_computer: Стек и технологии: Python, aiogram, PostgreSQL

