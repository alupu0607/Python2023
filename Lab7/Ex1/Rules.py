def check_missing_values(row):
    return any(value == '' for value in row)

def check_data_types(row, column_types):
    for column, expected_type in column_types.items():
        value = row.get(column)
        if value is not None and not isinstance(value, expected_type):
            return False
    return True
