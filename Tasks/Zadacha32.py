from queue import LifoQueue
import tkinter


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
    stack = LifoQueue(maxsize=500)
    list1 = list(map(int, row['Stacks'].split(' ')))
    list2 = []
    if len(list1) > 0:
        for value in list1:
            stack.put(value)
        resstack = str(list1)
        row['Stacks'] = resstack
        for k in range(3):  # Должно быть 100, но чтобы прога не ломалась пока 3
            list2.append(stack.get())
        itstr = str(list2)
        row['Removed_items'] = itstr

        window1(itstr)

    else:
        row["Stacks"] = 'Пустой ввод'
        row['Removed_items'] = 'Результата нет'

    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 32)")
    current_window.children.input_window_name = 'Ввод данных для задачи 32'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Stacks', 'TEXT', 'Введите стек через пробел'),
        ('Removed_items', 'TEXT', 0)
    ]
