import yaml
from typing import Optional

from bank_account import BankAccount


def store(account: BankAccount):
    with open(file='stored_account.yml', mode='w') as file_account:
        account_exporter = account.__dict__
        del account_exporter['_lock']
        yaml.dump(account_exporter, file_account)

def retrieve() -> Optional[BankAccount]:
    try:
        with open(file='stored_account.yml', mode='r') as file_account:
            account_importer = yaml.load(file_account)
            account = BankAccount()
            account.open()
            account._balance = account_importer['_balance']
            return account
    except FileNotFoundError:
        return None
