from unittest.mock import MagicMock, patch
import pytest
import main as account


class API:
    @staticmethod
    def get_pin_from_stdin():
        with open("card.txt", "r") as f:
            lines = f.readlines()
            pin = lines[0]
            if pin[:3] == "PIN":
                return int(pin[-4:])
            else:
                raise ValueError("There is no PIN inside card.txt")


class Card:
    # TODO: depedency injection. We should stop being aware
    # of API.get_pin_from_stdin!
    def __init__(self, src_account, pin):
        self.src_account = src_account
        self.pin = pin

    def transfer_to(self, dst_account, amount):
        if self.pin == API.get_pin_from_stdin():
            self.src_account.transfer_to(dst_account, amount)

class TestCard:
    def test_card_payment(self):
        # Given
        src_account = account.Account("Card Holder", 100)
        card = Card(src_account, pin=1234)
        dst_account = account.Account("Merchant", 1000)
        # When
        fake_get_pin_from_stdin = MagicMock(return_value=1234)
        with patch.object(API, 'get_pin_from_stdin', fake_get_pin_from_stdin):
            card.transfer_to(dst_account, 100)
        # Then
        assert src_account.get_balance() == 0
        assert dst_account.get_balance() == 1100
