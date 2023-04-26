from queue import LifoQueue
'''29 задача через список надо,
30 задача через коллекцию
'''

def algorith(row):
    stack = LifoQueue(maxsize=500)
    list1 = list(map(int, row['Stacks'].split(' ')))
    for value in list1:
        stack.put(value)
    row['Stacks'] = str(list1)
    return row


class Stack:
    def __init__(self):
        self.stack = []
        self.__max = None

    def empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

    def pop(self):
        if len(self.stack) == 0:
            return None
        removed = self.stack.pop()
        if len(self.stack) == 0:
            self.__max = 0
        elif removed == self.__max:
            self.__max = self.stack[0]
            for value in self.stack:
                if value > self.__max:
                    self.__max = value
        return removed

    def max(self):
        return self.__max

    def push(self, item):
        self.stack.append(item)
        if len(self.stack) == 1 or item > self.__max:
            self.__max = item


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 29)")
    current_window.children.input_window_name = 'Ввод данных для задачи 29'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Stacks', 'TEXT', 'Введите стек через пробел')
    ]
