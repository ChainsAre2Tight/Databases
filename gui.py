import sys
from tkinter import messagebox, ttk
from tkinter import filedialog
import os

import sql_functions
import config_reader
from tkinter import *

# TODO comment everything

def default_function(a):
    return a


def pass_function():
    pass


class Window:
    def __init__(self, name_window="Untitled", *args, **kwargs):
        self.root = Tk()
        self.root.title(name_window)


class MainWindowChildren:
    def __init__(self):
        self.input_window = None
        self.input_window_open = False
        self.output_window = None
        self.output_window_open = False


class MainWindowVariables:
    def __init__(self):
        self.name_preset = str()
        self.name_database = str()
        self.name_table = str()
        self.data_format = tuple()
        self.input_window_name = str()
        self.padx = 100
        self.pady = 1
        self.increment_column_name = 'id'
        self.algorithm = default_function
        self.list_of_databases = []
        self.list_of_tables = []


class MainWindowWidgets:
    def __init__(self):
        self.dbname_entry_label = None
        self.dbname_entry = None
        self.dbname_button = None
        self.tname_entry_label = None
        self.tname_entry = None
        self.tname_button = None
        self.create_database_button = None
        self.create_table_button = None
        self.open_input_window_button = None
        self.export_button = None
        self.button_close_window = None
        self.button_open_output_window = None
        self.dbname_entry_combobox = None
        self.tname_entry_combobox = None


