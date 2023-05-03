from queue import LifoQueue


def algorith(row):
    stack = LifoQueue(maxsize=500)
    list1 = list(map(int, row['Stacks'].split(' ')))
    list2 = []
    for value in list1:
        stack.put(value)
    resstack = str(list1)
    row['Stacks'] = resstack
    for k in range(3): #Должно быть 100, но чтобы прога не ломалась пока 3
        list2.append(stack.get())
    itstr = str(list2)
    row['Removed_items'] = itstr
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 32)")
    current_window.children.input_window_name = 'Ввод данных для задачи 32'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Stacks', 'TEXT', 'Введите стек через пробел'),
        ('Removed_items', 'TEXT', 0)
    ]
