# Pygame window

import sys
import pygame
from settings import Settings
from  ship import Ship


class AlienInvasion:
    """ manage game resources and actions in this class"""

    def __init__(self):
        """initialize game and create game resources"""
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        """start the game"""
        while True:
            self._check_events()
            self._update_events()

    def _check_events(self):
        """monitor the events of keys and mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_events(self):
        # re-print screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # show up the screen
        pygame.display.flip()


if __name__ == '__main__':
    # create the class instance and run this game
    ai = AlienInvasion()
    ai.run_game()
