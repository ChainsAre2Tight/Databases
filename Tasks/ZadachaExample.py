def alg(row):
    """
    На ввод попадает словарь, представляющий из себя ряд таблицы
    Ключ - название столбца, задается в data_format

    В функции главной является строка следующего вида, которая ИЗМЕНЯЕТ данные во введенном словаре
    :return: тот же словарь в измененном виде
    """
    row['algnum'] = str(row['num']) + str(row['type'])
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (пример)")
    # устанавливаем название главного окна

    current_window.children.input_window_name = 'Ввод данных для ввода в таблицу'
    # устанавливаем название окна для ввода данных

    current_window.variables.algorithm = alg
    # можно не менять, передаем функцию для обработки данных

    # устанавливанем тип данных для программы
    current_window.variables.data_format = [('num', 'INT', 'Введите число'),
                                            # [('имя_столбца', 'тип_данных', 'Описание_поля_ввода')]
                                            # Если описание поля ввода 0 или False то поля ввода создано не будет
                                            ('type', 'VARCHAR(50)', 'Введеите строку'),
                                            ('numtype', 'VARCHAR(50)', 0)]


if __name__ == '__main__':
    pass