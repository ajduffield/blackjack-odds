import unittest
from table_manager import *
from strategy import *
from shoe_manager import *
import test_config as cfg


def make_loaded_shoe(cards):
    shoe_cards = make_shoe(6)
    cards = [Card(x) for x in cards]
    shoe_cards.cards = cards
    shoe = Shoe(6)
    shoe.shoecards = shoe_cards
    return shoe


def make_round_setup(player_cards: [], dealer_cards: [], shoe_cards: []):
    shoe = make_loaded_shoe(player_cards + dealer_cards + shoe_cards)
    player = Player(1000)
    player_bet = 10
    num_player_hands = int(len(player_cards) / 2)
    return shoe, player, player_bet, num_player_hands


def add_suit(string: str):
    output = []
    for l in string:
        output.append(l + 'X')
    return output


# these tests

# player starting, player additional, dealer starting, dealer additional, result
blackjack_situations = [
    'AJ,,AT,,0',  # both blackjack push - A up
    'JA,,KA,,0',  # both blackjack push - K up
    'AT,,A5,,1.5',  # play blackjack against dealer A up
    'AJ,,65,,1.5',  # regular blackjack
    'KQ,,AK,,-1',  # dealer blackjack
    '56,T,JA,,-1',  # dealer blackjack vs player 21
]

hard_situations = [
    'Q8,,T5,K,1',  # player stay vs dealer bust
    'Q5,K,T5,K,-1',  # player bust vs dealer bust
    'QT,,KJ,,0',  # push
    '7J,,J7,,0',  # push
    'Q3,8,KT,,1',  # player win
    'T7,,83,7,-1',  # dealer win
    'T2,,6T,J,1',  # player stay vs dealer bust
    'T2,9,3T,5,1',  # player win
    '58,,46,9,-1'  # player stay loss
]

soft_situations = [
    'A7,T,T6,5,-1',  # player hit and loss
    'A7,T,T7,,1',  # player hit and win
    'A8,,KT,,-1',  # player stay and lose
    'A8,,98,,1',  # player stay and win
    'A3,2293,TK,,-1',  # lot of hit and lose
    'A2,2293,T8,,1',  # lot of hit and win
    'A2,2293,T9,,0',  # lot of hit and push
    'T9,,3A,TK,1',  # dealer down ace and win
    'T9,,A3,TK,1',  # dealer up ace and lose
    'T9,,9A,,-1',  # dealer down ace and lose
    'T9,,A9,,-1',  # dealer up ace and lose
    'A7,T,A6,K,1',  # both ace player win
    'A6,T,A6,4,-1',  # both ace player lose
    'A6,T,A6,57,-1',  # both ace player lose
]

double_situations = [
    '56,6,64,T,-2',  # double loss
    '36,T,6T,T,2',  # double win
    'A2,T,64,T,-2',  # ace loss
    'A2,7,64,9,2',  # ace win
    '74,9,A5,T5,-2',  # dealer ace loss
    '64,9,9T,,0',  # push
]

# payout is structured as final_hand:payout;final_hand_2:payout...
split_situations = [
    '88,TK,TJ,,8T:-1;8K:-1',  # split loss
    '88,TK,T5,T,8T:1;8K:1',  # split win
    '88,T5K,T5,2,8T:1;85K:-1',  # split win one lose one
    '88,T57,T8,,8T:0;857:1',  # split win one push one
    '88,T56,T9,,8T:-1;856:0',  # split lose one push one
    '33,3TKQ,6T,3,3T:-1;3K:-1;3Q:-1',  # triple split win none
    '33,35TKQ,5T,2,35T:1;3K:-1;3Q:-1',  # triple split win one
    '33,3TKQ,6T,6,3T:1;3K:1;3Q:1',  # triple split win all
    '66,66TKQJ,2T,6,6T:-1;6K:-1;6Q:-1;6K:-1',  # quadruple split lose all
    '88,88TK99,2T,5,8T:1;8K:1;89:0;89:0',  # quadruple split win two push two
    '88,8884K98A,2T,5,884:1;8K:1;89:0;88A:0',  # 5 split not allowed
]


