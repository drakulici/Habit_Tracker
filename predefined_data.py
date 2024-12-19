
"""
This module manages predefined habit data for the habit tracker application.
Class Predefined_data is defined to insert predefined habits into the database, 
add their corresponding completion dates, and delete them when necessary. 
"""

from datetime import datetime, timedelta
from database import Database


class Predefined_data():
    def __init__(self):
        """
        Initializes the Predefined_data class with predefined habits.
        It creates lists of daily and weekly habits, each with a starting date of four weeks ago.
        The habits are stored in the 'self.data' attribute as a combined list.
        """
        date_four_weeks_ago = (datetime.now() - timedelta(weeks=4)).strftime("%Y-%m-%d %H:%M:%S")
        daily_data = [                      # List of daily habits
            ("Drink water *predefined*", "Drink 2 glasses of water in the morning", "daily",date_four_weeks_ago),
            ("Read *predefined*", "Read 10 pages of a book", "daily", date_four_weeks_ago),
            ("Exercise *predefined*", "Do 10 pushups", "daily", date_four_weeks_ago),
            ("Meditate *predefined*", "Meditate for 10 minutes", "daily", date_four_weeks_ago)
        ]

        weekly_data = [                     # List of weekly habits
            ("Grocery shopping *predefined*", "Buy groceries for the week", "weekly", date_four_weeks_ago),
            ("Laundry *predefined*", "Do laundry", "weekly", date_four_weeks_ago),
            ("Clean house *predefined*", "Clean the house", "weekly", date_four_weeks_ago)
        ]
        
        self.data = daily_data + weekly_data

    def insert_data(self):
        """
        Inserts the predefined habits into the 'habits' table in the database.

        It creates an instance of the Database class and uses the 'insert' method
        to add the predefined habits stored in 'self.data' to the database.
        """
        db = Database()
        db.insert("habits", self.data)
        print("\nData inserted into the database.")

    def insert_completed_dates(self):
        """
        Inserts completion dates for the predefined habits into the 'completed_dates' table.
        For each predefined habit, it checks the frequency:
        - If the habit is daily, it inserts completion dates for the last 28 days.
        - If the habit is weekly, it inserts completion dates for the last 4 weeks.

        This method ensures that the predefined habits have historical completion data.
        """
        db = Database()
        habits = db.get_all_data_from_habit_table() # Get all habits from the habit table
        for habit in habits:                        # Loop through all habits
            habit_id = habit[0]                     # Get the id of the habit
            habit_name = habit[1]                   # Get the name of the habit
            frequency = habit[3]                    # Get the frequency of the habit
            if "*predefined*" in habit_name:
                if frequency == "daily":                 # If the habit is daily
                    for i in range(28):                  # Insert completed dates for the last 28 days
                        completed_date = datetime.now() - timedelta(days=i) # Get the date i days ago
                        completed_date_strf = completed_date.strftime("%Y-%m-%d %H:%M:%S")
                        data = [(habit_id, completed_date_strf)] # Create a tuple with the habit_id and the completed_date
                        db.insert("completed_dates", data) # Insert the data into the completed_dates table
                elif frequency == "weekly":                                   # If the habit is weekly
                    for i in range(1, 5):               # Insert completed dates for the last 4 weeks
                        completed_date = datetime.now() - timedelta(weeks=i) # Get the date i weeks ago
                        completed_date_strf = completed_date.strftime("%Y-%m-%d %H:%M:%S")
                        data = [(habit_id, completed_date_strf)] # Create a tuple with the habit_id and the completed_date
                        db.insert("completed_dates", data) # Insert the data into the date_completed table
        print("\nCompleted dates inserted into the database.") # Print a message that the completed dates have been inserted

    def delete_data(self):
        """
        Deletes all predefined habits from the 'habits' table in the database.

        It removes any habit whose name contains '*predefined*' to distinguish them
        from user-created habits. This helps in resetting or cleaning up the database.
        """
        db = Database()
        db.cursor.execute("DELETE FROM habits WHERE name LIKE '%*predefined*%'")
        db.connection.commit()
        print("\nPredefined data deleted from the database.")
