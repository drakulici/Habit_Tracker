# habit_manager.py - this module is responsible for handling the habit operations like adding a new habit, viewing habits, etc.
"""
habit_manager.py
This module is responsible for handling habit operations such as adding a new habit, viewing habits, marking habits as completed, and deleting habits. It also includes functionality to insert and delete predefined habits.
Classes:
    HabitManager: Manages habit-related operations including adding, viewing, marking as completed, and deleting habits.
Methods:
    __init__: Initializes the HabitManager with a database connection.
    add_habit: Adds a new habit to the database.
    view_habits: Displays all habits stored in the database.
    mark_habit_completed: Marks a specified habit as completed for the current day.
    delete_habit: Deletes a specified habit from the database.
    insert_predefined_habits: Inserts predefined habits into the database.
    delete_predefined_habits: Deletes predefined habits from the database.
"""

from habit import Habit
from database import Database
from predefined_data import Predefined_data


class HabitManager:
    def __init__(self):
        self.database = Database()

    def add_habit(self, name, description, frequency, created_date):
        habit = Habit(name, description, frequency, created_date)
        habit.save() 

    def view_habits(self):
        all_names = self.database.get("habits", "id, name") 
        for name in all_names:
            print(f"{name[0]}.{name[1]}")

    def mark_habit_completed(self, habit_id):
        habit = Habit(name=None, description=None, frequency=None, created_date=None)
        habit.mark_completed(habit_id)

    def delete_habit(self, habit_id):
        habit = Habit(name=None, description=None, frequency=None, created_date=None)
        habit.delete(habit_id)

        
    def insert_predefined_habits(self):
        predefined_data = Predefined_data()
        predefined_data.insert_data()
        predefined_data.insert_completed_dates()
    
    def delete_predefined_habits(self):
        predefined_data = Predefined_data()
        predefined_data.delete_data()