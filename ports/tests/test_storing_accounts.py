from bank_account import BankAccount
from ports import account_storage


def test_can_retrieve_account():
    account = account_storage.retrieve()
    assert not account


def test_can_retrieve_previously_opened_account():
    stored_account = BankAccount()
    stored_account.open()
    account_storage.store(stored_account)

    retrieved_account = account_storage.retrieve()

    assert stored_account.balance == retrieved_account.balance
