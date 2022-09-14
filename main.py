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
            print("Operation Aborted: You cannot deposit negative value! Balance on your account has not been changed")
        else:
            self.balance += amount

    def withdraw(self, amount):
        if amount < 0:
            print("Operation Aborted: You cannot withdraw negative value! Balance on your account has not been changed")
        else:
            self.balance -= amount


a1 = Account("Jan Kowalski", 1000)


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
        self.account.deposit(-100)
        assert self.account.get_balance() == orig_balance

    def test_withdraw_negative(self):
        orig_balance = self.account.get_balance()
        self.account.withdraw(-100)
        assert self.account.get_balance() == orig_balance

    def test_deposit_huge(self):
        orig_balance = self.account.get_balance()
        self.account.deposit(156151651651655)
        assert self.account.get_balance() == orig_balance + 156151651651655
