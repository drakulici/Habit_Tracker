# tests/test_database.py
import unittest
from unittest.mock import patch, MagicMock
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Patch sqlite3.connect so no real DB file is created
        patcher = patch('database.sqlite3.connect')
        self.mock_connect = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Instantiate Database (which will use the mocked connect)
        self.db = Database()

    def test_get_database_name(self):
        self.assertEqual(self.db.get_database_name(), "database.db")

    def test_create_tables(self):
        self.db.create_tables()
        # Check that two CREATE TABLE statements were executed
        calls = [call[0][0].lower() for call in self.mock_cursor.execute.call_args_list]
        self.assertIn("create table if not exists habits", calls[0])
        self.assertIn("create table if not exists completed_dates", calls[1])
        self.mock_conn.commit.assert_called_once()

    def test_get_all_tables(self):
        # Mock return value for get_all_tables
        self.mock_cursor.fetchall.return_value = [("habits",), ("completed_dates",)]
        tables = self.db.get_all_tables()
        self.mock_cursor.execute.assert_called_with("SELECT name FROM sqlite_master")
        self.assertEqual(tables, [("habits",), ("completed_dates",)])

    def test_get_method(self):
        # Mock return value for get
        self.mock_cursor.fetchall.return_value = [("habit1",), ("habit2",)]
        result = self.db.get("habits", "name")
        self.mock_cursor.execute.assert_called_once_with("SELECT name FROM habits")
        self.assertEqual(result, [("habit1",), ("habit2",)])

    def test_get_all_data_from_habit_table(self):
        # Mock return value
        self.mock_cursor.fetchall.return_value = [(1, "Run", "desc", "daily", "2024-01-01")]
        result = self.db.get_all_data_from_habit_table()
        self.mock_cursor.execute.assert_called_with("SELECT * FROM habits")
        self.assertEqual(result, [(1, "Run", "desc", "daily", "2024-01-01")])

    def test_get_all_data_from_completed_dates_table(self):
        self.mock_cursor.fetchall.return_value = [(1, 2, "2024-01-02")]
        result = self.db.get_all_data_from_completed_dates_table()
        self.mock_cursor.execute.assert_called_with("SELECT * FROM completed_dates")
        self.assertEqual(result, [(1, 2, "2024-01-02")])

    def test_insert_habits(self):
        data = [("Run", "desc", "daily", "2024-01-01")]
        self.db.insert("habits", data)
        self.mock_cursor.executemany.assert_called_once_with(
            "INSERT INTO habits (name, description, frequency, created_date) VALUES (?,?,?,?)", data
        )
        self.mock_conn.commit.assert_called()

    def test_insert_completed_dates(self):
        data = [(1, "2024-01-01 10:00:00")]
        self.db.insert("completed_dates", data)
        self.mock_cursor.executemany.assert_called_once_with(
            "INSERT INTO completed_dates (habit_id, completed_date) VALUES (?,?)", data
        )
        self.mock_conn.commit.assert_called()

    def test_count_habits(self):
        self.mock_cursor.fetchone.return_value = (5,)
        count = self.db.count_habits()
        self.mock_cursor.execute.assert_called_with("SELECT COUNT(*) FROM habits")
        self.assertEqual(count, 5)

    def test_get_all_names(self):
        self.mock_cursor.fetchall.return_value = [("Run",), ("Read",)]
        names = self.db.get_all_names()
        self.mock_cursor.execute.assert_called_with("SELECT name FROM habits")
        self.assertEqual(names, [("Run",), ("Read",)])

    def test_close(self):
        self.db.close()
        self.mock_conn.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()