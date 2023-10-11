# Write a script that converts a string of characters written in UpperCamelCase 
# into lowercase_with_underscores.


def convert(input_string):
    if input_string.find('_')!= -1 or not input_string[0].isupper():
        return "The input is not in UpperCamelCase"
 
    result_string = ''

    for char in input_string:
        if char.isupper():
            result_string += '_' + char.lower()
        else:
            result_string += char
    if result_string.startswith('_'):
        result_string = result_string[1:]

    return result_string


input_string = input("Enter a string in UpperCamelCase ")
converted_string = convert(input_string)
print(converted_string)





