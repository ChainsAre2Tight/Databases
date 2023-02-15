import sys
from tkinter import messagebox, ttk
from tkinter import filedialog
import os

import sql_functions
import config_reader
from tkinter import *


def default_function(a):
    """This is a template function, do not touch"""
    return a


def pass_function():
    """Do not touch"""
    pass


class Window:
    """Template class for windows"""

    def __init__(self, name_window="Untitled", *args, **kwargs):
        self.root = Tk()
        self.root.title(name_window)

# TODO replace tabulate with pandas.pivot_table
class MainWindowChildren:
    """Object of this class stores child objects for an instance of MainWindow"""

    def __init__(self):
        self.input_window = None  # instance of InputWindow class
        self.input_window_open = False  # is True when input window is open
        self.output_window = None  # instance of OutputWindow class
        self.output_window_open = False  # is True when output window is open


class MainWindowVariables:
    """Object of this class stores variables for an instance of MainWindow"""

    def __init__(self):
        self.name_preset = str()  # name of currently selected preset
        self.name_database = str()  # name of currently selected database
        self.name_table = str()  # name of currently selected table
        self.data_format = tuple()  # proprietary format for use in sql_function module, see ZadachaTest.py for info
        self.input_window_name = str()  # name of input window
        self.padx = 100  # padx for use in tkinter.pack()
        self.pady = 1  # padx for use in tkinter.pack()
        self.increment_column_name = 'id'  # determines the first column name, that is AUTO_INCREMENTed
        self.algorithm = default_function  # stores function, that is used to aggregate each inputed row
        self.list_of_databases = []  # stores list of all databases used with current preset, see update_comboboxes()
        self.list_of_tables = []  # stores list of all tables used with current databases, see update_comboboxes()
        self.theme = 'clam'  # determines theme for widgets


