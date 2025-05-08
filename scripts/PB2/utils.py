import random
from enum import Enum

def generate_unique_11_digit_numbers(n):
    numbers = set()
    while len(numbers) < n:
        number = random.randint(10_000_000_000, 99_999_999_999)  # Ensures 11-digit numbers
        numbers.add(number)

    return list(numbers)

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    NONE = 4

specified_level = LogLevel.DEBUG

def specify_logging_level(log_level):
    global specified_level
    specified_level = log_level

def log(message, message_level):
    if message_level.value >= specified_level.value:
        if message_level.value ==  LogLevel.WARNING:
            print(f"\033[31m{message}\033[0m")
        else:
            print(message)