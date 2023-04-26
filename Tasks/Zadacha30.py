from queue import LifoQueue


def algorith(row):
    stack = LifoQueue(maxsize=500)
    list1 = list(map(int, row['Stacks'].split(' ')))
    for value in list1:
        stack.put(value)
    row['Stacks'] = str(list1)
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 30)")
    current_window.children.input_window_name = 'Ввод данных для задачи 30'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Stacks', 'TEXT', 'Введите стек через пробел')
    ]
