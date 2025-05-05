import random

def generate_unique_11_digit_numbers(n):
    numbers = set()
    while len(numbers) < n:
        number = random.randint(10_000_000_000, 99_999_999_999)  # Ensures 11-digit numbers
        numbers.add(number)

    return list(numbers)
