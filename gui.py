import sql_functions
from tkinter import *
import sys


class Window:
    def __init__(self, name_window="Untitled", *args, **kwargs):
        self.root = Tk()
        self.root.title(name_window)


class Main:
    def __init__(self):
        self.name_database = None
        self.name_table = None
        self.table_format = None
        self.input_window_class_name = None
        self.input_window = None
        self.input_window_name = None
        self.file_name = None


class MainWindow(Window):
    def __init__(self, name_window, *args, **kwargs):
        super().__init__(name_window, *args, kwargs)

        self.root.geometry('500x300')
        self.root.resizable(0, 0)

        self.variables = Main()
        self.variables.name_database = StringVar()

        self.dbname_entry_label = Label(text='Введите название базы данных')
        self.dbname_entry_label.pack()
        self.dbname_entry = Entry(self.root, textvariable=self.variables.name_database)
        self.dbname_entry.pack()
        self.dbname_button = Button(text='Записать значение', command=self.get_dbname)
        self.dbname_button.pack()

        self.tname_entry_label = Label(text='Введите название таблицы')
        self.tname_entry_label.pack()
        self.tname_entry = Entry(self.root, textvariable=self.variables.name_table)
        self.tname_entry.pack()
        self.tname_button = Button(text='Записать значение', command=self.get_tname)
        self.tname_button.pack()

        self.create_database_button = Button(text='Создать базу данных', command=self.create_database)
        self.create_database_button.pack()

        self.create_table_button = Button(text='Создать таблицу', command=self.create_table)
        self.create_table_button.pack()

        self.open_input_window_button = Button(text='Ввести данные в таблицу', command=self.open_input_window)
        self.open_input_window_button.pack()

        self.export_button = Button(text='Экспортировать данные в Excel', command=self.export)
        self.export_button.pack()

        self.button_close_window = Button(text='Закрыть окно', command=sys.exit)
        self.button_close_window.pack()

    def get_dbname(self):
        self.variables.name_database = self.dbname_entry.get()

    def create_database(self):
        sql_functions.create_db(self.variables.name_database)

    def get_tname(self):
        self.variables.name_database = self.tname_entry.get()

    def create_table(self):
        sql_functions.create_table(self.variables.name_database,
                                   self.variables.name_table,
                                   self.variables.table_format)

    def open_input_window(self):
        self.variables.input_window = eval(
            f"""{self.variables.input_window_class_name}('{self.variables.input_window_name}')""")

    def export(self):
        sql_functions.excel_export_single(self.variables.name_database,
                                          self.variables.name_table,
                                          self.variables.file_name)


class InputWindow(Window):
    def __init__(self, name_window, *args, **kwargs):
        super().__init__(name_window, *args, **kwargs)


if __name__ == '__main__':
    a = MainWindow("Приложение 'Базы данных'")
    a.variables.input_window_class_name = 'InputWindow'
    a.variables.input_window_name = 'hbjhfvbhf'

    a.root.mainloop()

