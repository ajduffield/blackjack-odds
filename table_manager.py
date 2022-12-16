import config as cfg
from shoe_manager import make_shoe
from strategy import do_basic_strategy, take_insurance_or_even_money
from exceptions import NoMoneyException


def find_running_count(cards):
    running_count = 0
    for card in cards:
        if card.value >= 10 or card.value == 1:
            running_count -= 1
        elif card.value <= 6:
            running_count += 1
    return running_count


class Shoe:
    def __init__(self, decks):
        shoecards = make_shoe(decks)
        shoecards.shuffle()
        self.shoecards = shoecards
        self.red_card = int(cfg.table['deck_penetration'] * (decks * 52))
        self.on_card = 0
        self.running_count = 0
        self.true_count = 0
        print(self.shoecards.cards)

    def deal_cards(self, number):
        cards = self.shoecards.cards[self.on_card:self.on_card + number]
        self.update_table(number)
        return cards

    def decks_left(self):
        return ((self.shoecards.decks * 52) - self.on_card) / 52

    def update_table(self, cards_used):
        running_count_change = find_running_count(self.shoecards.cards[self.on_card:(self.on_card + cards_used)])
        self.on_card += cards_used
        self.running_count += running_count_change
        decks_left = self.decks_left()
        self.true_count = self.running_count / decks_left


class Hand:
    def __init__(self, shoe):
        self.shoe = shoe
        cards = shoe.deal_cards(2)
        if cards[0].isace and cards[0].value == 1 or cards[1].isace and cards[1].value == 1:
            raise Exception('Dealt an ace with a value of 1')
        if cards[0].isace and cards[1].isace:
            cards[0].value = 1
        self.cards = cards
        self.value = sum(self.cards)
        self.issoft = self.cards[0].isace or self.cards[1].isace

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __str__(self):
        return str(self.cards)

    def __repr__(self):
        return str(self.cards)

    def add_card(self):
        new_card = self.shoe.deal_cards(1)[0]
        if self.issoft and self.value + new_card.value > 21:
            print('setting existing ace to 1')
            # find the ace and set the value to 1:
            for card in self.cards:
                if card.isace and card.value == 11:
                    card.value = 1
                    break
            self.issoft = False
            self.value -= 10
        if new_card.isace:
            if self.value > 10:
                print('adding new ace as 1')
                new_card.value = 1
            else:
                self.issoft = True
        self.cards.append(new_card)
        self.value = sum(self.cards)

    def update(self):
        self.value = sum(self.cards)
        self.issoft = False
        for card in self.cards:
            if card.isace and card.value == 11:
                self.issoft = True
                break


class PlayerHand(Hand):
    def __init__(self, player, shoe, bet, is_doubleable=True, is_splitable=True, is_hitable=True):
        super().__init__(shoe)
        self.player = player
        self.bet = player.take_money(bet)
        self.is_doubleable = is_doubleable
        self.is_splitable = is_splitable and self.cards[0].rep == self.cards[1].rep
        self.is_hitable = is_hitable and not is_blackjack(self)

    def hit(self):
        self.add_card()
        self.is_splitable = False
        self.is_doubleable = False

    def stand(self):
        self.is_splitable = False
        self.is_doubleable = False
        self.is_hitable = False

    def double(self):
        if not self.is_doubleable:
            raise Exception("Attempting to double a non-doubleable hand")
        self.bet += self.player.take_money(self.bet)
        self.hit()
        self.is_hitable = False

    def split(self):
        if not self.is_splitable:
            raise Exception("Attempting to split a non-splitable hand")
        split_hand = PlayerHand(self.player, self.shoe, self.bet, is_doubleable=cfg.table_rules['DAS'])
        # give each hand one old card and one new card
        temp_split_card = self.cards[1]
        self.cards = [self.cards[0], split_hand.cards[0]]
        split_hand.cards = [temp_split_card, split_hand.cards[1]]
        self.update()
        split_hand.update()
        self.is_splitable = self.cards[0].rep == self.cards[1].rep
        split_hand.is_splitable = split_hand.cards[0].rep == split_hand.cards[1].rep
        return split_hand


def is_busted(hand: Hand):
    return hand.value > 21


def is_blackjack(hand: Hand):
    return len(hand.cards) == 2 and hand.value == 21


