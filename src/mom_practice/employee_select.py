from pathlib import Path
from typing import List


class Employee:
    def __init__(self, name: str, employee_id: int, age: int):
        self.name = name
        self.employee_id = employee_id
        self.age = age


def read_names_from_txt(file_path: str):

    path = Path(file_path)
    employees = []

    with path.open(encoding="utf-8") as f:

        for line in f:
            parts = line.strip().split(",")
            name, employee_id, age = parts[0].strip(), parts[1].strip(), parts[2].strip()
            if name:
                employees.append(Employee(name, int(employee_id), int(age)))
    return employees


def sort_list(list: List[str]):
    return sorted(list)

def employee_exist(list: List[str], name: str):
    return name in list

employees = read_names_from_txt("employees.txt")


sorted_names = sort_list(employees.name)
print(sorted_names)

selected_name = employee_exist(sorted_names, "James")
print(selected_name)