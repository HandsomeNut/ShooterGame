try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame as pg
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module {err}")
    sys.exit(2)
if not pg.font:
    print("Warning, fonts disabled")

# This goes outside the while loop, near the top of the program

pg.init()

bg = pg.image.load('bg.jpg')
screenwidth = 640
screenheight = 480

screen = pg.display.set_mode((screenwidth, screenheight))
pg.display.set_caption("First Game")


class Character(pg.sprite.Sprite):
    walkRight = [pg.image.load('R1.png'), pg.image.load('R2.png'), pg.image.load('R3.png'), pg.image.load('R4.png'),
                 pg.image.load('R5.png'), pg.image.load('R6.png'), pg.image.load('R7.png'), pg.image.load('R8.png'),
                 pg.image.load('R9.png')]
    walkLeft = [pg.image.load('L1.png'), pg.image.load('L2.png'), pg.image.load('L3.png'), pg.image.load('L4.png'),
                pg.image.load('L5.png'), pg.image.load('L6.png'), pg.image.load('L7.png'), pg.image.load('L8.png'),
                pg.image.load('L9.png')]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.isJump = False
        self.jumpCount = 10
        self.walkcount = 0
        self.left = False
        self.right = True
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 28, 52)


    def draw(self, screen):
        if self.walkcount + 1 >= 27:
            self.walkcount = 0

        if not self.standing:
            if self.left:
                screen.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            elif self.right:
                screen.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
        else:
            if self.right:
                screen.blit(self.walkRight[0], (self.x, self.y))
            else:
                screen.blit(self.walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 28, 52)
        # pg.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 50
        self.y = 410
        self.walkcount = 0
        font1 = pg.font.SysFont("calibri", 100)
        text = font1.render("-5", 1, (255, 0, 0))
        pg.draw.rect(screen,(0 ,0 ,200), (screenwidth/2 - 90, screenheight/2 - 80, 180, 150), 10)
        screen.blit(text, (screenwidth/2 - (text.get_width()/2), screenheight/2 - (text.get_height()/2)))
        pg.display.flip()
        i = 0
        while i < 100:
            pg.time.delay(10)
            i += 1
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()

class Enemy():
    walkRight = [pg.image.load('R1E.png'), pg.image.load('R2E.png'), pg.image.load('R3E.png'), pg.image.load('R4E.png'), pg.image.load(
        'R5E.png'), pg.image.load('R6E.png'), pg.image.load('R7E.png'), pg.image.load('R8E.png'), pg.image.load(
        'R9E.png'), pg.image.load('R10E.png'), pg.image.load('R11E.png')]
    walkLeft = [pg.image.load('L1E.png'), pg.image.load('L2E.png'), pg.image.load('L3E.png'), pg.image.load('L4E.png'), pg.image.load(
        'L5E.png'), pg.image.load('L6E.png'), pg.image.load('L7E.png'), pg.image.load('L8E.png'), pg.image.load(
        'L9E.png'), pg.image.load('L10E.png'), pg.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.speed = 3
        self.walkcount = 0
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.healthbar = (self.x + 17, self.y + 66, 31, 10)
        self.health = 10
        self.alive = True
        self.deathsound = pg.mixer.Sound("death.wav")

    def draw(self, screen):
        self.move()
        if self.walkcount + 1 >= 33:
            self.walkcount = 0


        if self.speed < 0:
            screen.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
            self.walkcount += 1
        else:
            screen.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
            self.walkcount += 1

        if self.alive:
            self.healthbar = (self.x + 13, self.y - 10, 3.1 * self.health, 5)
            pg.draw.rect(screen, (255, 0, 0), (self.healthbar[0], self.healthbar[1], 31, 5), 0)
            pg.draw.rect(screen, (0, 128, 50), self.healthbar, 0)

    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkcount = 0
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkcount = 0

        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # pg.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.deathsound.play()
            self.alive = False

class Projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)


def reDrawGameWindow(char, enemy, bullets, score):
    screen.blit(bg, (0, 0))
    char.draw(screen)
    if enemy.alive:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    font = pg.font.SysFont("ubuntu", 25, True)
    text = font.render(f"Score: {score}", 1, (10, 10, 230))
    screen.blit(text, (510, 0))
    pg.display.flip()


def main():

    clock = pg.time.Clock()

    char = Character(50, 410, 64, 64)
    enemy = Enemy(150, 410, 64, 64, 500)
    bullets = []
    shootLoop = 0
    score = 0

    bulletsound = pg.mixer.Sound("bullet.wav")
    hitsound = pg.mixer.Sound("hit.wav")

    pg.mixer.music.load("music.wav")
    pg.mixer.music.play(-1)

    screen.blit(bg, (0, 0))
    pg.display.flip()

    while 1:

        clock.tick(30)

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 5:
            shootLoop = 0

        for event in pg.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                pass

        for bullet in bullets:
            if screenwidth > bullet.x > 0:
                bullet.x += bullet.speed
            else:
                bullets.pop(bullets.index(bullet))
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1] and enemy.alive:
                if bullet.x + bullet.radius < enemy.hitbox[0] + enemy.hitbox[2] and bullet.x - bullet.radius > enemy.hitbox[0]:
                    enemy.hit()
                    bulletsound.play()
                    score += 10
                    bullets.pop(bullets.index(bullet))

        keys = pg.key.get_pressed()
        # Character actions
        if keys[pg.K_LEFT] and char.x > 0:
            char.x -= char.speed
            char.left = True
            char.right = False
            char.standing = False
        elif keys[pg.K_RIGHT] and char.x < screenwidth - char.width:
            char.x += char.speed
            char.left = False
            char.right = True
            char.standing = False
        else:
            char.standing = True
            char.walkCount = 0
        if not char.isJump:
            if keys[pg.K_UP]:
                char.right = False
                char.left = False
                char.isJump = True
        else:
            if char.jumpCount >= -10:
                neg = 1
                if char.jumpCount < 0:
                    neg = -1
                char.y -= (char.jumpCount ** 2) * 0.5 * neg
                char.jumpCount -= 1
            else:
                char.isJump = False
                char.jumpCount = 10
        if keys[pg.K_SPACE] and shootLoop == 0:
            if char.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                hitsound.play()
                bullets.append(Projectile(round(char.x + char.width // 2), round(char.y + char.height // 2), 6, (255, 0 , 255), facing))
            shootLoop = 1

        if char.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and char.hitbox[1] + char.hitbox[3] > enemy.hitbox[1] and enemy.alive:
            if char.hitbox[0] < enemy.hitbox[2] + enemy.hitbox[0] and char.hitbox[0] + char.hitbox[2] > enemy.hitbox[0]:
                score -= 5
                char.hit()

        reDrawGameWindow(char, enemy, bullets, score)


if __name__ == "__main__": main()

pg.quit()
