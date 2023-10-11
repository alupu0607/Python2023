import math
import re 
def calculate_gcd(numbers):
    if len(numbers) == 0:
        return None 
    elif len(numbers) == 1:
        return numbers[0] 

    gcd_result = int(numbers[0])
    for number in numbers[1:]:
        gcd_result = math.gcd(gcd_result, int(number))
    return gcd_result

def read_numbers_from_console():
    numbers = []
    while True:
        try:
            user_input = input("Enter numbers or 'done' to finish ")
            if user_input.lower() == 'done':
                break 
            number = int(user_input)
            numbers.append(number)
        except ValueError:
            print("Exception. Please enter a valid number or 'done' to finish ")
    return numbers


# Ex 1. Find The greatest common divisor of multiple numbers read from the console.
def ex1():
    numbers = read_numbers_from_console()
    result = calculate_gcd(numbers)
    return result
result1 = ex1() 
if result1 is not None:
    print("GCD of entered numbers:", result1)
else:
    print("No numbers entered.")


#Ex 5. Given a square matrix of characters write a script that prints the string obtained by going through the matrix in spiral order (as in the example):
#firs      1  2  3  4    =>   first_python_lab
#n_lt      12 13 14 5
#oba_      11 16 15 6
#htyp      10 9  8  7

def spiral_order(matrix):
    result = []
    while matrix:
        result += matrix[0]
        matrix = matrix[1:] # delete first row 

        if matrix and matrix[0]:
            for row in matrix:
                result.append(row[-1]) #row[0] is the first element in a row
            matrix = [row[:-1] for row in matrix]

        if matrix:
            result += matrix[-1][::-1]  #matrix[-1] is the last row
            # [::-1] is a slicing technique that reverses the order of elements in a list.
            #  So, matrix[-1][::-1] gives you the last row of the matrix reversed.
            matrix = matrix[:-1]

        if matrix and matrix[0]:
            for row in matrix[::-1]: #the first row reversed
                result.append(row[0]) #only take the first element
            matrix = [row[1:] for row in matrix]

    return ''.join(result) #return an actual string, not a list

matrix = [
    ['f', 'i', 'r', 's'],
    ['n', '_', 'l', 't'],
    ['o', 'b', 'a', '_'],
    ['h', 't', 'y', 'p']
]

result = spiral_order(matrix)
print(result)

#Ex 6. Write a function that validates if a number is a palindrome.
def check_palindrome(input_number):
    input_str = str(input_number)
    length = len(input_str)
    if length % 2 == 0:
        first_half = input_str[:length // 2]   # // this means integer division. the input until that index-1. THE ELEMENT ITSELF IS NOT ADDED
        second_half_reversed = input_str[length // 2:][::-1]
        
        if first_half == second_half_reversed:  # checks equality between two strings
            return True
        else:
            return False
    else:
        first_half = input_str[:length // 2]
        second_half_reversed = input_str[length // 2 + 1:][::-1]
        
        if first_half == second_half_reversed:
            return True
        else:
            return False

input_number = 12321
result = check_palindrome(input_number)
if result:
    print(f"{input_number} is a palindrome.")
else:
    print(f"{input_number} is not a palindrome.")

# Ex 7. Write a function that extract a number from a text
#  (for example if the text is "An apple is 123 USD", this function will return 123,
#  or if the text is "abc123abc" the function will extract 123).
#  The function will extract only the first number that is found.

def find_number(input_string): 
    match = re.search(r'\d+', input_string)
    if match:
        number = int(match.group())
        return number
    else:
        return None


input_string  = "The apple is 123 USD 123"
result_number = find_number(input_string)
if result_number:
    print(f"{result_number} is the first number.")
else:
    print("No numbers")


# Ex 8. Write a function that counts how many bits with value 1 a number has.
#  For example for number 24, the binary format is 00011000, meaning 2 bits with value "1"
def binary_number(input_number):
    result =[]
    while input_number:
        result.append(input_number%2)
        input_number //= 2

    return result.count(1)
input_number  = int("24")
result_binary = binary_number(input_number)
if result_binary:
    print(f"{result_binary} is the number of 1's")
else:
    print("No numbers")


# Ex 9. Write a functions that determine the most common letter in a string.
#  For example if the string is "an apple is not a tomato", 
# then the most common character is "a" (4 times). 
# Only letters (A-Z or a-z) are to be considered. 
# Casing should not be considered "A" and "a" represent the same character.

def letter_frequency (input_string) : 
    frequencies = [0] * 26  # 26 lowercase letters (a to z)
    input_string_lowered = input_string.lower()
    for char in input_string_lowered:
        if 'a' <= char <= 'z':
            frequencies[ord(char) - ord('a')] += 1  #ord gets the unicode 
    max_frequency = max(frequencies) # function to directly retrieve the max in a list
    max_char = chr(frequencies.index(max_frequency) + ord('a'))

    return max_char, max_frequency

input_string_frequency  = "an apple is not a tomato"
max_char, max_frequency = letter_frequency(input_string_frequency)

if max_frequency > 0:
    print(f"The character '{max_char}' has the maximum frequency of {max_frequency}.")
else:
    print("No letters found in the input string.")



# Ex 10 Write a function that counts how many words exists in a text. 
# A text is considered to be form out of words that are separated by only ONE space.
# For example: "I have Python exam" has 4 words.
def count_words(text):
    words = text.split(' ')
    word_count = len(words)
    return word_count
input_text = "I have Python exam"
word_count = count_words(input_text)
print(f"The text has {word_count} words.")