# test_habit_manager.py

import unittest
from unittest.mock import patch, MagicMock
from habit_manager import HabitManager

class TestHabitManager(unittest.TestCase):
    @patch('habit_manager.Habit')
    @patch('habit_manager.Database')
    def test_add_habit(self, mock_db, mock_habit):
        """
        Test add_habit calls Habit constructor and save on the created Habit instance.
        """
        hm = HabitManager()
        hm.add_habit("Run", "Run 5km", "daily", "2024-01-01")
        # Check Habit was called with correct arguments
        mock_habit.assert_called_once_with("Run", "Run 5km", "daily", "2024-01-01")
        # Check save was called on the Habit instance
        mock_habit.return_value.save.assert_called_once()

    @patch('builtins.print')
    @patch('habit_manager.Database')
    def test_view_habits(self, mock_db, mock_print):
        """
        Test view_habits fetches habits from DB and prints them.
        """
        mock_db_inst = MagicMock()
        mock_db.return_value = mock_db_inst
        mock_db_inst.get.return_value = [(1, "Run"), (2, "Read")]

        hm = HabitManager()
        hm.view_habits()

        mock_db_inst.get.assert_called_once_with("habits", "id, name")
        printed_lines = [args[0] for args, _ in mock_print.call_args_list]
        self.assertIn("1.Run", printed_lines)
        self.assertIn("2.Read", printed_lines)

    @patch('habit_manager.Habit')
    @patch('habit_manager.Database')
    def test_mark_habit_completed(self, mock_db, mock_habit):
        """
        Test mark_habit_completed creates a Habit instance and calls mark_completed.
        """
        hm = HabitManager()
        hm.mark_habit_completed(10)
        mock_habit.assert_called_once_with(name=None, description=None, frequency=None, created_date=None)
        mock_habit.return_value.mark_completed.assert_called_once_with(10)

    @patch('habit_manager.Habit')
    @patch('habit_manager.Database')
    def test_delete_habit(self, mock_db, mock_habit):
        """
        Test delete_habit creates a Habit instance and calls delete.
        """
        hm = HabitManager()
        hm.delete_habit(5)
        mock_habit.assert_called_once_with(name=None, description=None, frequency=None, created_date=None)
        mock_habit.return_value.delete.assert_called_once_with(5)

    @patch('habit_manager.Predefined_data')
    @patch('habit_manager.Database')
    def test_insert_predefined_habits(self, mock_db, mock_predef):
        """
        Test insert_predefined_habits calls insert_data and insert_completed_dates on Predefined_data.
        """
        hm = HabitManager()
        hm.insert_predefined_habits()
        # Check that a Predefined_data instance was created
        mock_predef.return_value.insert_data.assert_called_once()
        mock_predef.return_value.insert_completed_dates.assert_called_once()

    @patch('habit_manager.Predefined_data')
    @patch('habit_manager.Database')
    def test_delete_predefined_habits(self, mock_db, mock_predef):
        """
        Test delete_predefined_habits calls delete_data on Predefined_data.
        """
        hm = HabitManager()
        hm.delete_predefined_habits()
        mock_predef.return_value.delete_data.assert_called_once()

if __name__ == "__main__":
    unittest.main()