# noinspection PyTypeChecker
class MainWindow(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.root.resizable(False, False)
        self.variables = MainWindowVariables()
        self.children = MainWindowChildren()
        self.widgets = MainWindowWidgets()
        self.initialize_widgets()
        self.config = config_reader.DatabaseConfig()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.menu = Menu(self.root, tearoff=0)
        self.root.config(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label='Выбрать задачу', menu=self.file_menu, underline=0)

        self.config_menu = Menu(self.menu)
        self.config_menu.add_command(command=self.add_to_config, label="Сохранить")
        self.config_menu.add_command(command=self.remove_from_config, label='Удалить')
        self.menu.add_cascade(label='Конфигурация', menu=self.config_menu, underline=0)

    def initialize_widgets(self):
        self.widgets.dbname_entry_label = Label(self.root, text='Введите название базы данных')
        self.widgets.dbname_entry_label.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.dbname_entry_combobox = ttk.Combobox(self.root, values=self.variables.list_of_databases)
        self.widgets.dbname_entry_combobox.pack(padx=self.variables.padx, pady=self.variables.pady)
        # self.widgets.dbname_entry = Entry(self.root, textvariable=self.variables.name_database)

        self.widgets.dbname_button = Button(self.root, text='Записать значение', command=self.get_dbname)
        self.widgets.dbname_button.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.tname_entry_label = Label(self.root, text='Введите название таблицы')
        self.widgets.tname_entry_label.pack(padx=self.variables.padx, pady=self.variables.pady)

        # self.widgets.tname_entry = Entry(self.root, textvariable=self.variables.name_table)
        self.widgets.tname_entry_combobox = ttk.Combobox(self.root, values=self.variables.list_of_databases)
        self.widgets.tname_entry_combobox.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.tname_button = Button(self.root, text='Записать значение', command=self.get_name_table)
        self.widgets.tname_button.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.create_database_button = Button(self.root, text='Создать базу данных',
                                                     command=self.create_database)
        self.widgets.create_database_button.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.create_table_button = Button(self.root, text='Создать таблицу', command=self.create_table)
        self.widgets.create_table_button.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.open_input_window_button = Button(self.root, text='Ввести данные в таблицу',
                                                       command=self.open_input_window)
        self.widgets.open_input_window_button.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.export_button = Button(self.root, text='Экспортировать данные в Excel',
                                            command=self.export_current_table)
        self.widgets.export_button.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.button_open_output_window = Button(self.root, text='Открыть окно вывода',
                                                        command=self.open_output_window)
        self.widgets.button_open_output_window.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.widgets.button_close_window = Button(self.root, text='Закрыть окно', command=self.on_closing)
        self.widgets.button_close_window.pack(padx=self.variables.padx, side='bottom', pady=self.variables.pady)

    def update_comboboxes(self):
        schema = self.config.read()
        try:
            self.variables.list_of_databases = list(schema[self.variables.name_preset].keys())
            if self.variables.name_database != '':
                self.variables.list_of_tables = schema[self.variables.name_preset][self.variables.name_database]
            self.widgets.dbname_entry_combobox['values'] = self.variables.list_of_databases
            self.widgets.tname_entry_combobox['values'] = self.variables.list_of_tables
        except KeyError:
            pass


    def get_dbname(self):
        self.variables.name_database = self.widgets.dbname_entry_combobox.get()
        self.update_comboboxes()
        messagebox.showinfo(message=f'''Название базы данных внесено
(Выбраная база данных: '{self.variables.name_database}')''')
        return

    def create_database(self):
        try:
            sql_functions.create_db(self.variables.name_database)
            list_of_databases = '\n'.join(sql_functions.get_list_of_databases(True))
            messagebox.showinfo(message=f'''База данных {self.variables.name_database} создана

Список всех баз данных:
{list_of_databases}''')
            return 0
        except Exception as er:
            if type(er) == sql_functions.DatabaseCreationError:
                messagebox.showinfo(message=f'Ошибка при создании базы данных: {sql_functions.get_err_msg(er)}')
                return
            else:
                messagebox.showinfo(message='Возникла неизвестная ошибка при создании базы данных')
                return

    def get_name_table(self):
        self.variables.name_table = self.widgets.tname_entry_combobox.get()
        messagebox.showinfo(message=f'''Название таблицы внесено
(Выбранная таблица: '{self.variables.name_table}')''')

        return

    def add_to_config(self):
        answer = messagebox.askokcancel("Сохранить", "Вы хотите сохранить текущую конфигурацию?")
        if answer:
            if '' not in [self.variables.name_database, self.variables.name_table, self.variables.name_preset]:

                if not self.config.check(self.variables.name_preset,
                                         self.variables.name_database,
                                         self.variables.name_table):
                    self.config.write(self.variables.name_preset,
                                      self.variables.name_database,
                                      self.variables.name_table)
                messagebox.showinfo('Оповещение', 'Конфигурация занесена')
                self.update_comboboxes()
            else:
                messagebox.showwarning('Оповещение', 'Нет конфигурации')

    def remove_from_config(self):
        answer = messagebox.askokcancel("Сохранить", "Вы хотите удалить текущую конфигурацию?")
        if answer:
            if '' not in [self.variables.name_database, self.variables.name_table, self.variables.name_preset]:
                self.config.delete(self.variables.name_preset,
                                   self.variables.name_database,
                                   self.variables.name_table)
                messagebox.showinfo('Оповещение', 'Конфигурация удалена')
                self.update_comboboxes()
            else:
                messagebox.showwarning('Оповещение', 'Нет конфигурации')

    def create_table(self):
        try:
            sql_functions.simple_create_table(self.variables.name_database,
                                              self.variables.name_table,
                                              list(self.variables.data_format),
                                              self.variables.increment_column_name)
            list_of_tables = '\n'.join(sql_functions.get_list_of_tables(self.variables.name_database))
            messagebox.showinfo(message=f'''Таблица создана

Список всех таблиц в базе данных '{self.variables.name_database}':
{list_of_tables}
''')
            return
        except Exception as er:
            if type(er) == sql_functions.TableCreationError:
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message=f'Возникла ошибка при создании таблицы: {sql_functions.get_err_msg(er)}')
                return
            else:
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message='Возникла неизвестная ошибка при создании таблицы')
                return

    def open_input_window(self):
        if self.variables.data_format == tuple():
            messagebox.showwarning(message='Не выбрана конфигурация')
        elif not self.children.input_window_open:
            self.children.input_window = InputWindow(self.variables.input_window_name)
            self.clone_values_to_input_window()
            self.children.input_window.initialize_buttons()
            self.children.input_window.root.protocol("WM_DELETE_WINDOW", self.on_closing_input_window)
            self.children.input_window_open = True
            self.root.withdraw()
            return

    def on_closing_input_window(self):
        self.children.input_window_open = False
        self.children.input_window.root.destroy()
        self.children.input_window = None
        self.root.deiconify()
        return

    def open_output_window(self):
        if not self.children.output_window_open:
            self.children.output_window = OutputWindow(self.variables.name_table)
            self.children.output_window.root.protocol("WM_DELETE_WINDOW", self.on_closing_output_window)
            self.clone_values_to_output_window()
            self.children.output_window_open = True
        else:
            self.clone_values_to_output_window()
            self.children.output_window.root.title(self.variables.name_table)
            self.children.output_window.root.lift()

    def on_closing_output_window(self):
        self.children.output_window_open = False
        self.children.output_window.root.destroy()
        self.children.output_window = None

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы точно хотите выйти?"):
            self.root.destroy()
            sys.exit()

    def clone_values_to_input_window(self):
        self.children.input_window.variables.data_format = self.variables.data_format
        self.children.input_window.variables.name_database = self.variables.name_database
        self.children.input_window.variables.name_table = self.variables.name_table
        self.children.input_window.variables.pady = self.variables.pady
        self.children.input_window.variables.padx = self.variables.padx
        self.children.input_window.variables.algorithm = self.variables.algorithm
        return

    def clone_values_to_output_window(self):
        self.children.output_window.variables.name_database = self.variables.name_database
        self.children.output_window.variables.name_table = self.variables.name_table
        self.children.output_window.variables.pady = self.variables.pady
        self.children.output_window.variables.padx = self.variables.padx

        return

    def export_current_table(self):
        try:
            file = filedialog.asksaveasfilename(title='Select file',
                                                confirmoverwrite=True,
                                                initialdir=os.path.dirname(__file__))
            if file:
                sql_functions.excel_export_single(self.variables.name_database,
                                                  self.variables.name_table,
                                                  file)

                messagebox.showinfo(message='Таблица экспортирована в Excel')
        except Exception as er:
            if type(er) == sql_functions.TableCreationError:
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message=f'Возникла ошибка при экспорте в Excel: {sql_functions.get_err_msg(er)}')
                return 1
            else:
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message='Возникла неизвестная ощибка при экспорте в Excel')
                return -1


