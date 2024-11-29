from main import Task, TaskManager

# Путь к файлу с задачами
file_path = "tasks.json"


# Тест для добавления задачи
def test_add_task():
    manager = TaskManager(file_path)

    task = Task(0, "Тестовая задача", "Описание", "Работа", "2025-12-12", "Высокий")
    manager.add_task(task)

    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Тестовая задача"
    assert manager.tasks[0].status == "Не выполнена"

    with open(file_path, 'w') as file:
        file.write("[]")


# Тест для обновления статуса задачи
def test_update_task_status():
    manager = TaskManager(file_path)

    task = Task(0, "Тестовая задача", "Описание", "Работа", "2025-12-12", "Высокий")
    manager.add_task(task)

    manager.update_task_status(task.id, "Выполнена")

    assert manager.tasks[0].status == "Выполнена"

    with open(file_path, 'w') as file:
        file.write("[]")


# Тест для поиска задачи по ключевому слову
def test_search_tasks():
    manager = TaskManager(file_path)

    task1 = Task(0, "Тестовая задача 1", "Описание", "Работа", "2025-12-12", "Высокий")
    task2 = Task(0, "Тестовая задача 2", "Описание", "Учеба", "2025-12-12", "Низкий")
    manager.add_task(task1)
    manager.add_task(task2)

    found_tasks = manager.search_tasks("Тест")

    assert len(found_tasks) == 2
    assert found_tasks[0].title == "Тестовая задача 1"
    assert found_tasks[1].title == "Тестовая задача 2"

    # Ищем задачи по ключевому слову, которого нет в задачах
    found_tasks = manager.search_tasks("Билеберда")

    # Проверяем, что задачи не найдены
    assert len(found_tasks) == 0

    with open(file_path, 'w') as file:
        file.write("[]")


# Тест для удаления задачи
def test_delete_task():
    manager = TaskManager(file_path)

    task1 = Task(0, "Тестовая задача 1", "Описание", "Работа", "2025-12-12", "Высокий")
    task2 = Task(0, "Тестовая задача 2", "Описание", "Учеба", "2025-12-12", "Низкий")
    manager.add_task(task1)
    manager.add_task(task2)

    # Удаляем задачу с ID 1
    manager.delete_task(task1.id)

    # Проверяем, что задача удалена
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Тестовая задача 2"

    with open(file_path, 'w') as file:
        file.write("[]")
