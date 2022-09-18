import pytest
# Exceptions classes -----------------------------------------------------------------------------------------------


class NegativeAmountError(Exception):
    def __init__(self):
        super().__init__("Negative amount")


class NoMoney(Exception):
    def __init__(self):
        super().__init__("No money")


class WrongAmountType(Exception):
    def __init__(self):
        super().__init__("Wrong amount type")


class ZeroAmount(Exception):
    def __init__(self):
        super().__init__("Zero amount")


class TransferToItself(Exception):
    def __init__(self):
        super().__init__("Transfer to itself")

# Exceptions classes -----------------------------------------------------------------------------------------------

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
            raise NegativeAmountError
        else:
            self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise NoMoney
        elif amount < 0:
            raise NegativeAmountError
        else:
            self.balance -= amount

    def transfer_to(self, dst_account, amount):
        if not isinstance(amount, (int, float)):
            raise WrongAmountType
        if amount == 0:
            raise ZeroAmount
        if dst_account is self:
            raise TransferToItself
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
        with pytest.raises(NegativeAmountError):
            self.account.deposit(-150)
        assert orig_balance == self.account.get_balance()

    def test_withdraw_negative(self):
        orig_balance = self.account.get_balance()
        with pytest.raises(NegativeAmountError):
            self.account.withdraw(-150)
        assert orig_balance == self.account.get_balance()

    def test_withdraw_too_much(self):
        orig_balance = self.account.get_balance()
        with pytest.raises(NoMoney):
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
        with pytest.raises(NoMoney):
            self.src_account.transfer_to(self.dst_account, amount_to_transfer)
        assert self.src_account.get_balance() == orig_src_balance
        assert self.dst_account.get_balance() == orig_dst_balance

    def test_transfer_to_negative(self):
        with pytest.raises(NegativeAmountError):
            self.src_account.transfer_to(self.dst_account, -1000)
        assert self.src_account.get_balance() == 1000
        assert self.dst_account.get_balance() == 100

    def test_transfer_to_zero(self):
        with pytest.raises(ZeroAmount):
            self.src_account.transfer_to(self.dst_account, 0)

    def test_transfer_to_itself(self):
        with pytest.raises(TransferToItself):
            self.src_account.transfer_to(self.src_account, 1000.0)
        assert self.src_account.get_balance() == 1000.0

    def test_transfer_to_not_number(self):
        with pytest.raises(WrongAmountType):
            self.src_account.transfer_to(self.src_account, "42")
