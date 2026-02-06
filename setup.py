import os

# Create directories for the resorces and templates
directories = [
    'templates',
    'resources/rescores/math7Exams',
    'resources/rescores/math8Exams', 
    'resources/rescores/math9Exams',
    'resources/rescores-MathNotes/mathG7',
    'resources/rescores-MathNotes/mathG8',
    'resources/rescores-MathNotes/mathG9'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created: {directory}")

print("\nFolder structure created successfully!")
print("\nNow manually create these files in the templates folder:")
print("1. templates/login.html")
print("2. templates/register.html")  
print("3. templates/dashboard.html")
print("4. templates/subject.html")
print("\nCopy the HTML code I provided into these files.")