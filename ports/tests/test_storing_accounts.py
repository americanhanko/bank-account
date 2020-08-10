from bank_account import BankAccount
from ports import account_storage


def test_can_store_an_account_fine():
    account = BankAccount()
    account_storage.store(account)


def test_can_retrieve_account():
    account = account_storage.retrieve()
    assert account
