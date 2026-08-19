from enum import Enum


class BankAlert(str, Enum):
    USER_CREATED_SUCCESSFULLY = "✅ User created successfully!"
    USERNAME_MUST_BE_BETWEEN_3_AND_15_CHARACTERS = "Username must be between 3 and 15 characters"
    NEW_ACCOUNT_CREATED = "✅ New Account Created! Account Number:"

    #deposit page
    SUCCESS_DEPOSIT = "✅ Successfully deposited"
    PLEASE_SELECT_ACCOUNT = "❌ Please select an account."
    PLEASE_ENTER_VALID_AMOUNT = "❌ Please enter a valid amount."

    #transfer page
    SUCCESSFULLY_TRANSFERRED = "✅ Successfully transferred"
    PLEASE_FILL_FIELDS = "❌ Please fill all fields and confirm."
    INVALID_AMOUNT_OR_ACCOUNT = "❌ Error: Invalid transfer: insufficient funds or invalid accounts"
    NO_USER_FOUND_WITH_THIS_ACCOUNT_NUMBER = "❌ No user found with this account number."
    RECIPIENT_NAME_DOESNT_MATCH_THE_REGISTERED_NAME = "❌ The recipient name does not match the registered name."

    #profile page
    NAME_UPDATED_SUCCESSFULLY = "✅ Name updated successfully!"
    PLEASE_ENTER_VALID_NAME = "❌ Please enter a valid name."
    NAME_MUST_CONTAIN_TWO_WORDS_WITH_LETTERS_ONLY = "Name must contain two words with letters only"