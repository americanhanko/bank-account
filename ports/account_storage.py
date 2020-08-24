from typing import Optional

from bank_account import BankAccount
from ports import account_storage_in_memory_adapater as adapter
# from ports import account_storage_sql_database_adapter


def store(account: BankAccount) -> None:
    adapter.store(account)


def retrieve() -> Optional[BankAccount]:
    return adapter.retrieve()
