import datetime


def algorith(row):
    current_day = datetime.datetime.now().date()
    try:
        od = list(map(int, row['DoB'].split(' ')))
        birth_date = datetime.date(od[2], od[1], od[1])
        delta = (current_day - birth_date).days
        row['AD'] = str(delta)
    except ValueError:
        row['DoB'] = 'Bad Input'
        row['AD'] = 'No result'
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 20)")
    current_window.children.input_window_name = 'Ввод данных для задачи 20'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('FIO', 'VARCHAR(100)', 'Введите фамилию, имя и отчество'),
        ('DoB', 'VARCHAR(50)', 'Введите дату рождения через пробел'),
        ('AD', 'VARCHAR(50)', 0)]
