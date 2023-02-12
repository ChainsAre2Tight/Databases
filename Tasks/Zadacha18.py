import gui


def algorith(row):
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 18)")
    current_window.children.input_window_name = 'Ввод данных для задачи 18'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [('date_of_delivery', 'VARCHAR(50)', 'Введите дату ввоза'),
                                            ('department', 'VARCHAR(50)', 'Введите отдел'),
                                            ('type', 'VARCHAR(50)', 'Введите тип мебели'),
                                            ('price', 'VARCHAR(50)', 'Введите цену мебели')]


