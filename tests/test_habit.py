import unittest
from unittest.mock import patch, MagicMock
from habit import Habit

class TestHabit(unittest.TestCase):
    def setUp(self):
        """
        setUp is run before each test method. Here, you can create a Habit instance
        that's reused in test_save, test_delete, and test_mark_completed.
        """
        # Patch the Database class so no actual DB operations occur.
        patcher = patch('habit.Database')
        self.addCleanup(patcher.stop)  # Ensure the patch is stopped after tests
        self.mock_database = patcher.start()
        
        # Mock instance to test calls against
        self.mock_db_instance = MagicMock()
        self.mock_database.return_value = self.mock_db_instance

        # Create a test habit instance that will be used by all tests
        self.habit = Habit(
            name="Test Habit",
            description="A habit used for testing.",
            frequency="daily",
            created_date="2024-01-01 10:00:00"
        )

    def test_save(self):
        """
        Test that calling save() on self.habit inserts the correct data into the database.
        """
        self.habit.save()
        expected_data = [("Test Habit", "A habit used for testing.", "daily", "2024-01-01 10:00:00")]
        self.mock_db_instance.insert.assert_called_once_with("habits", expected_data)

    def test_delete(self):
        """
        Test that calling delete() executes the correct DELETE query.
        """
        habit_id = 1
        self.habit.delete(habit_id)
        self.mock_db_instance.cursor.execute.assert_called_once_with("DELETE FROM habits WHERE id=?", (habit_id,))
        self.mock_db_instance.connection.commit.assert_called_once()

    def test_mark_completed(self):
        """
        Test that calling mark_completed() inserts a record into completed_dates with the correct habit_id.
        """
        habit_id = 2
        self.habit.mark_completed(habit_id)
        # Check that insert was called with 'completed_dates'
        args, _ = self.mock_db_instance.insert.call_args
        table_name = args[0]
        data = args[1][0]
        self.assertEqual(table_name, "completed_dates")
        self.assertEqual(data[0], habit_id)  # Check the habit_id inserted

if __name__ == "__main__":
    unittest.main()