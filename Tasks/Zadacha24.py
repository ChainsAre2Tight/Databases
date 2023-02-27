def sign(x):
    return x >= 0


def algorith(row):
    try:
        mas_all = list(map(int, row['Mas_A3'].split(' ')))
        mas_pos = []
        mas_neg = []
        for x in mas_all:
            if sign(x):
                mas_pos.append(x)
            else:
                mas_neg.append(x)
        row['Mas_A3'] = str(mas_all)[1:-1]
        row['Mas_pos'] = str(mas_pos)[1:-1]
        row['Mas_neg'] = str(mas_neg)[1:-1]
    except ValueError:
        row['Mas_A3'] = 'Bad input'
        row['Mas_pos'] = 'No result'
        row['Mas_neg'] = 'No result'
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 24)")
    current_window.children.input_window_name = 'Ввод данных для задачи 24'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Mas_A3', 'TEXT', 'Введите список'),
        ('Mas_even', 'TEXT', 0),
        ('Mas_odd', 'TEXT', 0)
    ]
