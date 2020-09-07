from typing import Optional

from bank_account import BankAccount
# from ports import account_storage_in_memory_adapter as adapter
from ports import account_storage_file_adapter as adapter


def store(account: BankAccount) -> None:
    adapter.store(account)


def retrieve() -> Optional[BankAccount]:
    return adapter.retrieve()
