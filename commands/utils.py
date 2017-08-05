import random

import os


def generate_random_key(length=50, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"):
    rng = random.SystemRandom()
    return ''.join(rng.choice(allowed_chars) for _ in range(length))


def prompt_for(question, implicit_yes=True):
    if implicit_yes:
        print(question + " [Y/n]")
        choice = input().lower()
        if choice.startswith("n"):
            return False
        return True
    else:
        print(question + " [y/N]")
        choice = input().lower()
        if choice.startswith("y"):
            return True
        return False


def valid_input_for(query, on_fail="Please try again: ", is_valid=lambda x: x != ""):
    message = query
    while True:
        print(message, end="")
        x = input()
        if is_valid(x):
            break
        message = on_fail
    return x


def is_sudo():
    return os.getuid() == 0
