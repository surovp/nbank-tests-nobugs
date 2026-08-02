import random
from faker import Faker

faker = Faker()


class RandomData:
    @staticmethod
    def get_username() -> str:
        return ''.join(faker.random_letters(length=random.randint(3, 15)))

    @staticmethod
    def get_password() -> str:
        upper = [letter.upper() for letter in faker.random_letters(length=3)]
        lower = [letter.lower() for letter in faker.random_letters(length=3)]
        digits = [str(faker.random_digit()) for _ in range(3)]
        special = [random.choice('!@#$%^&')]
        password = upper + lower + digits + special
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def get_deposit_amount() -> float:
        return faker.pyfloat(min_value=0.01, max_value=5000.00, right_digits=2)

    @staticmethod
    def get_invalid_deposit_amount() -> float:
        return faker.pyfloat(min_value=5000.01, max_value=100000.00, right_digits=2)

    @staticmethod
    def negative_number() -> float:
        return faker.pyfloat(min_value=-5000.00, max_value=-0.01, right_digits=2)

    @staticmethod
    def get_invalid_account_id() -> int:
        invalid_id = [
            lambda: faker.random_int(-100, -1),
            lambda: faker.random_int(100000, 999999)
        ]
        return random.choice(invalid_id)()
