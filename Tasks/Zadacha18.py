import gui

window = gui.MainWindow("Приложение 'Базы данных' (задача 18)")
window.variables.input_window_class_name = 'InputWindow'
window.variables.input_window_name = 'Ввод данных для задачи 18'

window.variables.data_format = [('num', 'INT', 'enter num'), ('type', 'VARCHAR(50)', 'enter object type')]

window.root.mainloop()
