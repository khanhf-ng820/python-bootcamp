import csv
from datetime import date
from models import Task  # Import the Task class from models.py

def load_tasks(path: str) -> list[Task]:
    tasks = []  # Initialize an empty list to store tasks
    
    # Open the file safely
    with open(path, mode='r', encoding='utf-8') as file:
        # Read the CSV file, using the first row as headers
        reader = csv.DictReader(file)
        
        # Loop through each row, starting at line 2
        for line_num, row in enumerate(reader, start=2):
            try:
                # Create a Task object from the current row
                task = Task(
                    title=row['title'],
                    importance=int(row['importance']),
                    effort_h=float(row['effort_h']),
                    deadline=date.fromisoformat(row['deadline'])
                )
                tasks.append(task)  # Add the task to the list
            except Exception as e:
                # Raise an error with the line number if parsing fails
                raise ValueError(f"Error at line {line_num}: {e}")
                
    return tasks