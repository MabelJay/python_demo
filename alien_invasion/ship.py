import pygame


class Ship:
    """class for managing ship"""

    def __init__(self, ai_game):
        """initialize ship and set initial location"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # load ship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # set ship location
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """blit this ship"""
        self.screen.blit(self.image, self.rect)
