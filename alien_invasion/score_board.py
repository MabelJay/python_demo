import pygame.font
from pygame.sprite import Group
from ship import Ship


class ScoreBoard:
    """show the score info with this class"""

    def __init__(self, ai_game):
        """initialize score fields"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # score font settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the score image
        self.prep_score()
        self.pre_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        round_score = round(self.stats.score, -1)
        score_str = "{:,}".format(round_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # display the score on the right corner of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.score_rect.right - 20
        self.score_rect.top = 20

    def pre_high_score(self):
        """render high score image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # display the high score in the top center of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """check if current score is higher than known high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.pre_high_score()

    def show_score(self):
        """display score"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_level(self):
        """transfer grade to image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # level will locate in under of score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.score_rect.left
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """display how many ships left"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = self.screen_rect.right - ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)



