# habit.py - 
"""
This module defines the Habit class for managing habits, including saving,deleting and marking as complete in a database.
Class Habit represents a habit with attributes such as name, description, frequency, and created date. 
           Provides methods to save, delete and check off as completed habits in the database.
Methods:
    __init__(self, name=None, description=None, frequency=None, created_date=None): Initializes a new Habit instance.
    save(self): Saves the habit to the database.
    delete(self, id): Deletes the habit with the specified id from the database.
    mark_completed(self, habit_id): Marks the habit with the specified id as completed for the day.
"""


import datetime
from database import Database


class Habit:   # This class represents a habit with attributes such as name, description, frequency, and created date. 
    def __init__(self, name=None, description=None, frequency=None, created_date=None):    
        self.name = name
        self.description = description
        self.frequency = frequency
        if created_date is None:        # This line is checking if the created_date is None.
            self.created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # and if it is None, it is setting the created_date to the current date and time.
        else:
            self.created_date = created_date # If the created_date is not None, it is setting the created_date to the provided value.
        self.database =  Database()    # database instance is created in the __init__ method so that it can be used to interact with the database throughout the class.

    


    def save(self):
        data = [(self.name, self.description, self.frequency, self.created_date)] # This line is creating a list of tuples containing the habit data.
        self.database.insert("habits", data) # This line is calling the insert method of the Database class to insert the habit data into the habits table.
        print(f"{self.name} habit has been saved successfully!") # This line is printing a success message after saving the habit data.

    def delete(self, id):           # This method deletes the habit with the specified id from the database.
        data = (id,)                # This line is creating a tuple containing the id of the habit to be deleted.
        self.database.cursor.execute("DELETE FROM habits WHERE id=?", data)   # This line is executing a DELETE SQL query to delete the habit with the specified id.
        self.database.connection.commit()     # This line is committing the changes to the database.
        print(f"Habit with id {id} has been deleted successfully!")

    def mark_completed(self, habit_id):
        habit_id = int(habit_id)
        today = datetime.datetime.now()
        completed_date = today
        countQuery = self.database.cursor.execute("SELECT COUNT(*) FROM completed_dates WHERE habit_id = ? AND DATE(completed_date) = DATE(?)",(habit_id, completed_date)).fetchall()
        count = countQuery
        if count[0][0] == 0:          
            completed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = [(int(habit_id), completed_date)]        # USER INPUTS ARE ALWAYS STR!!!! SO WE NEED TO CONVERT TO INT!!! 4 hours lost!!! 
            self.database.insert("completed_dates", data)
            print("\nHabit marked as completed for the day. Well done! Keep it up!")
        else:
            print("\nHabit has already been marked as completed for the day.")
            return
        