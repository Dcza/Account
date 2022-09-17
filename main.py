import pytest


class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def get_owner(self):
        return self.owner

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Negative value")
        else:
            self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("No money")
        elif amount < 0:
            raise ValueError("Negative value")
        else:
            self.balance -= amount

    def transfer_to(self, dst_account, amount):
        if not isinstance(amount, (int, float)):
            raise ValueError("wrong amount type")
        if amount == 0:
            raise ValueError("zero amount")
        if dst_account is self:
            raise ValueError("transfer to itself")
        self.withdraw(amount)
        dst_account.deposit(amount)


class TestAccount:
    def setup(self):
        # Given (part1)
        self.owner = "Jan Kowalski"
        self.account = Account(self.owner, 1000)

    def test_get_owner(self):  # Check if owner is in string type and if it's return same value as we provided
        assert isinstance(self.account.get_owner(), str)
        assert self.account.get_owner() == self.owner

    def test_get_balance(self):
        assert isinstance(self.account.get_balance(), int)

    def test_deposit(self):
        orig_balance = self.account.get_balance()
        self.account.deposit(100)
        assert self.account.get_balance() == orig_balance + 100

    def test_withdraw(self):
        orig_balance = self.account.get_balance()
        self.account.withdraw(100)
        assert self.account.get_balance() == orig_balance - 100

    def test_deposit_negative(self):
        orig_balance = self.account.get_balance()
        with pytest.raises(ValueError, match="Negative value"):
            self.account.deposit(-150)
        assert orig_balance == self.account.get_balance()

    def test_withdraw_negative(self):
        orig_balance = self.account.get_balance()
        with pytest.raises(ValueError, match="Negative value"):
            self.account.withdraw(-150)
        assert orig_balance == self.account.get_balance()

    def test_withdraw_too_much(self):
        orig_balance = self.account.get_balance()
        with pytest.raises(ValueError, match="No money"):
            self.account.withdraw(1500)
        assert orig_balance == self.account.get_balance()

    def test_deposit_huge(self):
        orig_balance = self.account.get_balance()
        self.account.deposit(156151651651655)
        assert self.account.get_balance() == orig_balance + 156151651651655


class TestAccountTransfer:
    def setup(self):
        self.src_account = Account("Jan Kowalski", 1000.0)
        self.dst_account = Account("Piotr Wisniewski", 100.0)

    def test_transfer_to(self):
        orig_src_balance = self.src_account.get_balance()
        orig_dst_balance = self.dst_account.get_balance()
        self.src_account.transfer_to(self.dst_account, 1000.0)
        assert self.src_account.get_balance() == orig_src_balance - 1000.0
        assert self.dst_account.get_balance() == orig_dst_balance + 1000.0

    def test_transfer_to_too_much(self):
        orig_src_balance = self.src_account.get_balance()
        orig_dst_balance = self.dst_account.get_balance()
        amount_to_transfer = 2*orig_src_balance
        with pytest.raises(ValueError, match="No money"):
            self.src_account.transfer_to(self.dst_account, amount_to_transfer)
        assert self.src_account.get_balance() == orig_src_balance
        assert self.dst_account.get_balance() == orig_dst_balance

    def test_transfer_to_negative(self):
        with pytest.raises(ValueError, match="Negative value"):
            self.src_account.transfer_to(self.dst_account, -1000)
        assert self.src_account.get_balance() == 1000
        assert self.dst_account.get_balance() == 100

    def test_transfer_to_zero(self):
        with pytest.raises(ValueError, match="zero amount"):
            self.src_account.transfer_to(self.dst_account, 0)

    def test_transfer_to_itself(self):
        with pytest.raises(ValueError, match="transfer to itself"):
            self.src_account.transfer_to(self.src_account, 1000.0)
        assert self.src_account.get_balance() == 1000.0

    def test_transfer_to_not_number(self):
        with pytest.raises(ValueError, match="wrong amount type"):
            self.src_account.transfer_to(self.src_account, "42")
