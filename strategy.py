import config as cfg


# ------------ BASIC STRATEGY METHODS ------------
def do_soft_basic_strategy(nonace, dealer_upcard, double_allowed):
    if nonace == 9:
        return 's'
    elif nonace == 8:
        if dealer_upcard == 6 and double_allowed:
            return 'd'
        return 's'
    elif nonace == 7:
        if dealer_upcard <= 6 and double_allowed:
            return 'd'
        elif dealer_upcard <= 8:
            return 's'
        return 'h'
    elif nonace == 6:
        if dealer_upcard in [3, 4, 5, 6] and double_allowed:
            return 'd'
        return 'h'
    elif nonace in [5, 4]:
        if dealer_upcard in [4, 5, 6] and double_allowed:
            return 'd'
        return 'h'
    else:
        # nonace in 3, 2
        if dealer_upcard in [5, 6] and double_allowed:
            return 'd'
        return 'h'


def split_pair_basic_strategy(card, dealer_upcard):
    if card in [10, 5, 4]:
        return False
    elif card == 9:
        return dealer_upcard not in [7, 10, 11]
    elif card == 8:
        return True
    elif card == 7:
        return dealer_upcard <= 7
    elif card == 6:
        return dealer_upcard in [3, 4, 5, 6]
    elif card in [3, 2]:
        return dealer_upcard in [4, 5, 6, 7]


def do_basic_strategy(hand_total, soft, pair, dealer_upcard, double_allowed):
    if soft and pair:
        # must be AA
        return 'sp'
    if soft:
        return do_soft_basic_strategy(hand_total - 11, dealer_upcard, double_allowed)
    if pair and split_pair_basic_strategy(hand_total / 2, dealer_upcard):
        return 'sp'
    # must be normal hand
    if hand_total >= 17:
        return 's'
    elif hand_total >= 13:
        if dealer_upcard >= 7:
            return 'h'
        return 's'
    elif hand_total == 12:
        if dealer_upcard >= 7 or dealer_upcard <= 3:
            return 'h'
        return 's'
    elif hand_total == 11:
        if double_allowed:
            return 'd'
        return 'h'
    elif hand_total == 10:
        if dealer_upcard <= 9 and double_allowed:
            return 'd'
        return 'h'
    elif hand_total == 9:
        if dealer_upcard in [3, 4, 5, 6] and double_allowed:
            return 'd'
        return 'h'
    else:
        # hand total of 8 or less
        return 'h'


# ------------ BETTING METHODS ------------
def make_bet(true_count):
    rounded_true_count = int(true_count)
    if cfg.bets.get(rounded_true_count):
        return cfg.bets[rounded_true_count]
    max_listed = max(cfg.bets.keys())
    min_listed = min(cfg.bets.keys())
    if true_count > max_listed:
        return cfg.bets[max_listed]
    # must be less
    return cfg.bets[min_listed]


def take_insurance_or_even_money(true_count):
    return true_count >= 3

