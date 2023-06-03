import pygame
import sys
import random
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a custom event for spawning an enemy
SPAWNENEMY = pygame.USEREVENT + 1

score = 0


class SpriteSheet:
    def __init__(self, filename, n_across, n_down):
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.n_across = n_across
        self.n_down = n_down
        self.width = self.sprite_sheet.get_width() / n_across
        self.height = self.sprite_sheet.get_height() / n_down

    def get_image(self, x, y, width, height):
        # Grab a single image out of a larger spritesheet
        # Returns an image
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))  # Assuming black is your background color and is to be treated as transparent
        return image
    
    def get_random_image(self):
        x = random.randrange(self.n_across)
        y = random.randrange(self.n_down)
        return self.get_image(x * self.width, y * self.height, self.width, self.height)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player_100.png')  # Load the image for the player
        self.rect = self.image.get_rect()  # Get the rect of the image
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Set the starting position
        self.speed = 5  # Set the player's speed

    def update(self):
        keys = pygame.key.get_pressed()  # Get the keys pressed
        if keys[K_a]:  # Move left
            self.rect.move_ip(-self.speed, 0)
        if keys[K_d]:  # Move right
            self.rect.move_ip(self.speed, 0)
        if keys[K_w]:  # Move up
            self.rect.move_ip(0, -self.speed)
        if keys[K_s]:  # Move down
            self.rect.move_ip(0, self.speed)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('arrow_15.png')
        self.rect = self.image.get_rect(center=position)
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_sheet = SpriteSheet('pirates2_500.png', 7, 5)
        self.image = self.sprite_sheet.get_random_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        global score
        self.rect.move_ip(0, self.speedy)
        # If the enemy moves off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            score -= 5  # Subtract 5 points from the score
            self.kill()  # Remove the enemy


def main():
    global score
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.SysFont(None, 36)

    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Set the timer to trigger the SPAWNENEMY event every 10000 milliseconds (10 seconds)
    pygame.time.set_timer(SPAWNENEMY, 3000)

    score = 0
    high_score = 0
    lives = 3

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bullet = Bullet(player.rect.center)
                    bullets.add(bullet)
            elif event.type == SPAWNENEMY:
                # When the SPAWNENEMY event occurs, spawn an enemy
                enemy = Enemy()
                enemies.add(enemy)

        screen.fill((0, 0, 0))

        text = font.render(f'Score: {score} / Hi: {high_score} / Lives: {lives}', True, (255, 255, 255), (0, 0, 0))
        screen.blit(text, (10, 10))

        player.update()
        screen.blit(player.image, player.rect)

        bullets.update()
        bullets.draw(screen)

        enemies.update()
        enemies.draw(screen)

        for enemy in enemies:
            if pygame.sprite.collide_mask(player, enemy):
                enemy.kill()
                lives -= 1
                if lives == 0:
                    lives = 3
                    high_score = score
                    score = 0
            for bullet in bullets:
                if pygame.sprite.collide_mask(bullet, enemy):
                    bullet.kill()
                    enemy.kill()
                    score += 10

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
