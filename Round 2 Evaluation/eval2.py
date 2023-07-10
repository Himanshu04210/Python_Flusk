employees = [
    {"name":"Himanshu", "salary":15000, "designation":"developer"},
    {"name":"Pavan", "salary":13450, "designation":"manager"},
    {"name":"john", "salary":1500, "designation":"tester"},
]

bestEmployee = {"name":"", "salary":0, "designation":"null"}

for employee in employees:
    if employee["salary"] > bestEmployee["salary"] :
        bestEmployee = employee
        
print(bestEmployee)