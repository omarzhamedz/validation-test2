import unittest
from unittest.mock import patch, MagicMock
from employee_repository import EmployeeRepository

class TestEmployeeRepository(unittest.TestCase):
    
    @patch('employee_repository.requests.get')
    def test_get_employees_success(self, mock_get):
        """✅ Test successful retrieval and sorting of employees"""
        # --- Mock Data ---
        mock_data = [
            {"id": 3, "name": "Alice", "position": "Developer"},
            {"id": 1, "name": "Bob", "position": "Manager"},
            {"id": 2, "name": "Charlie", "position": "Designer"}
        ]

        # --- Mock Response Setup ---
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        # --- Test Logic ---
        repo = EmployeeRepository("https://fakeapi.com/employees")
        employees = repo.get_employees()

        # --- Assertions ---
        self.assertEqual(len(employees), 3)
        self.assertEqual(employees[0]["name"], "Bob")
        self.assertEqual(employees[1]["name"], "Charlie")
        self.assertEqual(employees[2]["name"], "Alice")

        # Ensure sorting by ID
        ids = [emp["id"] for emp in employees]
        self.assertEqual(ids, sorted(ids))

    @patch('employee_repository.requests.get')
    def test_get_employees_error_response(self, mock_get):
        """❌ Test API returning non-200 status"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        repo = EmployeeRepository("https://fakeapi.com/employees")

        with self.assertRaises(Exception) as context:
            repo.get_employees()

        self.assertIn("Failed to fetch employees", str(context.exception))

    @patch('employee_repository.requests.get')
    def test_employees_sorting_only(self, mock_get):
        """🔢 Test that sorting logic works independently"""
        mock_data = [
            {"id": 10, "name": "Zoe"},
            {"id": 5, "name": "Adam"},
            {"id": 8, "name": "Liam"}
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        repo = EmployeeRepository("https://fakeapi.com/employees")
        employees = repo.get_employees()

        sorted_ids = [5, 8, 10]
        self.assertEqual([emp["id"] for emp in employees], sorted_ids)

if __name__ == '__main__':
    unittest.main()
