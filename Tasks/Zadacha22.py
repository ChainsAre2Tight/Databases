import math


def algorith(row):
    try:
        row['Degree'] = float(row['Degree'])
        row['Radians'] = float(math.radians(row['Degree']))
    except ValueError:
        row['Degree'] = 'Bad input'
        row['Radians'] = 'No result'
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 21)")
    current_window.children.input_window_name = 'Ввод данных для задачи 21'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Degree', 'DECIMAL(8,3)', 'Введите градусы'),
        ('Radians', 'DECIMAL(8,3)', 0),
    ]
