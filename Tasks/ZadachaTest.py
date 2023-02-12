def alg(row):
    row['algnum'] = str(row['num']) + str(row['type'])
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (тест)")
    current_window.children.input_window_name = 'Ввод данных для теста'
    current_window.variables.algorithm = alg
    current_window.variables.data_format = [('num', 'INT', 'enter num'),
                                            ('type', 'VARCHAR(50)', 'enter object type'),
                                            ('numtype', 'VARCHAR(50)', 0)]


if __name__ == '__main__':
    pass
