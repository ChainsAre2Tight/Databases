Структура этой программы следующая:

class Window - статический, от него наследуются другие окна

class MainWindow - класс главного окна, содержит 3 подкласса:
.variables(MainWindowVariables),
который используется для хранения переменных (дабы не мешали в дебаге искать нужный объект) и
.widgets(MainWindowWidgets), содержащий все виджеты основного окна
.children(MainWindowChildren), хранящий объекты окон ввода-вывода и bool открыты ли они

В классе основного окна определены методы для работы с его виджетами, которые для непосредственной
работы с MySQL обращаются к модулю sql_functions

Меню содержит следующий функционал:
1) выбор пресета решаемой программы (в нем определены типы данных для таблицы, название окна и алгоритм обработки данных)
2) Сохранение/удаление текущий конфигурации из конфига

Конфигурация представляет собой отношение пресет - база_данных - таблица, которая позволяет пользователю в главном окне выбрать из выпадающего меню одну из сохраненных баз данных для текущего пресета и одну из сохраненных таблиц в выбранной базе данных, что позволяет пользователю быстрее найти необходимую рабочую область

В главном окне представлен следующий функционал:
1) Выпадающее меню для выбора базы данных
2) Кнопка для подтверждения выбора базы данных
3) Выпадающее меню для выбора таблицы
4) Кнопка для подтверждения выбора таблицы
5) Кнопка для создания базы данных
6) Кнопка для создания таблицы внутри выбранной базы данных
7) Кнопка для вызова окна ввода данных в таблицу
8) Кнопка для экспорта текущей таблицы в Excel
9) Кнопка для вызова окна вывода
10) Кнопка для закрытия окна

Окно ввода данных может быть открыто лишь одно, чтобы пользователь ничего не сломал, поэтому при открытом окне ввода главное окно сворачивается.

Окно вывода также может быть только одно, но когда оно открыто главное окно не сворачивается, лишь кнопка, отвечающая за открытие окна вывода обновляет в уже открытом окне данные о выбранной таблице и поднимает его на передний план.

Поля ввода в окне ввода и их описание генерируются автоматически на основе пресета(см. ZadachaExample)

Окно ввода содержит следующий функционал:
1) Кнопка отправки данных, которая записывает введенные пользователем данные, обрабатывает их и отправляет в базу данных
2) Для каждого столбца, для которого в формате данных указано описание, генерируется текст с этим описанием и поле для ввода данных

Окно вывода имеет кнопку для получения данных из выбранной в главном окне таблицы

Рассмотрим типичный сценарий использования этой программы на примере пресета ZadachaExample:

1) Пользователь выбирает пресет из первого раздела меню "Выбрать задачу"
2) Если у пользователя уже есть сохраннённая база данных и таблица для этой задачи, что он выбирает базу данных из выпадающего меню, подтверждает ввод нажатием на соответствующую кнопку и потом делает тоже самое для выбора таблицы. Если у пользователя еще нет сохранненной таблицы, то он печатает в окно ввода название базы данных и таблицы и подтверждает ввод
3) Если нужно создать базу данных и/или таблицу, пользователь может это сделать с помощью соответствующих пунктов меню
4) Пользователь вызывает окно ввода данных и порядно вводит нужные данные, отправляя их в базу данных
5) Пользователь вызывает окно вывода и/или сохраняет таблицу в .xlsx формате

После этого (ну или в любой момент) пользователь может закрыть окно или переключиться на другой пресет для работы с другим форматом данных
