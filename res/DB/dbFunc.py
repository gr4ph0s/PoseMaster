import os
import sqlite3

class DbFunc(object):
    """ Interface class for easily get access to data"""

    def __init__(self, dbPath):
        """
        We assume db path is valid and db exist or is in folder where she can be writted.
        :param dbPath: 
        """
        self.dbPath = dbPath
        self.connection = None
        self.cursor = None

    def check_db_exist(self):
        """
        Check if a db exist or not
        :return: Bool
        """
        return os.path.exists(self.dbPath)

    def connect(self):
        """
        Set self.connection and self.cursor if success
        :return: Bool if succes or not
        """
        if not self.connection and not self.cursor:
            try:
                self.connection = sqlite3.connect(self.dbPath)
                self.cursor = self.connection.cursor()
                return True
            except:
                return False

        return False

    def disconnect(self):
        """
        Disconnect from db and set self.cursor/connection to None
        :return: True or False
        """
        try:
            self.connection.close()
            self.connection = None
            self.cursor = None
            return True
        except:
            return False

    def select(self, column_name, table, conditions, order_condition=None, nb=0):
        """
        execute a select command into the db.
        Connection and disconnection are Note handle !
        :param column_name: list of the column name
        :param table:  the table from we want data
        :param conditions:  dict the condition to match => {'column_name': [Value,"!="]}
        :param order_condition: String for order condition
        :param nb: the max number of result we want. 0 for all
        :return: 
        """
        if not column_name or not table or not conditions:
            return False

        text_column = ', '.join(column_name)

        text_condition = str()
        data_condition = dict()
        first = True
        for condition in conditions:
            data_condition[condition] = conditions[condition][0]

            if first:
                first = False
            else:
                text_condition += " and "

            text_condition += condition
            text_condition += " "
            if len(conditions[condition]) == 1:
                text_condition += "="
            else:
                text_condition += conditions[condition][1]
            text_condition += " :"
            text_condition += condition

        sql = 'SELECT {} ' \
              'FROM {} ' \
              'WHERE {} '.format(text_column, table, text_condition)

        if order_condition:
            sql += 'ORDER BY {}'.format(order_condition)

        if nb:
            sql += 'LIMIT {}'.format(nb)

        self.cursor.excute(sql, data_condition)
        result_list = list()
        for row in self.cursor:
            result_dict = dict()
            for i, column_name in enumerate(column_name):
                result_dict[column_name] = row[i]
            result_list.append(result_dict)

        return result_list

    def insertOne(self, table_name, datas):
        """
        Insert One data into the db. Return the inserted id or False
        Connection and disconnection are Note handle !
        :param table_name: String table name
        :param datas: dict contening data {'column_name': value}
        :return: False if fail or the id inserted
        """
        if not table_name or not datas:
            return False

        try:
            sql = 'INSERT INTO {}' \
                  '({})' \
                  'VALUES' \
                  '(:{})'.format(
                table_name,
                ', '.join(datas.keys()),
                ',:'.join(datas.keys())
            )

            self.cursor(sql, datas)

            self.connection.commit()

            return self.cursor.lastrowid

        except:
            self.connection.rollback()
            return False

    def insertMultiple(self, table_name, datas):
        """
        Insert One data into the db. Return the inserted id or False
        Connection and disconnection are Note handle !
        :param table_name: String table name
        :param datas: list of dict contening data {'column_name': value}
        :return: False if fail or the id inserted
        """
        if not table_name or not datas:
            return False

        try:
            sql = 'INSERT INTO {}' \
                  '({})' \
                  'VALUES' \
                  '(:{})'.format(
                table_name,
                ', '.join(datas.keys()),
                ',:'.join(datas.keys())
            )

            self.cursor(sql, datas)

            self.connection.commit()

            return self.cursor.lastrowid

        except:
            self.connection.rollback()
            return False



    def check_table_exist(self, table_name):
        """
        Check if a table exist in the db
        :param table_name: The name of the table to check
        :return: Bool, True if exist
        """
        if not self.connect():
            return False

        column = ["*"]
        table = "sqlite_master"
        conditions = dict()
        conditions["name"] = [table_name, "="]

        data = self.select(column, table, conditions)

        self.disconnect()

        if data:
            return True
        else:
            return False