import pymysql.cursors
import pandas.io.sql
import warnings
from tabulate import tabulate


class CustomError(Exception):
    pass


class OtherError(CustomError):
    def __str__(self):
        return self.args


class FunctionError(CustomError):
    # Custom exception to show in which function there was an error
    action = 'do stuff'
    default_exception = Exception()

    def __init__(self, error=default_exception):
        self.error = error
        super().__init__(self.error)

    def __str__(self):
        return f'Error while trying to {self.action} ({str(self.error.__class__)[8:-2]}: {self.error.args[1]})'


class DatabaseCreationError(FunctionError):
    action = 'create database'


class TableCreationError(FunctionError):
    action = 'create table'


class DatabaseDeletionError(FunctionError):
    action = 'delete database'


class TableDeletionError(FunctionError):
    action = 'delete table'


class SqlInputError(FunctionError):
    action = 'input values to table'


class SqlOutputError(FunctionError):
    action = 'output values from table'


class SqlExportError(FunctionError):
    action = 'export values to Excel'


class ColumnNumberError(CustomError):
    def __init__(self, columns, expected_columns, row):
        self.columns = columns
        self.expected_columns = expected_columns
        self.row = row + 1
        super().__init__(self.columns, self.expected_columns, self.row)
        self.args = (1,
                     f'Your # of columns in row №{self.row} doesnt match expected # of columns ({self.columns}, '
                     f'expected: {self.expected_columns})')


class MissingAttributeError(CustomError):
    def __init__(self, missing_attribute_name):
        if missing_attribute_name == 'table_format':
            error_id = 1
        elif missing_attribute_name == 'values_list':
            error_id = 2
        elif missing_attribute_name == 'file_name':
            error_id = 3
        else:
            error_id = -1
        self.args = (error_id, f'{missing_attribute_name} required as argument')


class InappropriateFilenameError(CustomError):
    def __init__(self):
        self.args = (1, r'Your filename contains special symbols (\ | / : * ? " < >)')


def check_filename(name):
    """Check if the given string is suitable for a filename"""

    for i in r'\|/:*?"<>':
        if i in name:
            return False
    return True


def create_db(database_name, password='root'):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = f'CREATE DATABASE {database_name}'
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return 0
    except Exception as er:
        raise DatabaseCreationError(er)


def delete_db(database_name, password='root'):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = f'DROP DATABASE {database_name}'
        cursor.execute(sql)
        connection.close()
        return 1
    except Exception as er:
        raise DatabaseDeletionError(er)


def create_table(database_name, table_name, table_format=None, password='root'):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        # TableFormat => '[('var1', 'INT'), ('var2', 'VARCHAR(123)'), ('var3', 'TEXT(149)'), ...]

        if table_format:
            cursor = connection.cursor()
            sql_gen = ', '.join([' '.join(table_format[i]) for i in range(len(table_format))])
            sql = f'CREATE TABLE {table_name} ({sql_gen})'
            cursor.execute(sql)
            connection.commit()
            connection.close()
        else:
            raise MissingAttributeError('table_format')

        return 1
    except Exception as er:
        raise TableCreationError(er)


def delete_table(database_name, table_name, password='root'):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()
        sql = f'DROP TABLE {table_name}'
        cursor.execute(sql)
        connection.commit()
        connection.close()

        return 1
    except Exception as er:
        raise TableDeletionError(er)


def sql_input(database_name, table_name, table_format=None, values_list=None, password='root'):
    try:
        connection = pymysql.connect(host='localhost',
                                     password=password,
                                     user='root',
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()

        if table_format and values_list:

            # Generates sql statement from table_format and values_list
            sql_gen = ', '.join([table_format[i][0] for i in range(len(table_format))])
            val_gen = ('%s, ' * len(table_format))[:-2]
            sql = f'''INSERT INTO {table_name} ({sql_gen}) VALUES ({val_gen})'''
            for i in range(len(values_list)):
                if table_format and values_list and len(values_list[i]) != len(table_format):
                    # if inputted # of columns doesn't match the specified in table_format
                    raise ColumnNumberError(len(values_list[i]), len(table_format), i)

                cursor.execute(sql, values_list[i])
                connection.commit()
            connection.close()

        elif not table_format:
            raise MissingAttributeError('table_format')
        elif not values_list:
            raise MissingAttributeError('Values_list')

        return 1

    except Exception as er:
        raise SqlInputError(er)


def sql_output(database_name, table_name, where_statement=False, password='root'):
    try:
        connection = pymysql.connect(host='localhost',
                                     password=password,
                                     user='root',
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = f"SELECT * from {table_name}" + f' WHERE {where_statement}' * (1 if where_statement else 0)
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()

        # returns data from the table
        return result
    except Exception as er:
        raise SqlOutputError(er)


def excel_export_single(database_name, table_name, file_name, where_statement=False, password='root'):
    try:
        connection = pymysql.connect(host='localhost',
                                     password=password,
                                     user='root',
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        sql = f"SELECT * from {table_name}" + f' WHERE {where_statement}' * (1 if where_statement else 0)
        if not file_name:
            raise MissingAttributeError('file_name')
        elif not check_filename(file_name):
            raise InappropriateFilenameError
        else:
            warnings.simplefilter('ignore')
            truck = pandas.io.sql.read_sql(sql, connection)
            truck.to_excel(file_name + '.xlsx')
        connection.close()

        return 1
    except Exception as er:
        raise SqlExportError(er)


def get_columns(database_name, table_name, password='root'):
    connection = pymysql.connect(host='localhost',
                                 password=password,
                                 user='root',
                                 db=database_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = f'SHOW COLUMNS FROM {table_name}'
        cursor.execute(sql)
        columns = list(map(lambda x: (x['Field'], x['Type']), cursor.fetchall()))
        connection.close()
    return columns


def get_increment(database_name, table_name, column_name, password='root'):
    connection = pymysql.connect(host='localhost',
                                 password=password,
                                 user='root',
                                 db=database_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = f'select {table_name}.{column_name} from {table_name} order by {column_name} desc limit 1'
        cursor.execute(sql)
        result = cursor.fetchall()[0][column_name]
        connection.close()
        return result


def formated_print(rows):
    headers = list(rows[0].keys())
    megalist = []
    for i in rows:
        val = list(i.values())
        megalist.append(val)
    print(tabulate(megalist, headers=headers))


if __name__ == '__main__':
    Table_format = [('input', 'INT'), ('result', 'INT')]
    Values = [(11, 12), (13, 14)]
    dn = 'test'
    tn = 'test1'
    try:
        pass
        # create_db(dn)
        # create_table(dn, tn, Table_format)
        # sql_input(dn, tn, Table_format, Values)
        # print(sql_output(dn, tn))
        # excel_export(dn, tn, 'absolutest')

    finally:
        pass
        # delete_table(dn, tn)
        # delete_db(dn)