class PlayingTests(unittest.TestCase):
    # not a test case
    def setup_and_run_test_from_string(self, test):
        player_cards, player_extra, dealer_cards, dealer_extra, result = tuple(test.split(','))
        shoe, player, player_bet, num_player_hands = make_round_setup(add_suit(player_cards),
                                                                      add_suit(dealer_cards),
                                                                      add_suit(player_extra + dealer_extra))
        play_round(shoe, player, player_bet, num_player_hands)
        self.assertEqual(player.bankroll, 1000 + player_bet * float(result))

    def test_basic_strategy(self):
        pass

    def test_betting_strategy(self):
        pass

    def test_blackjack(self):
        for i, test in enumerate(blackjack_situations):
            print(f'Running test {str(i+1)}: {test}')
            self.setup_and_run_test_from_string(test)

    def test_hard(self):
        for i, test in enumerate(hard_situations):
            print(f'Running test {str(i+1)}: {test}')
            self.setup_and_run_test_from_string(test)

    def test_soft(self):
        for i, test in enumerate(soft_situations):
            print(f'Running test {str(i+1)}: {test}')
            self.setup_and_run_test_from_string(test)

    def test_double(self):
        for i, test in enumerate(double_situations):
            print(f'Running test {str(i+1)}: {test}')
            self.setup_and_run_test_from_string(test)

    def test_split(self):
        for i, test in enumerate(split_situations):
            print(f'Running test {str(i+1)}: {test}')
            player_cards, player_extra, dealer_cards, dealer_extra, result = tuple(test.split(','))
            shoe, player, player_bet, num_player_hands = make_round_setup(add_suit(player_cards),
                                                                          add_suit(dealer_cards),
                                                                          add_suit(player_extra + dealer_extra))
            play_round(shoe, player, player_bet, num_player_hands)
            split_results = [x.split(':') for x in result.split(';')]
            print(str(split_results))
            expected_bankroll = 1000
            for result in split_results:
                expected_bankroll += player_bet * float(result[1])
            self.assertEqual(player.bankroll, expected_bankroll)

    def test_hit(self):
        self.assertEqual(True, True)

    def test_stay(self):
        pass

    def test_ace(self):
        pass


class BackboneTests(unittest.TestCase):
    def test_shoe(self):
        self.assertEqual(len(make_shoe(4).cards), 52 * 4)
        self.assertEqual(len(make_shoe(6).cards), 52 * 6)

        self.assertEqual(len(Shoe(4).shoecards.cards), 52 * 4)
        self.assertEqual(len(Shoe(6).shoecards.cards), 52 * 6)

    def test_player(self):
        player = Player(1000)
        self.assertEqual(player.bankroll, 1000)

        # winning a hand
        player.take_money(10)
        self.assertEqual(player.bankroll, 990)
        player.win_money(10, 1)
        self.assertEqual(player.bankroll, 1010)

        # losing a hand
        player = Player(1000)
        player.take_money(10)
        self.assertEqual(player.bankroll, 990)
        player.win_money(10, -1)
        self.assertEqual(player.bankroll, 990)

        # pushing a hand
        player = Player(1000)
        player.take_money(25)
        self.assertEqual(player.bankroll, 975)
        player.win_money(25, 0)
        self.assertEqual(player.bankroll, 1000)

        # getting blackjack
        player.take_money(10)
        self.assertEqual(player.bankroll, 990)
        player.win_money(10, 1.5)
        self.assertEqual(player.bankroll, 1015)

    def test_round(self):
        round = make_round(['AS', 'JD'], ['5S', 'TC'], ['3D'])
        self.assertEqual(round.shoe.shoecards.cards, [Card('AS'), Card('JD'), Card('5S'), Card('TC'), Card('3D')])

        # self.assertEqual(round.shoe.shoecards.cards, [Card('3D')])

    def test_deal_cards(self):
        shoe = make_loaded_shoe(['AD', 'KD', 'TD', 'JD', '5D', '3D', '7S', '5C', '2C'])

        shoe.deal_cards(2)
        self.assertEqual(shoe.running_count, -2)

        shoe.deal_cards(2)
        self.assertEqual(shoe.running_count, -4)

        shoe.deal_cards(2)
        self.assertEqual(shoe.running_count, -2)

        shoe.deal_cards(1)
        self.assertEqual(shoe.running_count, -2)
        # -2 / just less than 6
        self.assertLess(shoe.true_count, -.33)
        self.assertGreater(shoe.true_count, -.4)

        shoe.deal_cards(2)
        self.assertEqual(shoe.running_count, 0)
        self.assertEqual(shoe.true_count, 0)

    def test_true_count_conversion(self):
        shoe = Shoe(6)

        self.assertEqual(shoe.running_count, 0)
        self.assertEqual(shoe.true_count, 0)

        shoe.deal_cards(52)
        self.assertEqual(shoe.running_count / 5, shoe.true_count)

        shoe.deal_cards(52)
        self.assertEqual(shoe.running_count / 4, shoe.true_count)

        shoe.deal_cards(52)
        self.assertEqual(shoe.running_count / 3, shoe.true_count)

        shoe.deal_cards(52)
        self.assertEqual(shoe.running_count / 2, shoe.true_count)

    def test_on_card(self):
        shoe = Shoe(6)

        self.assertEqual(shoe.shoecards.decks, 6)
        self.assertEqual(shoe.on_card, 0)
        self.assertEqual(shoe.red_card, 52 * 4.5)

        shoe.deal_cards(5)
        self.assertEqual(shoe.on_card, 5)

        shoe.deal_cards(10)
        self.assertEqual(shoe.on_card, 15)

        shoe.deal_cards(100)
        self.assertEqual(shoe.on_card, 115)

    def test_decks_left(self):
        shoe = Shoe(6)

        self.assertEqual(shoe.decks_left(), 6)

        shoe.deal_cards(1)
        self.assertEqual(shoe.decks_left(), ((6*52)-1)/52)

        shoe.deal_cards(51)
        self.assertEqual(shoe.decks_left(), 5)

        shoe.deal_cards(104)
        self.assertEqual(shoe.decks_left(), 3)


    def test_table_update(self):
        pass


if __name__ == '__main__':
    unittest.main()

