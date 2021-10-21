import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """define a class for a single alien"""

    def __init__(self, ai_game):
        """initialize alien and initial location"""
        super().__init__()
        self.screen = ai_game.screen

        # load alien image and set rect fields
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # each alien's initial location is on the left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store precise location for aliens
        self.x = float(self.rect.x)

        self.settings = ai_game.settings

    def update(self):
        """move to right"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """if the alien locates in screen edge, then return True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True



