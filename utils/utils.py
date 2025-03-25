import random
import string

def generate_reference(length=7, min_numbers=2):
    """
    Generates a random string with:
    - Uppercase letters (A-Z)
    - Lowercase letters (a-z)
    - At least 2 numbers (0-9)
    - Total length of 7 characters
    
    Args:
        length (int): Total length of string (default: 7)
        min_numbers (int): Minimum numbers required (default: 2)
    
    Returns:
        str: Random mixed string
    
    Raises:
        ValueError: If min_numbers > length
    """
    # Input validation
    if min_numbers > length:
        raise ValueError(f"Can't have {min_numbers} numbers in a {length}-character string")
    
    # 1. Generate required numbers
    numbers = [random.choice(string.digits) for _ in range(min_numbers)]
    
    # 2. Generate remaining characters as letters
    letters = [random.choice(string.ascii_letters) for _ in range(length - min_numbers)]
    
    # 3. Combine and shuffle
    all_chars = numbers + letters
    random.shuffle(all_chars)
    
    # 4. Return as string
    return ''.join(all_chars)

