import csv

data = [
    ['Name', 'Age', 'Salary'],
    ['John', 25, 50000.0],
    ['Jane', 30, 60000.0],
    ['Bob', 28, 70000.0],
]

file_path = './example.csv'
with open(file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(data)

print(f'CSV file "{file_path}" created successfully.')
