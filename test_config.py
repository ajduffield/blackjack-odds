table_rules = {
    'BJP': 3/2,  # BlackJack payout
    'max_split': 3,
    'decks': 8,
    'DAS': True,  # Double after split
    'H17': True,  # Hit soft 17
    'surrender': False,
    'min_bet': 10,
    'max_bet': 10000
}

player = {
    'use_deviations': False,
    'bankroll': 5000
}

table = {
    'players': 1,
    'deck_penetration': .75
}

bets = {
    -1: 1,
    0: 1,
    1: 2,
    2: 3,
    3: 4,
    4: 12
}

stats = {
    'shoes_played': 10,
}


def get_test_cfg(name):
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