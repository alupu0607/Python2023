import Validator as v  

if __name__ == "__main__":
    file_path = "example.csv"

    rules = {
        'check_missing_values': None,
        'check_data_types': {'Age': int, 'Salary': float}
    }

    csv_validator = v.CSVValidator(file_path)

    results = csv_validator.validate(rules)

    for rule, result in results.items():
        print(f"{rule}: {'Failed' if result else 'Passed'}")
