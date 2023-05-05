import tkinter


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


def window1(x):
    root = tkinter.Tk()
    root.geometry("300x200")

    def on_closing():
        root.destroy()

    root.title("Вывод результата задачи")
    label = tkinter.Label(root, text=x)
    label.pack()
    exit_button = tkinter.Button(root, text="Exit", command=on_closing)
    exit_button.pack(pady=20)


def algorith(row):
    stack1 = Stack()
    list1 = list(map(str, row['Stacks'].split(' ')))
    list2 = []
    if len(list1) > 1:
        for value in list1:
            stack1.push(value)
        resstack = str(list1)
        row['Stacks'] = resstack
        for k in range(3):
            list2.append(stack1.pop())
        itstr = str(list2)
        row['Removed_items'] = itstr

        window1(itstr)
    else:
        window1('Результата нет')
        row["Stacks"] = 'Пустой ввод'
        row['Removed_items'] = 'Результата нет'
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 31)")
    current_window.children.input_window_name = 'Ввод данных для задачи 31'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Stacks', 'TEXT', 'Введите стек через пробел'),
        ('Removed_items', 'TEXT', 0)
    ]
