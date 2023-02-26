import numpy as np


class MATRIX:
    def __init__(self, info):
        self.rows = info[0]
        self.columns = info[1]
        self.values = info[2:]
        if len(self.values) > self.rows * self.columns:
            self.values = self.values[:self.rows*self.columns]
        elif len(self.values) < self.rows * self.columns:
            d = (len(self.values) - self.rows * self.columns) * -1
            for i in range(d):
                self.values.append(0)

    def convert(self):
        val = iter(self.values)
        list_of_values = []
        for x in range(0, self.rows):
            list_of_values.append([i for i in range(self.columns)])
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                list_of_values[x][y] = next(val)
        return list_of_values


def algorith(row):
    matrix1 = MATRIX(list(map(int, row['M1'].split(' '))))
    matr1 = np.array(matrix1.convert())
    matrix2 = MATRIX(list(map(int, row['M2'].split(' '))))
    matr2 = np.array(matrix2.convert())
    if matrix1.columns == matrix2.rows:
        row['M3'] = str(matr1.dot(matr2))[1:-1]
    else:
        row['M3'] = 'bad input'
    row['M1'] = str(matr1)[1:-1]
    row['M2'] = str(matr2)[1:-1]
    return row


def set_variables(current_window):
    current_window.root.title("Приложение 'Базы данных' (задача 19)")
    current_window.children.input_window_name = 'Ввод данных для задачи 19'
    current_window.variables.algorithm = algorith
    current_window.variables.data_format = [
        ('M1', 'VARCHAR(100)', 'Введите размеры первой матрицы и \n значения матрицы через пробел'),
        ('M2', 'VARCHAR(100)', 'Введите размеры второй матрицы и \n значения матрицы через пробел'),
        ('M3', 'VARCHAR(100)', 0)]