class InputWindow(Window):
    def __init__(self, name_window, *args, **kwargs):
        super().__init__(name_window, *args, **kwargs)

        # self.root.geometry('500x300')
        self.root.resizable(False, False)

        self.variables = InputWindowVariables()

        self.labels = []
        self.entries = []
        self.entry_variables = dict()

        self.get_values_button = Button(self.root,
                                        text='Ввести данные и отправить в таблицу',
                                        command=self.get_values)
        self.get_values_button.pack(side='bottom',
                                    padx=self.variables.padx,
                                    pady=self.variables.pady)

    def initialize_buttons(self):
        input_data = [index for index in self.variables.data_format if index[2]]
        for column in input_data:
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
        try:
            for index, OBJECT in enumerate(self.entries):
                self.entry_variables[self.variables.data_format[index][0]] = OBJECT.get()
            self.variables.algorithm(self.entry_variables)
            values = [tuple(map(lambda x: x[1], self.entry_variables.items())), ]
            sql_functions.sql_input(self.variables.name_database,
                                    self.variables.name_table,
                                    self.variables.data_format,
                                    values)
            messagebox.showinfo(message='Данные успешно внесены')
            return 0
        except Exception as er:
            if type(er) == sql_functions.SqlInputError:
                messagebox.showinfo(title='Ошибка',
                                    icon='error',
                                    message=f'Ошибка при занесении данных в таблицу: {sql_functions.get_err_msg(er)}')
                return 1
            else:
                return -1


class InputWindowVariables:
    def __init__(self):
        self.name_database = None
        self.name_table = None
        self.data_format = None
        self.algorithm = None
        self.padx = None
        self.pady = None


class OutputWindow(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.variables = OutputWindowVariables()
        self.text_field = Label(self.root, text=self.variables.output_text, anchor='nw')
        self.text_field.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.update_button = Button(self.root, text='Получить данные из таблицы', command=self.update_values)
        self.update_button.pack(padx=self.variables.padx, pady=self.variables.pady, side='bottom')

    def update_values(self):
        try:
            text = sql_functions.sql_output(self.variables.name_database,
                                            self.variables.name_table)
            formatted_text = sql_functions.formatted_print(text)
            self.variables.output_text = formatted_text
            self.text_field.config(text=self.variables.output_text)
            print(formatted_text)
        except Exception as er:
            if type(er) == sql_functions.SqlOutputError:
                a = sql_functions.get_err_msg(er)
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message=f'Возникла ошибка при получении данных из таблицы: {a}')
            else:
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message='Возникла неизвестная ошибка при получении данных из  таблицы')
            return


class OutputWindowVariables:
    def __init__(self):
        self.padx = None
        self.pady = None
        self.name_database = None
        self.name_table = None
        self.output_text = str()


if __name__ == '__main__':
    pass
