# Ex1. Write a function to return a list of the first n numbers in the Fibonacci string.
def fibo(n):
    a = 1
    b = 1
    contor =2
    while contor!= n:
        contor+=1
        z = a+b
        a = b
        b = z

    return b
    
ex1 = fibo(5)
print(ex1)



# Ex2. Write a function that receives a list of numbers and returns a list of the prime numbers found in it.
def check_prime(n):
    if n <=1:
        return 0
    elif n==2:
        return 1
    else:
        for i in range(2, int(n**0.5) + 1):
            if n%i ==0: 
                return 0
        return 1

def primes(list):
    primes = []
    for item in list:
        if check_prime(item):
            primes.append(item)
    return primes

ex2 = primes([1,2,3,4,5,6,7,8])
print(ex2)

# Ex3. Write a function that receives as parameters two lists a and b and returns: 
# (a intersected with b, a reunited with b, a - b, b - a)
def list_operations(a, b):
    set_a = set(a)
    set_b = set(b)

    intersection = list(set_a & set_b)
    union = list(set_a | set_b)
    difference_a = list(set_a - set_b)
    difference_b = list(set_b - set_a)

    return intersection, union, difference_a, difference_b

list_a = [1, 2, 3, 4, 5]
list_b = [3, 4, 5, 6, 7]

intersection, union, difference_a, difference_b = list_operations(list_a, list_b)
print("Intersection:", intersection)
print("Union:", union)
print("Difference (a - b):", difference_a)
print("Difference (b - a):", difference_b)

# Ex 4. Write a function that receives as a parameters a list of musical notes (strings), 
# a list of moves (integers) and a start position (integer). 
# The function will return the song composed by going though the musical 
# notes beginning with the start position and following the moves given as parameter. Example :
# compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2) => ["mi", "fa", "do", "sol", "re"]

def compose(musical_notes, moves, start_position):
    composed_song = []
    current_position = start_position

    for move in moves:
        current_position = (current_position + move) % len(musical_notes)
        composed_song.append(musical_notes[current_position])

    return composed_song
notes = ["do", "re", "mi", "fa", "sol"]
moves = [1, -3, 4, 2]
start_position = 2
ex4 = compose(notes, moves, start_position)
print(ex4)

# Ex5. Write a function that receives as parameter a matrix and will 
# return the matrix obtained by replacing all the elements under the main diagonal with 0 (zero).

def matrix(a):
    for i in range(0, len(a)):
        for j in range(0, len(a[i])):
            if i>j:
                a[i][j] = 0
    return a


ex5 = matrix([[1,2,3],[4,5,6],[1,9,3]])
print(ex5)

# Ex6. Write a function that receives as a parameter a variable number of lists and a whole number x. 
# Return a list containing the items that appear exactly x times in the incoming lists. 
# Example: For the [1,2,3], [2,3,4],[4,5,6], [4,1, "test"] and x = 2 lists [1,2,3 ] 
# #1 is in list 1 and 4, 2 is in list 1 and 2, 3 is in lists 1 and 2.

def find_elements(x, *lists):
    d = {} #define a dictionary
    returned_list = []
    for lst in lists:
        for item in lst: 
            if item in d:
                d[item] +=1
            else:
                d[item] =1

    for key,value in d.items():
        if value == x:
            returned_list.append(key)

    return returned_list


ex6 = find_elements(2,[1,2,3], [2,3,4], [4,5,6], [4,1,"test"])
print(ex6)


# Ex7. Write a function that receives as parameter a list of numbers (integers) and 
# will return a tuple with 2 elements. The first element of the tuple will be the number
#  of palindrome numbers found in the list and the second element will be the greatest palindrome number.
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
        
def palindrome(list):
    palindromes = 0
    max_palindrome = -1
    for item in list:
        if check_palindrome(item):
            palindromes+=1
            if max_palindrome < item:
                max_palindrome = item
    return (palindromes, max_palindrome)