class Player:
    def __init__(self, bankroll):
        self.bankroll = bankroll

    @property
    def bankroll(self):
        return self._bankroll

    @bankroll.setter
    def bankroll(self, value):
        if value < 0:
            raise NoMoneyException()
        self._bankroll = value

    def take_money(self, value):
        self.bankroll -= value
        return value

    def win_money(self, bet, payout):
        self.bankroll += (bet + bet * payout)


class Round:
    def __init__(self, shoe, player, player_bet, num_player_hands):
        self.shoe = shoe
        self.player_hands = [PlayerHand(player, shoe, player_bet) for _ in range(num_player_hands)]
        self.dealer_hand = Hand(shoe)
        self.dealer_upcard = self.dealer_hand.cards[0]

    def __str__(self):
        return str(self.player_hands + ['|'] + self.dealer_hand.cards)

    def __repr__(self):
        return str(self.player_hands + ['|'] + self.dealer_hand.cards)


def get_winner(player: Hand, dealer: Hand):
    if is_blackjack(player) and is_blackjack(dealer):
        return 't', 'Push BlackJack', 0
    if is_blackjack(player):
        return 'p', 'Player BlackJack', cfg.table_rules['BJP']
    if is_blackjack(dealer):
        return 'd', 'Dealer BlackJack', -1
    if player.value > 21:
        return 'd', 'Player bust', -1
    if dealer.value > 21:
        return 'p', 'Dealer bust', 1
    if player > dealer:
        return 'p', f'Player {player.value} beats dealer {dealer.value}', 1
    if player < dealer:
        return 'd', f'Player {player.value} loses to dealer {dealer.value}', -1
    return 't', f'Tie at {player.value}={dealer.value}', 0


def play_round(shoe, player, player_bet, num_player_hands):
    print('ROUND STARTING: COUNTS NOW: RC: ' + str(shoe.running_count) + ' TC: ' + str(shoe.true_count) + ' BET: ' + str(player_bet))
    round = Round(shoe, player, player_bet, num_player_hands)
    # check dealer card for blackjack
    print(str(round))

    # offer insurance
    if round.dealer_upcard.rep == 'A':
        insurance = take_insurance_or_even_money(shoe.true_count)
        if insurance:
            insurance_bet = (player_bet * num_player_hands) / 2
            print("Taking insurance for " + str(insurance_bet))
            player.take_money(insurance_bet)
            if is_blackjack(round.dealer_hand):
                player.win_money(insurance_bet, 2)
                print('Won insurance ' + str(player.bankroll))
            else:
                player.win_money(insurance_bet, -1)
                print('Lost insurance ' + str(player.bankroll))


    # play player hand
    # skip player decisions if the dealer has a blackjack
    if not is_blackjack(round.dealer_hand):
        for hand in round.player_hands:
            while hand.is_hitable:
                action = do_basic_strategy(hand.value, hand.issoft,
                                           hand.is_splitable,
                                           round.dealer_upcard.value,
                                           hand.is_doubleable)
                print('ACTION IS: ' + action)
                if action == 'sp':
                    print('SPLIT ' + str(round.player_hands))
                    round.player_hands.append(hand.split())
                    print('SPLIT AFTER' + str(round.player_hands))
                elif action == 'd':
                    hand.double()
                elif action == 'h':
                    hand.hit()
                elif action == 's':
                    hand.stand()
                else:
                    raise Exception("Unknown action")

    # play dealer hand
    skip_dealer = True
    for hand in round.player_hands:
        if not is_blackjack(hand) and not is_busted(hand):
            skip_dealer = False
    while not skip_dealer and (round.dealer_hand.value < 17 or (cfg.table_rules['H17'] and round.dealer_hand.value == 17 and round.dealer_hand.issoft)):
        round.dealer_hand.add_card()
    print(str(round))
    # find winner
    for hand in round.player_hands:
        winner, description, payout = get_winner(hand, round.dealer_hand)
        print(winner, description, str(payout))
        player.win_money(hand.bet, payout)
        print('WON $' + str((hand.bet + hand.bet * payout)) + ' TOTAL $' + str(player.bankroll))


# if __name__ == '__main__':
    # s = Shoe(20)
    # print(s.shoecards.cards)
    # rounds = 100
    # print(f'running {str(rounds)} rounds... player | dealer')
    # for i in range(rounds):
    #     h = Round(s)
    #     # s.update_table(4)
    #     print(h)
    #     # out = h.get_winner()
    #     print(h)
    #     print(out)
    #     print(f'Cards played: {str(s.on_card)}, RC: {str(s.running_count)}, TC: {str(s.true_count)}')

