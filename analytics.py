# analytic.py - this module is responsible for handling the analytics operations 
"""
This module is responsible for handling the analytics operations related to habits.
Functions:
    - get_tracked_habits(): Retrieves and prints all tracked habits from the database.
    - get_habits_with_same_periodicity(): Retrieves and prints habits with the same periodicity (daily or weekly) based on user input.
    - run_streak_all(): Calculates and prints the streak of completions for all habits.
    - run_streak_one(): Calculates and prints the streak of completions for a specific habit based on user input.
    - longest_run_streak_out_of_all_habits(): Determines and prints the habit(s) with the longest streak of completions.
"""



from database import Database
from habit_manager import HabitManager

database = Database()
habit_manager = HabitManager()

def get_tracked_habits():
    result = database.get("habits", "id, name")
    for i in result:
        print(i[0], ".", i[1])
    return result

def get_habits_with_same_periodicity():
    input_frequency = input("Enter the frequency, daily or weekly: ")
    print("\n")
    if "daily" in input_frequency:
        result = database.cursor.execute("SELECT name FROM habits WHERE frequency='daily'").fetchall()
        for i in result:
            print(i[0])
    elif "weekly" in input_frequency:
        result = database.cursor.execute("SELECT name FROM habits WHERE frequency='weekly'").fetchall()
        for i in result:
            print(i[0])
    return result

def run_streak_all():
    habits = database.get("habits", "*") 
    for habit in habits:
        habit_id = habit[0]
        habit_name = habit[1]
        completition_dates = database.cursor.execute("SELECT completed_date FROM completed_dates WHERE habit_id=?", (habit_id,)).fetchall()
        print(f"\nHabit {habit_name} has a streak of {len(completition_dates)} days.")

def run_streak_one():
    habit_id = input("Enter the id of the habit: ")
    habit_id = int(habit_id)
    completition_dates = database.cursor.execute("select completed_date from completed_dates where habit_id=?", (habit_id,)).fetchall()
    print(f"\nHabit {habit_id} has a streak of {len(completition_dates)} days.")

def longest_run_streak_out_of_all_habits():
    habits = database.get("habits", "*")
    max_streak = 0
    habit_with_max_streak = None

    for habit in habits:
        habit_id = habit[0]
        habit_name = habit[1]
        # Get all completion dates for this habit
        completion_dates = database.cursor.execute("SELECT completed_date FROM completed_dates WHERE habit_id=?",(habit_id,)).fetchall()
        streak = len(completion_dates)

        # Update the habit with the max streak if current streak is higher
        if streak > max_streak:
            max_streak = streak
            habit_with_max_streak = habit_name
        elif streak == max_streak:
            habit_with_max_streak += f", {habit_name}"

    if habit_with_max_streak:
        print(f"\nThe habit(s) with the most completions is/are '{habit_with_max_streak}' with {max_streak} completions.")
        return habit_with_max_streak
    else:
        print("\nNo habits found.")
        return None