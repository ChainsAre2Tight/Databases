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


def algorith(row):
    stack1 = Stack()
    list1 = list(map(int, row['Stacks'].split(' ')))
    list2 = []
    for value in list1:
        stack1.push(value)
    row['Stacks'] = str(list1)
    for k in range(3):
        list2.append(stack1.pop())
    row['Removed_items'] = str(list2)
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 31)")
    current_window.children.input_window_name = 'Ввод данных для задачи 31'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Stacks', 'TEXT', 'Введите стек через пробел'),
        ('Removed_items', 'TEXT', 0)
    ]
