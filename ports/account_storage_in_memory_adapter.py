from typing import Optional

from bank_account import BankAccount

_account: Optional[BankAccount] = None


def store(account: BankAccount):
    global _account
    _account = account


def retrieve() -> Optional[BankAccount]:
    return _account
