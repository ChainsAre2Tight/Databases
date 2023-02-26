import numpy as np


class MATRIX:
    def __init__(self, info):
        self.rows = info[0]
        self.columns = info[1]
        self.values = iter(info[2:])

    def create(self):
        name = []
        for x in range(0, self.rows):
            name.append([i for i in range(self.columns)])
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                name[x][y] = next(self.values)
        return name


def algorith(row):
    matr1 = np.array(MATRIX.create(MATRIX(list(map(int, row['M1'].split(' '))))))
    matr2 = np.array(MATRIX.create(MATRIX(list(map(int, row['M2'].split(' '))))))
    row['M3'] = matr1.dot(matr2)
    row['M1'] = matr1
    row['M2'] = matr2
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 19)")
    current_window.children.input_window_name = 'Ввод данных для задачи 19'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('M1', 'VARCHAR(100)', 'Введите размеры первой матрицы и значения матрицы через пробел'),
        ('M2', 'VARCHAR(100)', 'Введите размеры второй матрицы и значения матрицы через пробел'),
        ('M3', 'VARCHAR(100)', 0)]
