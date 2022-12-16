import random


class Card:
    rep_to_value_map = {
        'A': 11,
        'K': 10,
        'Q': 10,
        'J': 10,
        'T': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2
    }

    def __init__(self, rep):
        self.rep = rep[0]
        self.suit = rep[1]
        self.value = self.rep_to_value_map[rep[0]]
        self.isace = rep[0] == 'A'

    def __str__(self):
        if self.isace:
            return self.rep + str(self.value)
        return self.rep

    def __repr__(self):
        if self.isace:
            return self.rep + str(self.value)
        return self.rep

    def __int__(self):
        return self.value

    def __radd__(self, other):
        return int(self) + int(other)

    def __eq__(self, other):
        return self.rep == other.rep and self.suit == other.suit


class ShoeCards:
    def __init__(self, decks, cards):
        self.decks = decks
        self.cards = cards

    # shuffles the shoe
    def shuffle(self):
        random.shuffle(self.cards)


# returns a shoe not shuffled
def make_shoe(decks: int) -> ShoeCards:
    cards = []
    for deck in range(decks):
        cards += make_deck()
    return ShoeCards(decks, cards)


# returns 1 deck not shuffled
def make_deck() -> []:
    card_reprs = ['AC', 'AD', 'AH', 'AS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS', 'JC', 'JD', 'JH', 'JS', 'TC', 'TD',
                  'TH', 'TS', '9C', '9D', '9H', '9S', '8C', '8D', '8H', '8S', '7C', '7D', '7H', '7S', '6C', '6D', '6H', '6S',
                  '5C', '5D', '5H', '5S', '4C', '4D', '4H', '4S', '3C', '3D', '3H', '3S', '2C', '2D', '2H', '2S']

    cards = []
    for card_rep in card_reprs:
        cards.append(Card(card_rep))

    return cards


if __name__ == '__main__':
    a = make_shoe(3)
    a.shuffle()
    print(a.cards)
