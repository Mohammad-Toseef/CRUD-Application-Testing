from mysql.connector import connect, Error
import csv
import ast
import os
from dotenv import load_dotenv

DATABASE = "File_Storage"

HOST = "localhost"

load_dotenv('../environment.env')


class Connection:
    my_db = None
    table_name = ''
    table_columns = []

    @staticmethod
    def connect():
        """
        make a mysql database connection and store it inside my_db class variable
        :return: None
        """
        try:
            Connection.my_db = connect(
                    host=HOST,
                    user=os.environ.get('secretUser'),
                    password=os.environ.get('secretKey'),
                    database=DATABASE,
            )
        except Error as e:
            print('error'+str(e))

    @staticmethod
    def upload_file(name):
        """
        Create a new table with given filename and insert the file content
        to that table

        :param name: Filename that has to be uploaded
        :return: None

        Note: filename will be treated as table_name
        """
        with open(name, 'r') as file:
            filename = "_".join(name.split('.'))
            Connection.table_name = filename
            reader = csv.reader(file)
            statement = Connection.create_statement(filename, reader)
            cursor = Connection.my_db.cursor()
            cursor.execute('DROP TABLE IF EXISTS ' + filename + ';')
            cursor.execute(statement)
        with open(name, 'r') as file:
            reader = csv.reader(file)
            Connection.insert_statement(reader)
            Connection.my_db.commit()
            # Connection.load_columns()

    @staticmethod
    def load_columns():
        """
        Saves the column_names of the table in table_columns list
        :return: None
        """
        cursor = Connection.my_db.cursor()
        cursor.execute('SHOW COLUMNS FROM ' + DATABASE + '.' + Connection.table_name)
        data = cursor.fetchall()
        for column in data:
            Connection.table_columns.append(column[0])

    @staticmethod
    def datatype(val, current_type):
        """
        determines the type of the given value
        :param val: any number or string
        :param current_type: current_data_type of the value
        :return: sql data type
        """
        try:
            # Evaluates numbers to an appropriate type, and strings an error
            t = ast.literal_eval(val)
        except ValueError:
            return 'varchar'
        except SyntaxError:
            return 'varchar'
        if type(t) in [int, float]:
            if (type(t) in [int]) and current_type not in ['float', 'varchar']:
                # Use smallest possible int type
                if (-32768 < t < 32767) and current_type not in ['int', 'bigint']:
                    return 'smallint'
                elif (-2147483648 < t < 2147483647) and current_type not in ['bigint']:
                    return 'int'
                else:
                    return 'bigint'
            if type(t) is float and current_type not in ['varchar']:
                return 'decimal'
        else:
            return 'varchar'

    @staticmethod
    def create_statement(filename, reader):
        longest, columns, type_list = [], [], []
        Connection.table_columns = columns = Connection.load_metadata(columns, longest, reader, type_list)
        statement = 'create table ' + filename + '('

        for i in range(len(columns)):
            if i == 0 or i == 1:
                key = 'PRIMARY KEY' if i == 0 else 'UNIQUE'
                statement = (statement + '\n{} {}({})  ' + key + ',').format(columns[i].lower(),
                                                                             type_list[i], str(longest[i]))
#            elif type_list[i] == 'varchar':
#                statement = (statement + '\n{} varchar({}),').format(columns[i].lower(), str(longest[i]))
            else:
                statement = (statement + '\n' + '{} {}({})' + ',').format(columns[i].lower(), type_list[i],
                                                                          str(longest[i]))

        statement = statement[:-1] + ');'
        return statement

    @staticmethod
    def load_metadata(columns, longest, reader, type_list):
        """
        extracts column names from file content ,determines the data type of each column
        and max length required for each column field

        :param columns: a list to store column names
        :param longest: a list to store length of each column field
        :param reader: a csv reader object to read the file contents
        :param type_list: a list to store datatype of each column
        :return: list of columns
        """
        for row in reader:
            if len(columns) == 0:
                columns = row
                for col in row:
                    longest.append(0)
                    type_list.append('')
                    if col.count('.') > 0:
                        columns.insert(columns.index(col), "_".join(col.split('.')))
                        columns.pop(columns.index(col))
            else:
                for i in range(len(row)):
                    # NA is the csv null value
                    if type_list[i] == 'varchar' or row[i] == 'NA':
                        pass
                    else:
                        var_type = Connection.datatype(row[i], type_list[i])
                        type_list[i] = var_type
                    if len(row[i]) > longest[i]:
                        longest[i] = len(row[i])
        return columns

    @staticmethod
    def insert_statement(reader):
        """
        reads the file content and returns the corresponding insert statement
        :param reader: csv file reader
        :return:
        """
        i = 0
        cursor = Connection.my_db.cursor()
        for row in reader:
            if i == 0:
                pass
            else:
                insert_query = 'INSERT INTO ' + DATABASE + '.' + Connection.table_name + ' values ('
                for cell in row:
                    insert_query += '\'' + cell + '\','
                insert_query = insert_query[:-1] + ')'
                cursor.execute(insert_query)
            i += 1
        Connection.my_db.commit()

    @staticmethod
    def select_statement():
        """
        fetches the rows from the table
        :return: list of rows
        """
        cursor = Connection.my_db.cursor()
        data = []
        cursor.execute('SELECT * FROM '+Connection.table_name)
        data.append(Connection.table_columns)
        data.append(cursor.fetchall())
        return data

    @staticmethod
    def update(data, record_id):
        """
        :param data: row data to be updated
        :param record_id: id of the record
        :return: None
        """
        cursor = Connection.my_db.cursor()
        update_stat = 'UPDATE '+Connection.table_name+' SET '
        statement = ''
        for key, value in data.items():
            statement += str(key) + ' = \'' + str(value) + '\' ,'
        update_stat = update_stat + statement[:-1] + ' WHERE id = \'' + str(record_id) + '\''
        cursor.execute(update_stat)
        Connection.my_db.commit()

    @staticmethod
    def add_row(data):
        """
        adds a new row to table
        :param data: row to be updated
        :return: None
        """
        cursor = Connection.my_db.cursor()
        for key in list(data.keys())[:2]:
            value = data[key]
            cursor.execute('SELECT * FROM ' + Connection.table_name + ' WHERE '
                           + str(key) + ' = \'' + str(value) + '\'')
            if cursor.fetchone():
                return 'The value entered in \'' + key + ' field \' already exist !'
        add_stat = 'INSERT INTO ' + DATABASE + '.' + Connection.table_name + ' values('
        for value in data.values():
            add_stat = (add_stat + '\'' + str(value) + '\',')
        add_stat = add_stat[:-1] + ')'
        cursor.execute(add_stat)
        Connection.my_db.commit()
