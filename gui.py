import sql_functions
from tkinter import *
import sys
# TODO comment everything

class Window:
    def __init__(self, name_window="Untitled", *args, **kwargs):
        self.root = Tk()
        self.root.title(name_window)


class MainWindowVariables:
    def __init__(self):
        self.name_database = None
        self.name_table = None
        self.data_format = None
        self.input_window = None
        self.input_window_name = None
        self.file_name = None
        self.pady = 1


class MainWindow(Window):
    def __init__(self, name_window, *args, **kwargs):
        super().__init__(name_window, *args, **kwargs)

        self.root.geometry('500x310')
        self.root.resizable(False, False)

        self.variables = MainWindowVariables()
        # TODO move widgets to separate function
        self.message = StringVar()
        self.message_label = Label(textvariable=self.message)
        self.message_label.pack(pady=self.variables.pady)

        self.dbname_entry_label = Label(text='Введите название базы данных')
        self.dbname_entry_label.pack(pady=self.variables.pady)
        self.dbname_entry = Entry(self.root, textvariable=self.variables.name_database)
        self.dbname_entry.pack(pady=self.variables.pady)
        self.dbname_button = Button(text='Записать значение', command=self.get_dbname)
        self.dbname_button.pack(pady=self.variables.pady)

        self.tname_entry_label = Label(text='Введите название таблицы')
        self.tname_entry_label.pack(pady=self.variables.pady)
        self.tname_entry = Entry(self.root, textvariable=self.variables.name_table)
        self.tname_entry.pack(pady=self.variables.pady)
        self.tname_button = Button(text='Записать значение', command=self.get_name_table)
        self.tname_button.pack(pady=self.variables.pady)

        self.create_database_button = Button(text='Создать базу данных', command=self.create_database)
        self.create_database_button.pack(pady=self.variables.pady)

        self.create_table_button = Button(text='Создать таблицу', command=self.create_table)
        self.create_table_button.pack(pady=self.variables.pady)

        self.open_input_window_button = Button(text='Ввести данные в таблицу', command=self.open_input_window)
        self.open_input_window_button.pack(pady=self.variables.pady)

        self.export_button = Button(text='Экспортировать данные в Excel', command=self.export)
        self.export_button.pack(pady=self.variables.pady)

        self.button_close_window = Button(text='Закрыть окно', command=sys.exit)
        self.button_close_window.pack(side='bottom', pady=self.variables.pady)

    def get_dbname(self):
        self.variables.name_database = self.dbname_entry.get()
        self.message.set('Название базы данных внесено')
        return 0

    def create_database(self):
        sql_functions.create_db(self.variables.name_database)
        self.message.set('База данных создана')
        # TODO error handling
        return 0

    def get_name_table(self):
        self.variables.name_table = self.tname_entry.get()
        self.message.set('Название таблицы внесено')
        return 0

    def create_table(self):
        sql_functions.simple_create_table(self.variables.name_database,
                                          self.variables.name_table,
                                          self.variables.data_format)
        # TODO error handling
        self.message.set('Таблица создана')
        return 0

    def open_input_window(self):
        self.variables.input_window = InputWindow(self.variables.input_window_name)
        self.clone_values()
        self.variables.input_window.initialize_buttons()
        return 0

    def clone_values(self):
        self.variables.input_window.variables.data_format = self.variables.data_format
        self.variables.input_window.variables.name_database = self.variables.name_database
        self.variables.input_window.variables.name_table = self.variables.name_table
        self.variables.input_window.variables.pady = self.variables.pady
        return 0

    def export(self):
        sql_functions.excel_export_single(self.variables.name_database,
                                          self.variables.name_table,
                                          self.variables.file_name)
        # TODO message label, error handling
        return 0


class InputWindow(Window):
    def __init__(self, name_window, *args, **kwargs):
        super().__init__(name_window, *args, **kwargs)

        self.root.geometry('500x300')

        self.variables = InputWindowVariables()

        self.message_input_window = StringVar()
        self.message_input_window.set('sfhgb')
        self.message_label = Label(self.root, textvariable=self.message_input_window)
        self.message_label.pack(pady=self.variables.pady)

        self.labels = []
        self.entries = []
        self.entry_variables = dict()

        self.get_values_button = (Button(self.root,
                                         text='Ввести данные и отправить в таблицу',
                                         command=self.get_values).pack(side='bottom',
                                                                       pady=self.variables.pady))

    def initialize_buttons(self):
        for column in self.variables.data_format:
            label = Label(self.root, text=column[2])
            label.pack()
            entry = Entry(self.root)
            entry.pack()
            self.labels.append(None)
            self.labels[-1] = label
            self.entries.append(0)
            self.entries[-1] = entry
            self.entry_variables[column[0]] = 0
        return 0

    def get_values(self):
        for index, OBJECT in enumerate(self.entries):
            self.entry_variables[self.variables.data_format[index][0]] = OBJECT.get()
        values = [tuple(map(lambda x: x[1], self.entry_variables.items())), ]
        sql_functions.sql_input(self.variables.name_database,
                                self.variables.name_table,
                                self.variables.data_format,
                                values)
        self.message_input_window.set('Данные успешно внесены')
        # TODO pass a func object into this method to process data and update table
        return 0


class InputWindowVariables:
    def __init__(self):
        self.name_database = None
        self.name_table = None
        self.data_format = None
        self.pady = None

# TODO exception handling
if __name__ == '__main__':
    pass
