import sys
import threading
import time
import unittest

import pytest

from bank_account import BankAccount


class BankAccountTest(unittest.TestCase):
    def test_newly_opened_account_has_zero_balance(self):
        account = BankAccount()

        account.open()

        self.assertEqual(account.get_balance(), 0)

    def test_can_deposit_money(self):
        account = self._create_account(amount=100)

        self.assertEqual(account.get_balance(), 100)

    def test_can_deposit_money_sequentially(self):
        account = self._create_account(amount=100)
        account.deposit(50)

        self.assertEqual(account.get_balance(), 150)

    def test_can_withdraw_money(self):
        account = self._create_account(amount=100)

        account.withdraw(50)

        self.assertEqual(account.get_balance(), 50)

    def test_can_empty_bank_account(self):
        account = self._create_account(amount=100)

        account.withdraw(100)

        self.assertEqual(account.get_balance(), 0)

    def test_can_withdraw_money_sequentially(self):
        account = self._create_account(amount=100)

        account.withdraw(20)
        account.withdraw(70)

        self.assertEqual(account.get_balance(), 10)

    def test_checking_balance_of_closed_account_throws_error(self):
        account = BankAccount()
        account.open()

        account.close()

        with self.assertRaisesWithMessage(ValueError):
            account.get_balance()

    def test_deposit_into_closed_account_raises(self):
        account = BankAccount()
        account.open()
        account.close()

        with self.assertRaisesWithMessage(ValueError):
            account.deposit(50)

    def test_withdraw_from_closed_account_raises(self):
        account = BankAccount()
        account.open()
        account.close()

        with self.assertRaisesWithMessage(ValueError):
            account.withdraw(50)

    def test_close_already_closed_account_raises(self):
        account = BankAccount()

        with self.assertRaisesWithMessage(ValueError):
            account.close()

    def test_open_already_opened_account_raises(self):
        account = BankAccount()
        account.open()

        with self.assertRaisesWithMessage(ValueError):
            account.open()

    def test_reopened_account_does_not_retain_balance(self):
        account = self._create_account(amount=50)
        account.close()

        account.open()

        self.assertEqual(account.get_balance(), 0)

    def test_cannot_withdraw_more_than_deposited(self):
        account = self._create_account(amount=25)

        with self.assertRaises(ValueError):
            account.withdraw(50)

    def test_cannot_withdraw_negative(self):
        account = self._create_account(amount=100)

        with self.assertRaisesWithMessage(ValueError):
            account.withdraw(-50)

    def test_cannot_deposit_negative(self):
        account = BankAccount()
        account.open()

        with self.assertRaisesWithMessage(ValueError):
            account.deposit(-50)

    def test_can_handle_concurrent_transactions(self):
        account = self._create_account(amount=100)

        self._adjust_balance_concurrently(account)

        self.assertEqual(account.get_balance(), 100)

    def test_can_handle_initial_dollar_amount(self):
        account = BankAccount()

        account.open(amount=50)

        self.assertEqual(account.get_balance(), 50)

    def test_able_to_open_account_with_minimum_required_balance(self):
        account = BankAccount(minimum_balance=100)

        self.assertEqual(account.minimum_balance, 100)

    # Utility functions
    @staticmethod
    def _adjust_balance_concurrently(account):
        def transact():
            account.deposit(5)
            time.sleep(0.001)
            account.withdraw(5)

        # Greatly improve the chance of an operation being interrupted
        # by thread switch, thus testing synchronization effectively
        try:
            sys.setswitchinterval(1e-12)
        except AttributeError:
            # For Python 2 compatibility
            sys.setcheckinterval(1)

        threads = [threading.Thread(target=transact) for _ in range(1000)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def assertRaisesWithMessage(self, exception):
        return self.assertRaisesRegex(exception, r".+")

    @staticmethod
    def _create_account(amount):
        account = BankAccount()
        account.open()
        account.deposit(amount)
        return account


@pytest.mark.parametrize("minimum_balance,amount", [(100, 50), (50, 0), (1, 0)])
def test_cannot_open_account_with_less_than_minimum_balance(minimum_balance, amount):
    account = BankAccount(minimum_balance=minimum_balance)

    with pytest.raises(
        ValueError,
        match=f"Opening requires at least minimum balance of {minimum_balance}",
    ):
        account.open(amount=amount)


def test_account_requires_minimum_balance_of_at_least_zero():
    with pytest.raises(ValueError, match="Minimum balance must be at least zero"):
        BankAccount(minimum_balance=-15)

def test_withdraw_below_minimum_balance_raises():
    account = BankAccount(minimum_balance=1)
    account.open(amount=3)

    with pytest.raises(ValueError, match="Cannot withdraw below minimum required balance of 1. You can withdraw a maximum of 2."):
        account.withdraw(amount=3)
