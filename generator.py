from random import choice
import string


def generate_password(length: int) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(choice(characters) for _ in range(length))

    return password


if __name__ == "__main__":
    print(generate_password(16))
