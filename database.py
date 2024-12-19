# database.py
"""
This module provides a class `Database` for handling SQLite database operations related to habit tracking.
Classes:
    Database: A class to manage database connections, create tables, insert data, and query data.
Methods:
    __init__(self): Initializes the database connection and cursor.
    get_database_name(self): Returns the name of the database.
    create_tables(self): Creates the 'habits' and 'completed_dates' tables if they do not exist.
    get(self, table_name, column): Retrieves specified column data from a given table.
    get_all_tables(self): Returns the names of all tables in the database.
    get_all_data_from_habit_table(self): Returns all data from the 'habits' table.
    get_all_data_from_completed_dates_table(self): Returns all data from the 'completed_dates' table.
    insert(self, table_name, data): Inserts data into the specified table.
    close(self): Closes the database connection.
    count_habits(self): Returns the count of habits in the 'habits' table.
    get_all_names(self): Returns the names of all habits in the 'habits' table.
Usage:
    Create an instance of the Database class and call its methods to interact with the database.
"""

import sqlite3
from datetime import datetime, timedelta


class Database:
    """ This class is responsible for handling the database operations. """
    def __init__(self):                 # This constructor is initializing the connection and cursor objects.
        self.connection = sqlite3.connect(self.get_database_name())
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def get_database_name(self):            # This method is returning the database name.
        return "database.db"


    """ This method is creating 2 tables, 1 habits table and 1 completed_dates table. """
    def create_tables(self):
        # This line is creating a habits table with 5 columns: id, name, description, frequency, and created_date.
        self.cursor.execute("CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY, name, description, frequency, created_date)")
        # This line is creating a completed_dates table with 3 columns: id, habit_id, and completed_date.
        self.cursor.execute("CREATE TABLE IF NOT EXISTS completed_dates (id INTEGER PRIMARY KEY, habit_id, completed_date, FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE)")
        self.connection.commit()

    def get(self,table_name, column):
        res = self.cursor.execute("SELECT " + column + " FROM " + table_name)
        return res.fetchall()

    def get_all_tables(self):               # This method is returning all the tables in the database.
        self.cursor.execute("SELECT name FROM sqlite_master")
        return self.cursor.fetchall()

    def get_all_data_from_habit_table(self): # This method is returning all the data from the habits table.
        res = self.cursor.execute("SELECT * FROM habits")
        return res.fetchall()
    
    def get_all_data_from_completed_dates_table(self): # This method is returning all the data from the completed_dates table.
        res = self.cursor.execute("SELECT * FROM completed_dates")
        return res.fetchall()

    def insert(self, table_name, data):     # This method is inserting data into the specified table.
        if table_name == "habits":
            self.cursor.executemany("INSERT INTO habits (name, description, frequency, created_date) VALUES (?,?,?,?)", data)
        elif table_name == "completed_dates":
            self.cursor.executemany("INSERT INTO completed_dates (habit_id, completed_date) VALUES (?,?)", data)
        self.connection.commit()

    def close(self):                        # This method is closing the connection to the database.
        self.connection.close()


    def count_habits(self):        # This method is returning the count of habits in the habits table.
        res = self.cursor.execute("SELECT COUNT(*) FROM habits")
        return res.fetchone()[0]

    def get_all_names(self):    # This method is returning the names of all habits in the habits table.
        res = self.cursor.execute("SELECT name FROM habits")
        return res.fetchall()

myDatabase = Database() # This line is creating an instance of the Database class.
myDatabase.create_tables() # This line is calling the create_tables method of the Database class to create tables in the database.
