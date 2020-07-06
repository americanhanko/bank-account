import threading


class BankAccount:
    def __init__(self, minimum_balance=0):
        self._minimum_balance = minimum_balance
        self._balance = 0
        self._opened = False
        self._lock = threading.Lock()

    @property
    def minimum_balance(self):
        return self._minimum_balance

    def get_balance(self):
        self._require_opened()
        return self._balance

    def open(self, amount=0):
        if self._opened:
            raise ValueError('Account already opened')
        self._opened = True
        self._balance = amount

    def deposit(self, amount):
        self._require_opened()
        self._require_positive_transaction_amount(amount)
        self._change_balance(amount)

    def withdraw(self, amount):
        self._require_opened()
        self._require_positive_transaction_amount(amount)
        if self._balance < amount:
            raise ValueError('Cannot overdraw account')
        self._change_balance(-amount)

    @staticmethod
    def _require_positive_transaction_amount(amount):
        if amount < 0:
            raise ValueError('Cannot withdraw negative amount')

    def close(self):
        self._require_opened()
        self._balance = 0
        self._opened = False

    def _change_balance(self, amount):
        with self._lock:
            self._balance += amount

    def _require_opened(self):
        if not self._opened:
            raise ValueError('Requires an opened account')
