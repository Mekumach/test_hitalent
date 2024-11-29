import json
from datetime import datetime


class Task:
    # Задаем атрибуты для задачи
    def __init__(self, task_id: int, title: str, description: str, category: str,
                 due_date: str, priority: str, status: str = "Не выполнена"):
        self.id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    # Преобразование объекта класса в словарь, чтобы сохранить в формате JSON
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    # Представление задачи в строковом формате
    def __str__(self):
        return (
                f"ID: {self.id}\n"
                f"Название: {self.title}\n"
                f"Описание: {self.description}\n"
                f"Категория: {self.category}\n"
                f"Срок выполнения: {self.due_date}\n"
                f"Приоритет: {self.priority}\n"
                f"Статус: {self.status}\n"
        )

    # Статический метод для создания объекта задачи из словаря
    @staticmethod
    def from_dict(data: dict):
        return Task(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"],
        )


# Класс для управления задачами
class TaskManager:
    # Инициализирующий метод
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tasks = self.load_tasks()
        self.last_id = self.get_last_id()

    # Загрузка задач
    def load_tasks(self) -> list[Task]:
        with open(self.file_path, "r") as file:
            data = json.load(file)
            return [Task.from_dict(task) for task in data]

    # Сохранение задач в JSON-формате
    def save_tasks(self):
        with open(self.file_path, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    # Получение последнего ID задачи
    def get_last_id(self):
        if not self.tasks:
            return 0
        return max(task.id for task in self.tasks)

    # Добавление новой задачи
    def add_task(self, task: Task):
        self.last_id += 1
        task.id = self.last_id
        self.tasks.append(task)
        self.save_tasks()

    # Изменение существующей задачи
    def edit_task(self, task_id: int, **kwargs):
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError("Задача с этим ID не найдена")
        for key, value in kwargs.items():
            if value is not None:
                setattr(task, key, value)
        self.save_tasks()

    # Удаление задачи по id
    def delete_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    # Получение задачи по id
    def get_task_by_id(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    # Поиск задач по ключевому слову
    def search_tasks(self, keyword: str):
        return [
            task for task in self.tasks
            if (keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower())
            or keyword.lower() in task.status.lower()
        ]

    # Обновление статуса задач
    def update_task_status(self, task_id: int, new_status: str):
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError("Задача с указанным ID не найдена")
        if new_status not in ["Выполнена", "Не выполнена"]:
            raise ValueError("Статус должен быть либо 'Выполнена', либо 'Не выполнена'")
        task.status = new_status
        self.save_tasks()


# Проверка, чтобы поле не было пустым
def non_empty_input(prompt: str):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Вы должны что-нибудь ввести")


# Функция для получения приоритета с проверкой
def priority_input():
    while True:
        priority = input("Приоритет (Низкий/Средний/Высокий): ").strip()
        if priority in ["Низкий", "Средний", "Высокий"]:
            return priority
        print("Введите 'Низкий', 'Средний' или 'Высокий'")


# main функция, содержащая интерфейс программы
def main():
    # Создаем объект менеджера задач и загружаем задачи из файла
    manager = TaskManager("tasks.json")

    while True:
        print("\nМенеджер задач")
        print("1. Просмотр задач")
        print("2. Добавить задачу")
        print("3. Редактировать задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("6. Изменить статус задачи")
        print("7. Выход")
        number = input("Выберите действие: ")

        # Обрабатываем ответ каждого пункта из меню
        if number == "1":
            tasks = manager.tasks
            if not tasks:
                print("Список задач пуст")
            else:
                for task in tasks:
                    print(task)
        elif number == "2":
            title = non_empty_input("Название: ")
            description = non_empty_input("Описание: ")
            category = non_empty_input("Категория: ")

            while True:
                due_date = input("Дедлайн (YYYY-MM-DD): ")
                try:
                    input_date = datetime.strptime(due_date, "%Y-%m-%d")
                    if input_date <= datetime.now():
                        print("Дата должна быть больше текущей")
                    else:
                        break
                except ValueError:
                    print("Используйте формат YYYY-MM-DD")

            priority = priority_input()
            task = Task(0, title, description, category, due_date, priority)
            manager.add_task(task)
            print("Задача успешно добавлена!")
        elif number == "3":
            try:
                task_id = int(input("ID задачи для редактирования: "))
                task = manager.get_task_by_id(task_id)
                if not task:
                    print("Задача с таким ID не найдена")
                    continue

                title = input("Новое название (Enter для пропуска): ")
                description = input("Новое описание (Enter для пропуска): ")
                category = input("Новая категория (Enter для пропуска): ")
                due_date = input("Новый дедлайн (YYYY-MM-DD, Enter для пропуска): ")

                if due_date:
                    while True:
                        try:
                            input_date = datetime.strptime(due_date, "%Y-%m-%d")
                            if input_date <= datetime.now():
                                print("Дата должна быть больше текущей")
                                due_date = input("Новый дедлайн (YYYY-MM-DD, Enter для пропуска): ")
                            else:
                                break
                        except ValueError:
                            print("Некорректный формат даты")
                            due_date = input("Новый дедлайн (YYYY-MM-DD, Enter для пропуска): ")

                priority = input("Новый приоритет (Низкий/Средний/Высокий, Enter для пропуска): ")
                if priority:
                    while priority not in ["Низкий", "Средний", "Высокий"]:
                        print("Некорректный приоритет. Пожалуйста, выберите 'Низкий', 'Средний' или 'Высокий'.")
                        priority = input("Новый приоритет (Низкий/Средний/Высокий): ")

                manager.edit_task(
                    task_id,
                    title=title or None,
                    description=description or None,
                    category=category or None,
                    due_date=due_date or None,
                    priority=priority or None
                )
                print("Задача отредактирована!")
            except ValueError:
                print("Некорректный ввод ID")
        elif number == "4":
            try:
                task_id = int(input("ID задачи для удаления: ").strip())
                manager.delete_task(task_id)
                print("Задача удалена!")
            except ValueError:
                print("Некорректный ввод ID")
        elif number == "5":
            keyword = input("Ключевое слово: ").strip()
            tasks = manager.search_tasks(keyword=keyword)
            if not tasks:
                print("Подходящих задач не найдено")
            else:
                for task in tasks:
                    print(task)
        elif number == "6":
            try:
                task_id = int(input("ID задачи для изменения статуса: "))
                new_status = input("Новый статус (Выполнена/Не выполнена): ").strip()
                manager.update_task_status(task_id, new_status)
                print(f"Статус задачи с ID {task_id} был изменён")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif number == "7":
            print("Выход из программы")
            break
        else:
            print("Введите цифру из меню")


# Запуск программы
if __name__ == "__main__":
    main()
