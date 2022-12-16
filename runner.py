from table_manager import play_round, Shoe, Player
from strategy import make_bet
import config as cfg
import numpy as np
from exceptions import NoMoneyException
from stat_manager import GameStat, PlayerStat, ShoeStat, HandStat


def play_shoe(player):
    shoe = Shoe(cfg.table_rules['decks'])
    # shoe_stat = ShoeStat(shoe)
    while shoe.on_card < shoe.red_card:
        bet = make_bet(shoe.true_count) * cfg.table_rules['min_bet']
        play_round(shoe, player, bet, 1)


def play_session():
    player = Player(cfg.player['bankroll'])
    # player_stat = PlayerStat(player)
    for _ in range(cfg.stats['shoes_played']):
        play_shoe(player)
    return player


if __name__ == '__main__':
    results = []
    bankrupt_counter = 0
    game_stat = GameStat([])
    for _ in range(10):
        try:
            results.append(play_session().bankroll)
        except NoMoneyException:
            results.append(0)
            bankrupt_counter += 1
    print(np.mean(results))
    print(bankrupt_counter)
    print(min(results))
    print(max(results))


