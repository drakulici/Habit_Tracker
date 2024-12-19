# menu.py - this module is responsible for handling the menu operations and user interactions. 
# it serves as a central controller for the application.

"""
This module handles the user interface and menu navigation for the Habit Tracker application.

It presents menus to the user, processes their input, and calls functions from other modules
to perform actions like adding new habits, viewing existing ones, accessing analytics,
and managing predefined habits (admin only).

Functions:
- main_menu(): Displays the main menu options to the user. 
- chosen_habit_menu(): Displays options for a selected habit.
- analytics_menu(): Shows the analytics menu options.
- predefined_habit_menu(): Shows the predefined habits menu options.
- main(): The main function that runs the application, handling user input and coordinating actions.
- check_if_habits_in_database(): Checks if there are any habits in the database.
"""

import habit_manager
import analytics
from database import Database

def main_menu():                # This function displays the main menu options to the user.
    print("\n")
    print("Habit Tracker Menu")
    print("1. Add a new habit")
    print("2. View habits")
    print("3. Analytics Menu")
    print("4. Predefined habits - ADMIN ONLY - pass admin") 
    print("5. Exit")
    print("\n")

def chosen_habit_menu():         # This function displays options for a selected habit.y
    print("\n")
    print("1. Mark the Habit completed tor the day.")
    print("2. Delete Habit.")
    print("3. Back to main menu.")
    print("\n")

def analytics_menu():           # This function shows the analytics menu options.
    print("\n")
    print("1. All currently tracked habits.")
    print("2. All habits with the same periodicity.")
    print("3. Run streak of all defined habits.")
    print("4. Longest run streak of one habit.")
    print("5. Longest streak out of all habits.")
    print("6. Back to main menu.")
    print("\n")

def predefined_habit_menu():         # This function shows the predefined habits menu options.
    print("\n")
    print("1. Insert predefined habits. USE ONLY ONCE")
    print("2. Delete predefined habits.")
    print("3. Back to main menu.")
    print("\n")

def check_if_habits_in_database():                                     # This function checks if there are any habits in the database.
    database = Database()                                              # Create an instance of the Database class
    habits = database.get("habits","id, name")                         # Get all habit names from the database               
    if not habits:                                                     # If there are no habits in the database              
        print("\nNo habits to display.")                               # Display a message
        return False
    return True


def main():                                                             # This is the main function that runs the application.
    habit_m = habit_manager.HabitManager()                              # Create an instance of the HabitManager class
    database = Database()                                               # Create an instance of the Database class

    while True:
        main_menu()
        choice = input("Enter your choice: ")                           # Get the user's choice
        if choice == "1":                                               # If the user chooses to add a new habit
            while True:
                name = input("\nEnter habit name: ")
                if "*predefined*" in name:                              # Check if the habit name contains the predefined keyword
                    print("*predefined* is a reserved keyword. Please choose another name.")
                    break
                description = input("\nEnter habit description: ")      # Get the habit description
                while True:                                             # Loop until a valid frequency is entered
                    frequency = input("\nEnter habit frequency, 'daily' or 'weekly': ")
                    if frequency in ["daily", "weekly"]:                # Check if the frequency is valid
                        break
                    else:
                        print("\nInvalid frequency. Please enter 'daily' or 'weekly' only. Please try again.")
                habit_m.add_habit(name, description, frequency,created_date=None) # Add the habit
                break
        elif choice == "2":                                             # If the user chooses to view habits   
            if check_if_habits_in_database() is True:                               # Check if there are any habits in the database
                print("\nAll currently tracked habits:")
                print("Id - Habit Name")
                habit_m.view_habits()                                        # View the habits          
                print("\n")
            else:
                continue
            while True:                                                  # Loop until a valid choice is entered       
                habit_id = input("Enter the id of the habit you want to choose: ")
                chosen_habit_menu()                                      # Display the chosen habit menu options  
                choice = input("Enter your choice: ")
                if choice == "1":                                       # If the user chooses to mark the habit as completed
                    habit_m.mark_habit_completed(habit_id)
                    break
                elif choice == "2":                                     # If the user chooses to delete the habit
                    habit_m.delete_habit(habit_id)
                    break
                elif choice == "3":
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == "3":                                             # If the user chooses the analytics menu
            if check_if_habits_in_database() is True:                               # Check if there are any habits in the database
                analytics_menu()                                            # Display the analytics menu options
                analytics_choice = input("Enter your choice:")              # Get the user's choice
                if analytics_choice == "1":                                 # If the user chooses to view all currently tracked habits
                    print("All currently tracked habits:")
                    analytics.get_tracked_habits()                          # Call the get_tracked_habits function from the analytics module
                elif analytics_choice == "2":                               # If the user chooses to view habits with the same periodicity
                    print("All habits with the same periodicity.")         
                    analytics.get_habits_with_same_periodicity()            # Call the get_habits_with_same_periodicity function from the analytics module
                elif analytics_choice == "3":                               # If the user chooses to view the run streak of all defined habits
                    print("Run streak of all defined habit:")               
                    analytics.run_streak_all()                              # Call the run_streak_all function from the analytics module
                elif analytics_choice == "4":                               # If the user chooses to view the longest run streak of one habit
                    print("Choose one habit to see the longest run streak.")
                    habit_m.view_habits()                                   # View all habits
                    analytics.run_streak_one()                              # Call the run_streak_one function from the analytics module
                elif analytics_choice == "5":                               # If the user chooses to view the longest streak out of all habits
                    print("Longest streak out of all habits:")
                    analytics.longest_run_streak_out_of_all_habits()        # Call the longest_run_streak_out_of_all_habits function from the analytics module
                elif analytics_choice == "6":
                    continue
                else:
                        print("Invalid choice. Please try again.")
            else:
                continue  

            
        elif choice == "4":                                             # If the user chooses the predefined habits menu option
            while True:                                                 # Loop until a valid choice is entered
                password = input("Enter the admin password: ")          # Ask for the admin password
                if password != "admin":                                 # Check if the password is not admin                
                    print("Invalid password. Access denied.")           
                    break
                while True:                                             # Loop until a valid choice is entered   
                    predefined_habit_menu()
                    choice = input("Enter your choice: ")
                    if choice == "1":                                # If the user chooses to insert predefined habits
                        habit_m.insert_predefined_habits()          # Call the insert_predefined_habits function from the HabitManager class
                        break
                    elif choice == "2":                             # If the user chooses to delete predefined habits
                        habit_m.delete_predefined_habits()          # Call the delete_predefined_habits function from the HabitManager class
                        break
                    elif choice == "3":
                        break
                    else:
                        print("Invalid choice. Please try again.")
                break

        elif choice == "5":                 # If the user chooses to exit
            database.close()                # Close the database connection
            break                           # Exit the application
        else:
            print("Invalid choice. Please try again.")   