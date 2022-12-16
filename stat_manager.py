

class HandStat:
    def __init__(self, payout, bet, true_count, hand, dealer_hand, insurance_bet=0, insurance_payout=None):
        self.bet = bet
        self.payout = payout
        self.insurance_bet = insurance_bet
        self.insurance_payout = insurance_payout
        self.true_count = true_count
        self.hand = hand
        self.dealer_hand = dealer_hand


class ShoeStat:
    def __init__(self, hand_stats: []):
        self.hand_stats = hand_stats

    def get_session_result(self):
        pass

    def get_session_hourly(self):
        pass

    def get_session_edge_as_played(self):
        pass

    def get_session_flat_bet_house_edge(self):
        pass

    def get_breakeven_true_count(self):
        pass


class PlayerStat:
    pass


class GameStat:
    def __init__(self, session_stats: []):
        self.session_stats = session_stats

    # returns mean and standard deviation
    def get_average_sessions_result(self):
        pass

    # returns mean and standard deviation
    def get_average_hourly(self):
        pass

    def get_risk_of_ruin(self):
        pass

    def get_edge_stats(self):
        pass

    def get_average_breakeven_true_count(self):
        pass
