#chatgpt link: https://chatgpt.com/c/66ec6eea-9668-8002-aeba-69c15cd457bb
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def increase_salary(self, percentage):
        increase_amount = self.salary * (percentage / 100)
        self.salary += increase_amount

# Instantiate an Employee object
employee = Employee(name="John", salary=5000)

# Increase salary by 10%
employee.increase_salary(10)

# Print the updated salary
print(f"Updated salary for {employee.name} is: {employee.salary}")
