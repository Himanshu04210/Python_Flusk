def average_age_of_employees_with_s_job_title(company):
    # Initialize variables
    total_age = 0
    count = 0
    
    for employee in company['employees'].values():
        job_title = employee['job_title']
  
        if job_title.startswith('S'):
            total_age += employee['age']
            count += 1
    
    # Calculate the average age
    if count > 0:
        average_age = total_age / count
        return average_age
    else:
        return 0

# Test the function
company = {
    'employees': {
        'John': {'age': 35, 'job_title': 'Manager'},
        'Emma': {'age': 28, 'job_title': 'Software Engineer'},
        'Kelly': {'age': 41, 'job_title': 'Senior Developer'},
        'Sam': {'age': 30, 'job_title': 'Software Engineer'},
        'Mark': {'age': 37, 'job_title': 'Senior Manager'},
        'Sara': {'age': 32, 'job_title': 'Software Engineer'},
    }
}

print(average_age_of_employees_with_s_job_title(company))