
class GameStats:
    """trace game info"""

    def __init__(self, ai_game):
        """init aggregate info"""
        self.settings = ai_game.settings
        self.reset_stats()

        # flag to record game status
        self.game_active = False

        # not to reset highest score in any cases
        self.high_score = 0

    def reset_stats(self):
        """initialize info when changing in the game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

