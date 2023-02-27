def algorith(row):
    flag = False
    try:
        fb = float(row['First_Base'])
    except ValueError:
        row['First_Base'] = 'Bad input'
        flag = True
    try:
        sb = float(row['Second_Base'])
    except ValueError:
        row['Second_Base'] = 'Bad input'
        flag = True
    try:
        hg = float(row['Height'])
    except ValueError:
        row['Height'] = 'Bad input'
        flag = True
    if not flag:
        try:
            sq = lambda fb, sb, hg: float((fb + sb) * hg / 2)
            row['Square'] = sq(fb, sb, hg)
        except ValueError:
            row['Square'] = 'No result'
    else:
        row['Square'] = 'No result'
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 21)")
    current_window.children.input_window_name = 'Ввод данных для задачи 21'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('First_Base', 'VARCHAR(100)', 'Введите первое основание'),
        ('Second_Base', 'VARCHAR(100)', 'Введите второе основание'),
        ('Height', 'VARCHAR(100)', 'Введите высоту'),
        ('Square', 'VARCHAR(100)', 0)]
