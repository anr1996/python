## Starting The Game Project. ##
# Creating a Pygame Window and Responding to User Input

import sys

import pygame

from random import random
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

      



        """Setting the Background Color"""
        self.bg_color = (250,235,215)

    def run_game(self):
        """Start the main loop for the game."""

    

        while True:
            self._check_events()

            # consider creating a new alien.
            self._create_alien()
            

            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen() 
            


    def _check_events(self):
        """respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    
    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()




    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)  


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)
                    # printing len of bullets just verifies that the bullets are being removed once off the game screen.
        print(len(self.bullets))



    # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()



    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided
       
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_alien()    



    
    def _create_alien(self):
        """Create an alien, if conditions are right."""
        if random() < self.settings.alien_frequency:
            alien = Alien(self)
            self.aliens.add(alien)
            print(len(self.aliens))






    def _update_aliens(self):

        """update the positions of all aliens in the fleet."""
        self.aliens.update()
      



                 
    def _update_screen(self):
        """update images on the screen, and flip to the new screen"""

        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen) 


        # Make the most recent drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()

