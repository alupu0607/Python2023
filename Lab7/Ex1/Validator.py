import csv
import Rules as r

class CSVValidator:
    def __init__(self, file_path):
        self.rows = self.read_csv(file_path)

    def read_csv(self, file_path):
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            return list(reader)

    def validate(self, rules):
        validation_results = {}

        for rule, params in rules.items():
            if rule == 'check_missing_values':
                validation_results[rule] = any(r.check_missing_values(row) for row in self.rows)
            elif rule == 'check_data_types':
                column_types = params
                validation_results[rule] = all(r.check_data_types(row, column_types) for row in self.rows)

        return validation_results
