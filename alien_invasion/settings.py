
class Settings:
    """store all settings in this class"""

    def __init__(self):
        """initialize game's setting"""
        # screen setting
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # alien settings
        self.fleet_drop_speed = 1

        # game speed up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1

        # move to right when fleet_direction = 1, move to left when fleet_direction = -1
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        """speed up settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale



