
def get_number_of_digits(n : int) -> int:
    if n < 0:   n = -n + 1
    
    if n < 10:  return 1
    elif n < 100:  return 2
    elif n < 1000:  return 3
    elif n < 10000:  return 4
    elif n < 100000:  return 5
    elif n < 1000000:  return 6
    elif n < 10000000:  return 7
    elif n < 100000000:  return 8
    elif n < 1000000000:   return 9
    return 10

def get_indentation(string : str) -> int:
    i = 0
    while i < len(string) and string[i].isspace():
        i += 1
    if i == len(string):
        i = 0
    return i

def is_blank_line(string : str) -> int:
    i = 0
    while i < len(string) and string[i].isspace():
        i += 1
    return i == len(string)