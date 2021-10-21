import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """class for managing the bullet of ship"""

    def __init__(self, ai_game):
        """create a bullet object in current ship's location"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create a rect in (0,0) to trace the bullet and set the correct location
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # store the bullet location in float value
        self.y = float(self.rect.y)

    def update(self):
        """move up"""
        # update the float value of the bullet location
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """draw this bullet in the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
