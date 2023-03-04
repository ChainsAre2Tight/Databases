import pymysql.cursors
import pandas.io.sql
import warnings
from tabulate import tabulate


class CustomError(Exception):
    """Base custom exception class"""
    pass


class OtherError(CustomError):
    """Base custom exception class for regular errors"""

    def __str__(self):
        return self.args


class FunctionError(CustomError):
    """
    Exception class for all exceptions raised in this module

    action -- attribute, that indicates which function raised its appropriate exception
    """
    action = 'do stuff'
    default_exception = Exception()

    def __init__(self, error=default_exception):
        """
        param error -- stores error object as variable for easy access
        """
        self.error = error
        super().__init__(self.error)

    def __str__(self) -> str:
        """
        returns formatted string containing information about source of trouble and some information about it
        """
        return f'Error while trying to {self.action} ({str(self.error.__class__)[8:-2]}: {self.error.args[1]})'


class DatabaseCreationError(FunctionError):
    """Exception raised in create_db function of this module"""
    action = 'create database'


class TableCreationError(FunctionError):
    """Exception raised in create_table function of this module"""
    action = 'create table'


class DatabaseDeletionError(FunctionError):
    """Exception raised in delete_db function of this module"""
    action = 'delete database'


class TableDeletionError(FunctionError):
    """Exception raised in delete_table function of this module"""
    action = 'delete table'


class SqlInputError(FunctionError):
    """Exception raised in sql_input function of this module"""
    action = 'input values to table'


class SqlOutputError(FunctionError):
    """Exception raised in sql_output function of this module"""
    action = 'output values from table'


class SqlExportError(FunctionError):
    """Exception raised in excel_export_single function of this module"""
    action = 'export values to Excel'


class CustomInquiryError(FunctionError):
    """Exception raised in both local_custom_inquiry and global_custom_inquiry function of this module"""
    action = 'execute custom inquiry'


class GetDatabasesError(FunctionError):
    """Exception raised in get_list_of_databases function of this module"""
    action = 'get list of databases'


class GetTablesError(FunctionError):
    """Exception raised in get_list_of_tables function of this module"""
    action = 'get list of tables'


class ColumnNumberError(CustomError):
    """
    Custom exception that was raised in sql_input function, but currently is unused
    """

    def __init__(self, columns, expected_columns, row):
        self.columns = columns
        self.expected_columns = expected_columns
        self.row = row + 1
        super().__init__(self.columns, self.expected_columns, self.row)
        self.args = (1,
                     f'Your # of columns in row №{self.row} doesnt match expected # of columns ({self.columns}, '
                     f'expected: {self.expected_columns})')


class MissingAttributeError(CustomError):
    """
    Exception that is raised when some important attribute is not passed to some function
    """

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
    """
    Exception that is raised by excel_export_single function when selected name is inappropriate for Windows file system
    """

    def __init__(self):
        self.args = (1, r'Your filename contains special symbols (\ | / : * ? " < >)')


class InappropriateNameError(CustomError):
    """
    Exception raised by various function when inputted string is inappropriate for use in MySQL
    """

    def __init__(self):
        self.args = (1, 'Inappropriate name')


def check_filename(name: str) -> bool:
    """Check if the given string is suitable for a filename"""

    for i in r'\|/:*?"<>':
        if i in name:
            return False
    return True


def check_database_name(name: str, blacklist='''!@#$%^&*()=;/,.'"\n\t''') -> bool:
    """
    This function checks if inputted string contains any of the blacklisted characters
    :param name:  what string to check
    :returns True if no blacklisted characters are found, otherwise False

    :param blacklist: string, containing blacklisted characters
    """
    if name != '' and str(name) != 'none':
        for symbol in blacklist:
            if symbol in str(name):
                return False
        return True
    return False


def get_err_msg(er: object) -> tuple:
    """
    Simple function that
    :returns .args of given Exception object
    """
    return er.error.args


def local_custom_inquiry(database_name: str, inquiry: str, password: str = 'root') -> tuple:
    """
    Function that simply executes given SQL query in selected database
    :param database_name: defines what database to use
    :param inquiry: SQL statement
    :param password: server password
    :returns: tuple if SELECT statement is inputted
    :raises CustomInquiryError
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = inquiry
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return cursor.fetchall()
    except Exception as er:
        raise CustomInquiryError(er)


def global_custom_inquiry(inquiry: str, password: str = 'root') -> tuple:
    """
    Function that simply executes given SQL query
    :param inquiry: -- SQL statement
    :param password: -- server password
    :returns: tuple if SELECT statement is inputted
    :raises CustomInquiryError
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = inquiry
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return cursor.fetchall()
    except Exception as er:
        raise CustomInquiryError(er)


# noinspection PyTypeChecker
def get_list_of_databases(hide_defaults=False, password: str = 'root') -> list:
    """
    This function returns list of all databases on chosen server, can hide system ones
    :param hide_defaults: -- set to True if you want to hide system databases
    :param password: -- password
    :returns: list of all databases on chosen server
    :raises GetTablesError
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = 'SHOW DATABASES'
        cursor.execute(sql)
        connection.commit()
        connection.close()
        tables = cursor.fetchall()
        defaults = ('sys', 'performance_schema', 'mysql', 'information_schema')
        if not hide_defaults:
            defaults = []
        list_of_tables = [i['Database'] for i in tables if i['Database'] not in defaults]

        return list_of_tables
    except Exception as er:
        raise GetTablesError(er)


# noinspection PyTypeChecker
def get_list_of_tables(database_name: str, password: str = 'root') -> list:
    """
    This function returns list of all tables in chosen database
    :param database_name: defines database
    :param password: password
    :return: list of all tables in chosen database
    :raise GetTablesError
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = 'SHOW TABLES'
        cursor.execute(sql)
        connection.commit()
        connection.close()
        dbs = cursor.fetchall()
        list_of_databases = [i[f'Tables_in_{database_name}'] for i in dbs if i[f'Tables_in_{database_name}']]
        return list_of_databases
    except Exception as er:
        raise GetTablesError(er)


def create_db(database_name: str, password: str = 'root') -> None:
    """
    This function creates database if it's name passes check
    :param database_name: name of database
    :param password: password
    :raises DatabaseCreationError
    """
    try:
        if not check_database_name(database_name):
            raise InappropriateNameError
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
        return
    except Exception as er:
        raise DatabaseCreationError(er)


def delete_db(database_name: str, password: str = 'root') -> None:
    """
    This function deletes chosen database
    :param database_name: name of database staged for deletion
    :param password: password
    :raises DatabaseDeletionError
    """
    try:
        if not check_database_name(database_name):
            raise InappropriateNameError
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = f'DROP DATABASE {database_name}'
        cursor.execute(sql)
        connection.close()
        return
    except Exception as er:
        raise DatabaseDeletionError(er)


def simple_create_table(database_name: str, table_name: str, table_format: list, auto_increment_column_name=None,
                        password: str = 'root') -> None:
    """
    This function creates a table following table_format pattern
    :param database_name: name of selected database
    :param table_name: name of created stable
    :param table_format: list of tuples, that dictates format of created table. This variable should be as follows:
            [('var1', 'INT'), ('var2', 'VARCHAR(123)'), ('var3', 'TEXT(149)'), ...]
    :param auto_increment_column_name: if inputted, creates PRIMARY KEY AUTO_INCREMENT column with this name
    :param password: password
    :raise TableCreationError
    """
    try:
        if not check_database_name(database_name) or not check_database_name(table_name):
            raise InappropriateNameError
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=password,
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        if table_format:
            cursor = connection.cursor()
            if auto_increment_column_name:
                table_format.insert(0, (auto_increment_column_name, 'INT PRIMARY KEY AUTO_INCREMENT'))
            sql_gen = ', '.join([' '.join(table_format[i][:2]) for i in range(len(table_format))])
            sql = f'CREATE TABLE {table_name} ({sql_gen})'
            cursor.execute(sql)
            connection.commit()
            connection.close()
        else:
            raise MissingAttributeError('table_format')
        return
    except Exception as er:
        raise TableCreationError(er)


