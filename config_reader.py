import os
import re

default_config_name = 'list_of_databases.txt'


class DatabaseConfig:
    """
    This class is used to call its respective functions (read, write, check, delete)
    When creating an instance, custom config name can be passed, otherwise default name will be used
    """

    def __init__(self, name: str = None):
        global default_config_name
        if name is None:
            self.config_name = default_config_name
        else:
            self.config_name = name
        self.path = os.path.join(os.path.dirname(__file__), 'config')
        self.file_name = os.path.join(self.path, self.config_name)
        try:
            with open(self.file_name):
                pass
        except FileNotFoundError:
            with open(self.file_name, 'w'):
                pass

    def read(self) -> dict:
        """
        This function reads config and returns all preset-database-table relationships
        :return: dict[preset][database] = [table]
        """
        with open(self.file_name) as file:
            lines = list(map(lambda x: x.strip(), file.readlines()))
            schema = dict()
            for line in lines:
                preset = line[:line.find(':')]
                database = line[line.find(':') + 1:line.rfind(':')]
                table = line[line.rfind(':') + 1:]
                if preset in schema.keys():
                    if database in schema[preset].keys():
                        schema[preset][database].append(table)
                    else:
                        schema[preset][database] = [table]
                else:
                    schema[preset] = {database: [table]}
            return schema

    def write(self, preset: str, database: str, table: str) -> None:
        """
        This function writes a new line into config
        :param preset: preset
        :param database: database
        :param table: table
        """
        with open(self.file_name, 'a') as file:
            line = f'{preset}:{database}:{table}' + '\n'
            file.write(line)
        return

    def check(self, preset: str, database: str, table: str) -> bool:
        """
        This function checks if inputted preset-database-table relationship is already in config
        :param preset: preset
        :param database: database
        :param table: table
        :return: True, if present, else False
        """
        schema = self.read()
        if preset not in schema.keys() or database not in schema[preset] or table not in schema[preset][database]:
            return False
        return True

    def delete(self, preset: str, database: str | None = None, table: str | None = None) -> int:
        """
        This function reads all lines from config and re-writes config file without inputted relations
        :param preset: preset
        :param database: database
        :param table: table, if inputted deletes only database-table rows
        :return: number of deleted lines
        """
        count = 0
        with open(self.file_name) as file:
            old_lines = list(map(lambda x: x.strip(), file.readlines()))
            new_lines = list()
            if database is None:
                pattern = fr'{preset}:\w+$'
            elif table is None:
                pattern = fr'{preset}:{database}:\w+$'
            else:
                pattern = fr'{preset}:{database}:{table}$'
            for line in old_lines:
                if not re.match(pattern, line):
                    new_lines.append(line)
                else:
                    count += 1
        with open(self.file_name, 'w') as file:
            for line in new_lines:
                file.write(line + '\n')
        return count


if __name__ == '__main__':
    pass
