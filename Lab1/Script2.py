#Write a script that calculates how many vowels are in a string.

def calculate_vowels(input_string):
    number_of_vowels = 0
    input_string = input_string.lower()

    for char in input_string:
        if char in 'aeiou':
            number_of_vowels += 1

    return number_of_vowels

user_input = input("Enter a string: ")
result = calculate_vowels(user_input)
print("Number of vowels in the input:", result)