def delete_table(database_name: str, table_name: str, password: str = 'root') -> None:
    """
    This function deletes selected table
    :param database_name: determines from what database to delete table from
    :param table_name: determines what table to delete
    :param password: password
    :raises TableDeletionError
    """
    try:
        if not check_database_name(database_name) or not check_database_name(table_name):
            raise InappropriateNameError
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
        return
    except Exception as er:
        raise TableDeletionError(er)


def sql_input(database_name: str, table_name: str, table_format: str, values_list: list,
              password: str = 'root') -> None:
    """
    Inserts rows into table
    :param database_name: determines what database to use
    :param table_name: determines what table to insert values into
    :param table_format: data format, see simple_create_table for more info
    :param values_list: list of tuples, each tuple is a separate row [(value1, value2, ...), (value1, value2, ...)]
    :param password: password
    :raises SqlInputError
    """
    try:
        if not check_database_name(database_name) or not check_database_name(table_name):
            raise InappropriateNameError
        connection = pymysql.connect(host='localhost',
                                     password=password,
                                     user='root',
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        if table_format and values_list:
            sql_gen = ', '.join([table_format[i][0] for i in range(len(table_format))])
            val_gen = ('%s, ' * len(table_format))[:-2]
            sql = f'''INSERT INTO {table_name} ({sql_gen}) VALUES ({val_gen})'''
            for row in values_list:
                cursor.execute(sql, row)
                connection.commit()
            connection.close()
        elif not table_format:
            raise MissingAttributeError('table_format')
        elif not values_list:
            raise MissingAttributeError('Values_list')
        return

    except Exception as er:
        raise SqlInputError(er)


def sql_output(database_name: str, table_name: str, where_statement: str = None, password: str = 'root') -> tuple:
    """
    This function returns all rows from selected table, supports custom WHERE statements
    :param database_name: determines what database to use
    :param table_name: determines what table to use
    :param where_statement: if inputted, acts as WHERE statement
    :param password: password
    :return: list of dictionaries of all rows that are selected
    :raises SqlOutputError
    """
    try:
        if not check_database_name(database_name) or not check_database_name(table_name):
            raise InappropriateNameError
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
        return result
    except Exception as er:
        raise SqlOutputError(er)


def excel_export_single(database_name: str, table_name: str, file_name: str, where_statement: str = False,
                        password: str = 'root'):
    """
    This function creates a new .xlsx file from selected table, supports WHERE statement
    :param database_name: determines what database to use
    :param table_name: determines what table to export
    :param file_name: determines file name
    :param where_statement: adds a WHERE clause to query
    :param password: password
    :raises SqlExportError
    """
    try:
        if not check_database_name(database_name) or not check_database_name(table_name):
            raise InappropriateNameError
        connection = pymysql.connect(host='localhost',
                                     password=password,
                                     user='root',
                                     db=database_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        sql = f"SELECT * from {table_name}" + f' WHERE {where_statement}' * (1 if where_statement else 0)
        if not file_name:
            raise MissingAttributeError('file_name')
        elif not file_name.find(':\\') and not check_filename(file_name):
            raise InappropriateFilenameError
        else:
            warnings.simplefilter('ignore')
            truck = pandas.io.sql.read_sql(sql, connection)
            if file_name[-5:] != '.xlsx':
                file_name = file_name + '.xlsx'
            truck.to_excel(file_name)
        connection.close()
        return
    except Exception as er:
        raise SqlExportError(er)


def get_columns(database_name: str, table_name: str, password: str = 'root') -> list:
    """
    This function returns list off all column names of a table
    :param database_name: determines what database to use
    :param table_name: determines what table to use
    :param password: password
    :return: list of column names
    """
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


def formatted_print(rows: tuple) -> str:
    """
    This function receives list of rows and returns tabulated string for printing
    :param rows: list of dictionaries, primarily from sql_output function of this module
    :return: tabulated text
    """
    headers = list(rows[0].keys())
    medallist = []
    for i in rows:
        val = list(i.values())
        medallist.append(val)
    tabulated_rows = tabulate(medallist, headers=headers)
    return tabulated_rows


if __name__ == '__main__':
    pass