class MainWindowWidgets:
    """Object of this class stores widgets of an instance of MainWindow"""

    def __init__(self):
        self.dbname_entry_label = None
        self.dbname_button = None  # button that confirms database selection
        self.tname_entry_label = None
        self.tname_button = None  # button that confirms table selection
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

        self.style = ttk.Style(self.root)
        self.style.theme_use(self.variables.theme)

    def initialize_widgets(self):
        # TODO get values from entries by button press
        """This method creates widgets """
        self.widgets.dbname_entry_label = Label(self.root, text='Введите название базы данных')
        self.widgets.dbname_entry_combobox = ttk.Combobox(self.root, values=self.variables.list_of_databases)
        self.widgets.dbname_button = ttk.Button(self.root, text='Записать значение', command=self.get_dbname)
        self.widgets.tname_entry_label = Label(self.root, text='Введите название таблицы')
        self.widgets.tname_entry_combobox = ttk.Combobox(self.root, values=self.variables.list_of_databases)
        self.widgets.tname_button = ttk.Button(self.root, text='Записать значение', command=self.get_name_table)
        self.widgets.create_database_button = ttk.Button(self.root, text='Создать базу данных',
                                                         command=self.create_database)
        self.widgets.create_table_button = ttk.Button(self.root, text='Создать таблицу', command=self.create_table)
        self.widgets.open_input_window_button = ttk.Button(self.root, text='Ввести данные в таблицу',
                                                           command=self.open_input_window)
        self.widgets.export_button = ttk.Button(self.root, text='Экспортировать данные в Excel',
                                                command=self.export_current_table)
        self.widgets.button_open_output_window = ttk.Button(self.root, text='Открыть окно вывода',
                                                            command=self.open_output_window)
        self.widgets.button_close_window = ttk.Button(self.root, text='Закрыть окно', command=self.on_closing)
        self.pack_widgets()
        return

    def pack_widgets(self):
        """This method determines widget placement"""
        self.widgets.dbname_entry_label.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.dbname_entry_combobox.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.dbname_button.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.tname_entry_label.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.tname_entry_combobox.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.tname_button.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.create_database_button.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.create_table_button.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.open_input_window_button.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.export_button.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.button_open_output_window.pack(padx=self.variables.padx, pady=self.variables.pady)
        self.widgets.button_close_window.pack(padx=self.variables.padx, side='bottom', pady=self.variables.pady)

    def update_comboboxes(self):
        """
        This method reads config using .read method of ConfigReader class, stores it in schema variable
        If user has not yet selected a preset, it does nothing
        If user has already selected a preset, it updates database Combobox to include list of databases used with that
        preset, that are stored in config
        If both the preset and database are selected, it does the same for list of tables

        In config all the data is stored as preset:database:table format, new presetes are created from menu buttons,
        see add_to-config and remove_from_config for more info
        """
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
        """
        This method gets value from database combobox and stores it within .variables.name_database
        Then it displayes a pop-up window with the name of currently selected database
        """
        self.variables.name_database = self.widgets.dbname_entry_combobox.get()
        self.update_comboboxes()
        messagebox.showinfo(message=f'''Название базы данных внесено
(Выбраная база данных: '{self.variables.name_database}')''')
        return

    def create_database(self):
        """
        This method creates a new database using create_db function of sql_functions module
        Then it dispalys a pop-up window with a list of all databases on that server

        As create_db raises sql_function.DatabaseCreationError, try-except module uses it to determine if an error
        occured in create_db or in this function and then an error message is displayed accordingly
        """
        try:
            sql_functions.create_db(self.variables.name_database)
            list_of_all_databases = '\n'.join(sql_functions.get_list_of_databases(True))
            messagebox.showinfo(message=f'''База данных {self.variables.name_database} создана

Список всех баз данных:
{list_of_all_databases}''')
        except Exception as er:
            if type(er) == sql_functions.DatabaseCreationError:
                messagebox.showinfo(message=f'Ошибка при создании базы данных: {sql_functions.get_err_msg(er)}')
            else:
                messagebox.showinfo(message='Возникла неизвестная ошибка при создании базы данных')
        return

    def get_name_table(self):
        """
        This method gets value from tablename combobox and stores it within .variables.name_table
        Then it displayes a pop-up window with the name of currently selected table
        """
        self.variables.name_table = self.widgets.tname_entry_combobox.get()
        messagebox.showinfo(message=f'''Название таблицы внесено
(Выбранная таблица: '{self.variables.name_table}')''')
        return

    def create_table(self):
        """
        This method creates a new table using simple_create_table function of sql_functions module
        Then it dispalys a pop-up window with a list of all tables within that database

        As simple_create_table raises sql_function.TableCreationError, try-except module uses it to determine if an error
        occured in create_db or in this function and then an error message is displayed accordingly
        """
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
        except Exception as er:
            if type(er) == sql_functions.TableCreationError:
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message=f'Возникла ошибка при создании таблицы: {sql_functions.get_err_msg(er)}')
            else:
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message='Возникла неизвестная ошибка при создании таблицы')
        finally:
            return

    def add_to_config(self):
        """
        This method adds to config currently selected relationship preset-database-table using .write method of Database_config class of config_reader module
        Than it displays a pop-up window displaying either a warning or a success message
        """
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
        return

    def remove_from_config(self):
        """
        This method removes currently selected relationship preset-database-table from config using .delete method of Database_config class of config_reader module
        Than it displays a pop-up window displaying either a warning or a success message
        """
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
        return

    def open_input_window(self):
        """
        This method defines all actions that are performed when input window must be opened
        """
        if self.variables.data_format == tuple():  # checks if a preset has been selected
            messagebox.showwarning(message='Не выбрана конфигурация')
        elif not self.children.input_window_open:  # checks if another input window is open
            self.children.input_window = InputWindow(
                self.variables.input_window_name)  # creates an instance of InputWindow
            self.clone_values_to_input_window()  # copies variables
            self.children.input_window.initialize_buttons()  # initializes widgets depending on a selected preset
            self.children.input_window.root.protocol("WM_DELETE_WINDOW",
                                                     self.on_closing_input_window)  # sets a widow closure protocol
            self.children.input_window_open = True  # sets "window opened" flag to true
            self.root.withdraw()  # hides main window
        return

    def on_closing_input_window(self):
        """Defines actions that are performed when input window is closed"""
        self.children.input_window_open = False  # sets flag to False
        self.children.input_window.root.destroy()  # destroys window
        self.children.input_window = None  # destoys object
        self.root.deiconify()  # unhides the main window
        return

    def open_output_window(self):
        """Defines a series of actions that are performed when an output window must be opened"""
        if not self.children.output_window_open:  # checks if another output window is opened
            self.children.output_window = OutputWindow(
                self.variables.name_table)  # creates an instance of OuptupWindow class
            self.children.output_window.root.protocol("WM_DELETE_WINDOW",
                                                      self.on_closing_output_window)  # sets window closure protocol
            self.clone_values_to_output_window()  # copies some variables from parent to child
            self.children.output_window_open = True  # sets window open flag to True
        else:  # if another window is already opened
            self.clone_values_to_output_window()  # updates som evariables
            self.children.output_window.root.title(
                self.variables.name_table)  # re-titles output window to match currently selected table
            self.children.output_window.root.lift()  # brings the window to the top
        return

    def on_closing_output_window(self):
        """This method defines a series of actions that are performed when output window is due to be closed"""
        self.children.output_window_open = False  # sets window open flag to False
        self.children.output_window.root.destroy()  # destroys the window
        self.children.output_window = None  # destroys the window object
        return

    def on_closing(self):
        """This method defines a series of actions that are performed when the main window is due to be closed"""
        if messagebox.askokcancel("Выход", "Вы точно хотите выйти?"):
            self.root.destroy()
            sys.exit()

    def clone_values_to_input_window(self):
        """This method copies some variables from parent main window to its respective input window child"""
        self.children.input_window.variables.data_format = self.variables.data_format
        self.children.input_window.variables.name_database = self.variables.name_database
        self.children.input_window.variables.name_table = self.variables.name_table
        self.children.input_window.variables.pady = self.variables.pady
        self.children.input_window.variables.padx = self.variables.padx
        self.children.input_window.variables.algorithm = self.variables.algorithm
        self.children.input_window.variables.theme = self.variables.theme
        self.children.input_window.style.theme_use(self.children.input_window.variables.theme)
        return

    def clone_values_to_output_window(self):
        """This method copies some variables from parent main window to its respective input window child"""
        self.children.output_window.variables.name_database = self.variables.name_database
        self.children.output_window.variables.name_table = self.variables.name_table
        self.children.output_window.variables.pady = self.variables.pady
        self.children.output_window.variables.padx = self.variables.padx
        self.children.output_window.variables.theme = self.variables.theme
        self.children.output_window.style.theme_use(self.children.output_window.variables.theme)
        return

    def export_current_table(self):
        """
        This method saves the currently selected table in .xlsx format
        It shows a savefiledialog that lets the user select both the directory and the name of an exported file
        Then it actually performes the export using excel_export_single function of sql_functions module

        As excel_export_single raises sql_function.SqlExportError, try-except module uses it to determine if an error
        occured in excel_export_single or in this function and then an error message is displayed accordingly
        """
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
            else:
                messagebox.showinfo(title='Ошибка', icon='error',
                                    message='Возникла неизвестная ощибка при экспорте в Excel')
        return