ex7 = palindrome([121,333,123,898,413])
print(ex7)
# Ex8. Write a function that receives a number x, default value equal to 1, a list of strings, 
# and a boolean flag set to True. For each string, generate a list containing the characters that
#  have the ASCII code divisible by x if the flag is set to True,
#  otherwise it should contain characters that have the ASCII code not divisible by x. Example:
# x = 2, ["test", "hello", "lab002"], flag = False 
# will return (["e", "s"], ["e"]) . Note: The function must return list of lists.

def generate_character_lists(x=1, strings=[], flag=True):
    result = []
    for string in strings:
        char_list = []

        for char in string:
            ascii_code = ord(char)
            
            if (ascii_code % x == 0 and flag) or (ascii_code % x != 0 and not flag):
                char_list.append(char)

        result.append(char_list)

    return result


output = generate_character_lists(2, ["test", "hello", "lab002"], False)
print(output)

# Ex9. Write a function that receives as paramer a matrix which represents the heights of the
#  spectators in a stadium and will return a list of tuples (line, column) each one representing a
#  seat of a spectator which can't see the game. A spectator can't see the game if there is at least
#  one taller spectator standing in front of him. All the seats are occupied. All the seats are at the
#  same level. Row and column indexing starts from 0, beginning with the closest row from the field. 
# Example:
# FIELD
#[[1, 2, 3, 2, 1, 1],
# [2, 4, 4, 3, 7, 2],
# [5, 5, 2, 5, 6, 4],
# [6, 6, 7, 6, 7, 5]] 
# Will return : [(2, 2), (2, 4)]

def spectators(matrix):
    list_spectators = []
    for i in range (1,len(matrix)):
        for j in range (0,len(matrix[i])):
            if matrix[i][j] <= matrix[i-1][j]:
                list_spectators.append((i,j))
    return list_spectators

ex9 = spectators([[1, 2, 3, 2, 1, 1],[2, 4, 4, 3, 7, 2], [5, 5, 2, 5, 6, 4],[6, 6, 7, 6, 7, 5] ])
print(ex9)
# Ex10. Write a function that receives a variable number of lists and returns a
# list of tuples as follows: the first tuple contains the first items in the lists,
# the second element contains the items on the position 2 in the lists, etc. 
# Example: for lists [1,2,3], [5,6,7], ["a", "b", "c"]
# return: [(1, 5, "a ") ,(2, 6, "b"), (3,7, "c")]. 
# Note: If input lists do not have the same number of items, 
# missing items will be replaced with None
# to be able to generate max ([len(x) for x in input_lists]) tuples.
def combine_lists(*args):
    max_len = max(len(lst) for lst in args)
    result = []

    for i in range(max_len):
        items = [lst[i] if i < len(lst) else None for lst in args]
        result.append(tuple(items))

    return result


combined = combine_lists([1,2,3,8], [5,6,7], ["a", "b", "c"])
print(combined)


# Ex11. Write a function that will order a list of string tuples based
#  on the 3rd character of the 2nd element in the tuple. Example:
# ('abc', 'bcd'), ('abc', 'zza')] ==> [('abc', 'zza'), ('abc', 'bcd')]

def order(lst):
    # item[1] => al 2lea element din tuplu,  item[1][2] => al 3lea caracter din al doilea el din tuplu
    return lst.sort(key=lambda item: item[1][2] if len(item[1]) >= 3 else item[1]) 

ex11 = [('abc', 'bcd'), ('abc', 'zza')]
order(ex11)
print(ex11)


# Ex12. Write a function that will receive a list of words as parameter
#  and will return a list of lists of words, grouped by rhyme. 
# Two words rhyme if both of them end with the same 2 letters.
#  Example: group_by_rhyme(['ana', 'banana', 'carte', 'arme', 'parte']) 
# will return [['ana', 'banana'], ['carte', 'parte'], ['arme']]
def group_by_rhyme(list):
    d = {}
    for item in list:
        last_two_chars= item[-2:]
        if last_two_chars in d:
            d[last_two_chars].append(item)
        else:
            d[last_two_chars] = [item]

    return d.values()
        

ex12 = group_by_rhyme(['ana', 'banana', 'carte', 'arme', 'parte'])
print(ex12)