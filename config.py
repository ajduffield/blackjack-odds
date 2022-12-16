from test_config import get_test_cfg

# if debug is set to true, config is taken from test_config instead
debug = True

table_rules = {
    'BJP': 3/2,  # BlackJack payout
    'max_split': 3,
    'decks': 6,
    'DAS': True,  # Double after split
    'H17': True,  # Hit soft 17
    'surrender': False,
    'min_bet': 25,
    'max_bet': 10000
}

player = {
    'use_deviations': False,
    'bankroll': 10000
}

table = {
    'players': 1,
    'deck_penetration': .75
}

bets = {
    -2: 0,
    -1: 1,
    0: 1,
    1: 2,
    2: 6,
    3: 15,
    4: 20
}

stats = {
    'shoes_played': 10,
}


def get_cfg(name):
    if debug:
        return get_test_cfg(name)

    if name in ['tr', 'table_rules']:
        return table_rules
    if name in ['p', 'player']:
        return player
    if name in ['t', 'table']:
        return table
    if name in ['b', 'bets']:
        return bets
    if name in ['s', 'stats']:
        return stats

    raise Exception('Unknown cfg')
