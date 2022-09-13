class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def get_owner(self):
        return self.owner

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


a1 = Account("Jan Kowalski", 1000)


def test_get_owner():
    assert isinstance(a1.get_owner(), str)


def test_get_balance():
    assert isinstance(a1.get_balance(), (int, float))


def test_deposit():
    balance = a1.balance
    a1.deposit(100)
    assert a1.balance - balance == 100


def test_withdraw():
    balance = a1.balance
    a1.withdraw(100)
    assert balance - a1.balance == 100
