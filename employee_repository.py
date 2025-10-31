# employee_repository.py
import requests

class EmployeeRepository:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_employees(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            employees = response.json()
            # Sort by ID before returning
            return sorted(employees, key=lambda x: x["id"])
        else:
            raise Exception(f"Failed to fetch employees: {response.status_code}")
