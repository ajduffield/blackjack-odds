
class NoMoneyException(Exception):
    def __init__(self):
        super().__init__("No money left!")


class BadCountException(Exception):
    def __init__(self):
        super().__init__("Leaving until new shoe, bad count")