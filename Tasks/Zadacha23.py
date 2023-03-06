def algorith(row):
    try:
        a = list(map(int, row['Massive'].split(' ')))
        mas_even = []
        for k in range(len(a)):
            if (lambda x: x % 2 == 0)(a[k]):
                mas_even.append(k)
        row['Indexes'] = str(mas_even)
    except (ValueError, RuntimeError):
        row['Massive'] = 'Bad input'
        row['Indexes'] = 'No result'
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 23)")
    current_window.children.input_window_name = 'Ввод данных для задачи 23'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Massive', 'TEXT', 'Введите список'),
        ('Indexes', 'TEXT', 0),
    ]
