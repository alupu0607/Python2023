# Build an employee hierarchy with a base class Employee. Create subclasses for different 
# types of employees like Manager, Engineer, and Salesperson. Each subclass should have attributes 
# like salary and methods related to their roles.


class Employee():
    def __init__(self, name, surname, level, employee_id, salary):
        self.name = name
        self.surname = surname
        self.level = level
        self.employee_id = employee_id
        self.salary = salary
       
        
        
    def get_salary(self):
        return self.salary


class Manager(Employee):
    def __init__(self, name, surname, level,  employee_id, salary,  team):
        super().__init__(name, surname, level, employee_id, salary)
        self.team = team

    def manage_team(self):
        print(f"{self.name} {self.surname} is managing the team {self.team}.")

class Engineer(Employee):
    def __init__(self, name, surname, level, employee_id, salary, team,  specialization):
        super().__init__(name, surname, level, employee_id, salary)
        self.team = team
        self.specialization = specialization
    def print_specialization(self):
        print(f"{self.name} {self.surname} is a {self.level} enginner specialized in {self.specialization}.")

class SalesPerson(Employee):
    def __init__(self, name, surname, level, employee_id, salary, years_in_company, number_of_sales_per_year):
        super().__init__(name, surname, level, employee_id, salary)
        self.years_in_company = years_in_company
        self.number_of_sales_per_year = number_of_sales_per_year
    def print_number_of_sales_per_year(self):
        last_sale = self.number_of_sales_per_year[-1] if self.number_of_sales_per_year else 0
        print(f"{self.name} {self.surname} is a sales person with {last_sale} sales this year")


manager = Manager("John", "Doe", "Manager", "M001", 80000, "Marketing Team")
print(manager.get_salary())  
manager.manage_team()

engineer = Engineer("Alice", "Smith", "Senior", "E001", 70000, "Engineering Team", "Software Development")
print(engineer.get_salary())  
engineer.print_specialization()

salesperson = SalesPerson("Bob", "Johnson", "Executive", "S001", 90000, 3, [10, 20, 30, 40])
print(salesperson.get_salary()) 
salesperson.print_number_of_sales_per_year()