class InputWindow(Window):
    """
    An object of this class serves as an input window for the main one
    Widgets in this window are dynamically created from data_format variable of the main window
    When this window is open, the main one is hidden so that user won't performe any undesirable actions
    """

    def __init__(self, name_window, *args, **kwargs):
        super().__init__(name_window, *args, **kwargs)

        # self.root.geometry('500x300')
        self.root.resizable(False, False)

        self.variables = InputWindowVariables()  # creates an instance of sub-class for variables

        self.labels = []  # this list holds all Label objects of this window
        self.entries = []  # this list holds all Entry objects of this window
        self.entry_variables = dict()  # this dictionary is filled when get_values method is called, it is used for storing values from entries
        self.style = ttk.Style(self.root)

        self.get_values_button = ttk.Button(self.root,
                                            text='Ввести данные и отправить в таблицу',
                                            command=self.get_values)
        self.get_values_button.pack(side='bottom',
                                    padx=self.variables.padx,
                                    pady=self.variables.pady)

    def initialize_buttons(self):
        """
        This method creates Label and Entry widgets determined by data_format variable, see ZadachaTest for more info
        Creates entries only form column for which description is provided
        """
        input_data = [index for index in self.variables.data_format if
                      index[2]]  # creates entries only form column for which description is provided
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
        return

    def get_values(self):
        """
        This method gets values from entries, processes them using .variables.algorithm function and sends them to sql table using sql_input function of sql_function module

        As sql_input raises sql_function.SqlInputError try-except module uses it to determine if an error
        occured in sql_input or in this function and then an error message is displayed accordingly
        """
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
    """An instance of this class is used to store some variables for InputWindow class"""

    def __init__(self):
        self.name_database = None
        self.name_table = None
        self.data_format = None
        self.algorithm = None
        self.padx = None
        self.pady = None
        self.theme = str()


class OutputWindow(Window):
    """This class defines window that is used to show data from currently selected table"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.variables = OutputWindowVariables()
        self.text_field = Label(self.root, text=self.variables.output_text, anchor='nw')
        self.text_field.pack(padx=self.variables.padx, pady=self.variables.pady)

        self.update_button = ttk.Button(self.root, text='Получить данные из таблицы', command=self.update_values)
        self.update_button.pack(padx=self.variables.padx, pady=self.variables.pady, side='bottom')
        self.style = ttk.Style(self.root)

    def update_values(self):
        """
        This method gets values from table using sql_output function of sql_functions module and sets the text variable to text, generated by by formatted_print

        As sql_output raises sql_function.SqlOutputError, try-except module uses it to determine if an error
        occured in sql_output or in this function and then an error message is displayed accordingly
        """
        try:
            text = sql_functions.sql_output(self.variables.name_database,
                                            self.variables.name_table)
            formatted_text = sql_functions.formatted_print(text)
            self.variables.output_text = formatted_text
            self.text_field.config(text=self.variables.output_text)
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
    """An instance of this class is created by OutputWindow to sore some variables"""

    def __init__(self):
        self.padx = None
        self.pady = None
        self.name_database = None
        self.name_table = None
        self.output_text = str()
        self.theme = str()


if __name__ == '__main__':
    pass
