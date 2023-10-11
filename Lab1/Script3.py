#Write a script that receives two strings and prints the number of occurrences of the 
#first string in the second.

def calculate_occurences(input_string1, input_string2):
    count = 0
    input_string1 = input_string1.lower()
    input_string2 = input_string2.lower()
    index = input_string2.find(input_string1)
    
    while index != -1:
        count += 1
        index = input_string2.find(input_string1, index + 1)
    
    return count


user_input1 = input("Enter a string 1: ")
user_input2 = input("Enter a string 2: ")
result = calculate_occurences(user_input1, user_input2)
print("Occurences of the first string in the second:", result)
