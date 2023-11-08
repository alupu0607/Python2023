#  Ex1. Write a function that receives as parameters two lists a and b and returns a list of sets 
# containing: (a intersected with b, a reunited with b, a - b, b - a)

def ex1(a,b):
    set_a = set(a)
    set_b = set(b)

    intersection = set(set_a & set_b)
    union = set(set_a | set_b)
    difference_a = set(set_a - set_b)
    difference_b = set(set_b - set_a)

    return [intersection, union, difference_a, difference_b]


ex1 = ex1([1,2,3,4], [1,2,5,6,7])
print(ex1)



# Ex2. Write a function that receives a string as a parameter and returns a dictionary in which the keys 
# are the characters in the character string and the values are the number of occurrences of that 
# character in the given text. Example: For string "Ana has apples." given as a parameter the 
# function will return the dictionary:
#{'a': 3, 's': 2, '.': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 2, ' ': 2, 'A': 1, 'n': 1} .

def ex2 (text):
    d = {}
    for a in text:
        if a in d:
            d[a] +=1
        else:
            d[a] = 1
    return d

ex2 = ex2("Ana has apples")
print(ex2)


# Ex3.  Compare two dictionaries without using the operator "==" returning True or False. 
# (Attention, dictionaries must be recursively covered because they can contain other containers, 
# such as dictionaries, lists, sets, etc.)

def ex3(dict1, dict2):
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return False

    # Check for the same keys
    if set(dict1.keys()) != set(dict2.keys()):
        return False

    for key in dict1.keys():
        value1 = dict1[key]
        value2 = dict2[key]

        if isinstance(value1, dict) and isinstance(value2, dict):
            if not ex3(value1, value2):
                return False
        elif isinstance(value1, list) and isinstance(value2, list):
            if value1 != value2:
                return False
        elif isinstance(value1, set) and isinstance(value2, set):
            if value1 != value2:
                return False
        else:
            if value1 != value2:
                return False

    return True

dict1 = {"a": 1, "b": {"c": [2, 3]}, "d": [4, 5]}
dict2 = {"a": 1, "b": {"c": [3, 3]}, "d": [4, 5]}
dict3 = {"a":{"c": 2}}
result1 = ex3(dict1,dict2)
result2 = ex3(dict1,dict3)
print(result1)
print(result2)


#  Ex4. The build_xml_element function receives the following parameters: tag, content, and
#  key-value elements given as name-parameters. Build and return a string that represents the
#  corresponding XML element. Example: build_xml_element ("a", "Hello there", href =" http://python.org
#  ", _class =" my-link ", id= " someid ") returns the string = "<a href="http://python.org \ "_class =
#  " my-link \ "id = " someid \ "> Hello there "

def build_xml_element(tag, content, **attributes): # ** means that what i have there is a dictrionary
    xml_element = f"<{tag}" # embedding expressions into string-literals
    for key, value in attributes.items():
        xml_element += f' {key}="{value}"'
    xml_element += f">{content}</{tag}>"
    return xml_element

ex4 = build_xml_element("a", "Hello there", href="http://python.org", _class="my-link", id="someid")
print(ex4)



# Ex5. The validate_dict function that receives as a parameter a set of tuples 
# ( that represents validation rules for a dictionary that has strings as keys and values) 
# and a dictionary. A rule is defined as follows: (key, "prefix", "middle", "suffix").
#  A value is considered valid if it starts with "prefix", "middle" is inside the value 
# (not at the beginning or end) and ends with "suffix". The function will return True if 
# the given dictionary matches all the rules, False otherwise. Example: the rules 
# s={("key1", "", "inside", ""), ("key2", "start", "middle", "winter")} and 
# d= {"key1": "come inside, it's too cold out", "key3": "this is not valid"} => 
# False because although the rules are respected for "key1" and "key2" "key3" that 
# does not appear in the rules

def validate_dict(tuples, dictionary):
    for item in tuples:
        key, prefix, middle, suffix = item # destructuring

        if key not in dictionary.keys():
            return False

        value = dictionary[key]

        if prefix and not value.startswith(prefix):
            return False

        if middle and middle not in value[1:-1]:
            return False

        if suffix and not value.endswith(suffix):
            return False

    return True
s={("key1", "", "inside", ""), ("key2", "start", "middle", "winter")}
d= {"key1": "come inside, it's too cold out", "key3": "this is not valid"} 
ex5 = validate_dict(s, d)
print(ex5)



#Ex6. Write a function that receives as a parameter a list and returns a tuple (a, b), 
# representing the number of unique elements in the list, and b representing the number of 
# duplicate elements in the list (use sets to achieve this objective).

def ex6(list):
    unique_set = set()
    duplicate_set = set()
    for item in list:
        if item in unique_set:
            duplicate_set.add(item)
            unique_set.remove(item)
        else:
            unique_set.add(item)
    return (len(unique_set), len(duplicate_set))
ex6 = ex6([1,2,11,1,1,3,4,5])
print(ex6)


# Ex7. Write a function that receives a variable number of sets and returns a dictionary with the 
# following operations from all sets two by two: reunion, intersection, a-b, b-a. The key will 
# have the following form: "a op b", where a and b are two sets, and op is the applied operator
# : |, &, -. 
# Ex:
#{1,2}, {2, 3} =>
#{
#    "{1, 2} | {2, 3}":  {1, 2, 3},
#    "{1, 2} & {2, 3}":  { 2 },
#    "{1, 2} - {2, 3}":  { 1 },
#    ...
#}


def ex7(*sets):
    dictionary = {}
    for i in range(len(sets)):
        for j in range (i+1, len(sets)):
            set1 = sets[i]
            set2 = sets[j]

            intersection = set1 & set2  
            intersection_string = f"{set1}&{set2}"
            dictionary[intersection_string] = intersection

            union = set1 | set2
            union_string = f"{set1}|{set2}"
            dictionary[union_string] = union
            
          
            difference1 = set1 - set2
            difference1_string = f"{set1}-{set2}"
            dictionary[difference1_string] = difference1


            difference2 = set2 - set1
            difference2_string = f"{set2}-{set1}"
            dictionary[difference2_string] = difference2
    return dictionary

ex7 = ex7({1,2}, {2,3})
print(ex7)


#Ex10
# Write a function that receives a single dict parameter named mapping. This dictionary always 
# contains a string key "start". Starting with the value of this key you must obtain a list of 
# objects by iterating over mapping in the following way: the value of the current key is the key 
# for the next value, until you find a loop (a key that was visited before). The function must return 
# the list of objects obtained as previously described. Ex:
# loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'}) will return ['a', '6', 'z', '2']
def ex10(mapping):
    result = []
    visited = set() 
    current_key = "start"

    while current_key in mapping and current_key not in visited:
        visited.add(current_key)
        current_value = mapping[current_key]
        result.append(current_value)
        current_key = current_value
  
    return result[:-1]
ex10  = ex10({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'})
print(ex10)

#Ex11
# Write a function that receives a variable number of positional arguments and a variable number 
# of keyword arguments and will return the number of positional arguments whose values can be found
# among keyword arguments values. 
# Ex: my_function(1, 2, 3, 4, x=1, y=2, z=3, w=5) will return returna 3

def ex11(*args, **kwargs):
    matching_count = 0

    for arg in args:
        if arg in kwargs.values():
            matching_count += 1

    return matching_count
ex11 = ex11(1, 2, 3, 4, x=1, y=2, z=3, w=5)
print(ex11)