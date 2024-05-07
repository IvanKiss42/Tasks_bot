import psycopg2
from config import db_name, user, password, host, port


class DatBase:

    def __init__(self):
        self.connection = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def create_tasks_table(self):
        """Создание таблицы задач если не существует."""
        with self.connection:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS tasks (description TEXT)"
            )
            self.connection.commit()

    def add_task(self, data):
        """Добавление задачи."""
        with self.connection:
            self.cursor.execute(
                'INSERT INTO tasks (description) VALUES (%s)', (data,)
            )
            self.connection.commit()

    def list_tasks(self):
        """Вывод списка задач."""
        with self.connection:
            self.cursor.execute(
                "SELECT * FROM tasks;"
            )
            self.connection.commit()
            return self.cursor.fetchall()

    def check_task(self, description):
        """Проверка наличия задачи."""
        with self.connection:
            self.cursor.execute(
                "SELECT * FROM tasks WHERE description = %s", (description,)
            )
            self.connection.commit()
            return bool(self.cursor.fetchall())

    def remove_task(self, description):
        """Удаление задачи."""
        with self.connection:
            self.cursor.execute(
                "DELETE FROM tasks WHERE description = %s", (description,)
            )
            self.connection.commit()
