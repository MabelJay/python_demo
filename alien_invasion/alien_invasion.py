# Pygame window

import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard


class AlienInvasion:
    """ manage game resources and actions in this class"""

    def __init__(self):
        """initialize game and create game resources"""
        pygame.init()

        self.settings = Settings()
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))

        # full-screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # create an instance for saving game info
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet_()

        # create a play button
        self.play_button = Button(self, "Play")

        # create a play score board
        self.sb = ScoreBoard(self)

    def run_game(self):
        """start the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _update_bullets(self):
        self.bullets.update()
        # delete disappeared bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check if bullet hits the aliens
        # if yes, then delete corresponding bullet and alien
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # delete current bullets on screen and create a new series of aliens
            self.bullets.empty()
            self._create_fleet_()
            self.settings.increase_speed()

            # level up
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """update aliens group's location"""
        self._check_fleet_edges()
        self.aliens.update()

        # check collision between ship and aliens
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # check aliens if in the bottom
        self._check_aliens_bottom()

    def _ship_hit(self):
        """response to collision when ship the alien hit the ship"""

        if self.stats.ship_left > 1:
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # empty left aliens and bullets on screen
            self.aliens.empty()
            self.bullets.empty()

            # create a new group of aliens, ship will show in the bottom center
            self._create_fleet_()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_events(self):
        """monitor the events of keys and mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start to play game when user clicks the play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset game
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # empty the left aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new group of aliens, ship will be center
            self._create_fleet_()
            self.ship.center_ship()

            # hide the mouse when playing the game
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """response to key down event"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key ==pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """create a bullet and add it to bullets group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        # re-print screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # show the score
        self.sb.show_score()

        # display play button when game is in inactive status
        if not self.stats.game_active:
            self.play_button.draw_button()

        # display the screen
        pygame.display.flip()

    def _create_fleet_(self):
        """create a group of alien"""
        # create one aline object
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # alien_width = alien.rect.width
        # alien_height = alien.rect.height
        available_width = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_width // (2 * alien_width)

        # calculate the rows of aliens with screen height
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (2 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # create a group of aliens
        for row_number in range(number_rows):
            for alien_num in range(number_aliens_x):
                self._create_alien_(alien_num, row_number)

    def _create_alien_(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # alien_width = alien.rect.width
        # alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """take actions when alien reaches to the edges"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()

    def _change_fleet_direction(self):
        """move down the aliens and change the direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """check if aliens reaches at the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # process this case
                self._ship_hit()
                break


if __name__ == '__main__':
    # create the class instance and run this game
    ai = AlienInvasion()
    ai.run_game()
