def algorith(row):
    list_of_vowels = 'aoeyui'
    list_of_consonants = 'qwrtpsdfghjklzxcvbnm'
    sentence = row['Massive']
    cov = 0
    coc = 0
    for k in sentence:
        if k in list_of_vowels:
            cov +=1
        elif k in list_of_consonants:
            coc +=1
    First_20s = sentence[:20]
    Last_15s = sentence[-15:]
    row['Count_of_vowels'] = cov
    row['Count_of_constants'] = coc
    row['First_20'] = First_20s
    row['Last_15'] = Last_15s
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 24)")
    current_window.children.input_window_name = 'Ввод данных для задачи 24'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('Massive', 'TEXT', 'Введите список'),
        ('Count_of_vowels', 'INT', 0),
        ('Count_of_constants', 'INT', 0),
        ('First_20', 'TEXT', 0),
        ('Last_15', 'TEXT', 0)
    ]
