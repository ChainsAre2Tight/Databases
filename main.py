import os
import sys
from os import listdir
from os.path import isfile, join
import re
import importlib

import gui

pattern = r'^Zadacha\w+.py$'  # sets the patter for RegEx to search for suitable files with presets
imported_modules = dict()


def get_relative_path() -> str:
    """:return: path to current file"""
    dirname = os.path.dirname(__file__)
    return dirname


def get_list_of_all_files() -> list:
    """:returns: list of all files in a directory 'Tasks'"""
    mypath = os.path.join(get_relative_path(), 'Tasks')
    only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    only_files.sort()
    return only_files


def get_list_of_files_matching_pattern() -> list:
    """:returns: list of all files, which names match selected pattern"""
    global pattern
    list_of_valid_files = list()
    list_of_all_files = get_list_of_all_files()
    for file in list_of_all_files:
        match = re.search(pattern, file)
        if match:
            list_of_valid_files.append(file)
    return list_of_valid_files


def import_all_valid_modules():
    """This function imports all modules that match the pattern, see get_list_of_files_matching_pattern"""
    global imported_modules
    list_of_valid_files = [i.rstrip('.py') for i in get_list_of_files_matching_pattern()]
    path = os.path.join(get_relative_path(), 'Tasks')
    sys.path.append(path)
    for index, FILE in enumerate(list_of_valid_files):
        imported_modules[FILE] = importlib.import_module(FILE)


def button_function(module_name, current_window):
    """This is a decorator"""

    def set_settings():
        """This function applies settings from imported preset to imported MainWindow instance
        Then it updates comboboxes accordingly, see MainWindow.update_comboboxes for more info"""
        imported_modules[module_name].set_variables(current_window)
        current_window.variables.name_preset = module_name
        current_window.update_comboboxes()

    return set_settings


def initialize_menu(current_window):
    """This function creates menu buttons for MainWindow that lets user select a preset"""
    for module_name in imported_modules.keys():
        current_window.file_menu.add_command(label=module_name, command=button_function(module_name, current_window))


if __name__ == '__main__':
    import_all_valid_modules()
    window = gui.MainWindow()
    initialize_menu(window)
    window.root.mainloop()
