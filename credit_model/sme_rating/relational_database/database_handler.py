from multiprocessing import connection
from optparse import Values
from os.path import exists
import sqlite3
from sqlite3 import Error

from company_data import getCompanyData


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    if not exists(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()


def create_company_table(company_dict, connection_obj):
    cursor_obj = connection_obj.cursor()
    sql_statement = """CREATE TABLE tbl_company_data ("""
    for key in list(company_dict.keys()):
        values = company_dict[key]
        if (True in list(map(lambda x: x.isdigit(), list(map(lambda x: x.replace(".",""), values))))):
            sql_statement += (key+" FLOAT NOT NULL, ")
        else:
            sql_statement += (key+" TEXT  NOT NULL, ")
    sql_statement = sql_statement[:-2]
    sql_statement += ")"
    # execute sql statement
    cursor_obj.execute(sql_statement)


def insert_company_data(company_dict, connection_obj):
    cursor_obj = connection_obj.cursor()
    sql_statement = """INSERT INTO TABLE tbl_company_data ("""
    for key in list(company_dict.keys()):
        values = company_dict[key]
        if (True in list(map(lambda x: x.isdigit(), list(map(lambda x: x.replace(".",""), values))))):
            sql_statement += (key+" FLOAT NOT NULL,")
        else:
            sql_statement += (key+" TEXT  NOT NULL,)")
    sql_statement += ") VALUES("
    sql_statement = ""
    
    # execute sql statement
    cursor_obj.execute(sql_statement)


def create_all_tables(connection_obj):
    company_dict = getCompanyData()
    create_company_table(company_dict,connection_obj)


def main():
    # create database (if applicable)
    company_database = "sme_rating\databases\company_data.db"
    if exists(company_database):
        connection_obj = sqlite3.connect(company_database)
    else:
        connection_obj = create_connection(company_database)
    create_all_tables(connection_obj)
    
    

if __name__ == "main":
    main()