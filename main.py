from sqlite3 import enable_shared_cache
from pygame.locals import *
import pygame

pygame.init()

GRAVITY = 0.75
FPS = 120
W = 1000
H = 500

RED = (255,0,0)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Zombie shooter")

BG_image = pygame.image.load('BG2.jpg')
BG_image = pygame.transform.scale(BG_image,(W, H))

move_left = False
move_right = False

class player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img,(img.get_width() * scale, img.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, move_left, move_right):
        dx = 0
        dy = 0

        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump == True:
            self.vel_y = -11
            self.jump = False

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
        
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)

pl = player(100, 100, 0.2, 3)

def draw_line():
    pygame.draw.line(screen, RED, (0,400), (W, 400))
run = True
i = 0
while run:
    clock.tick(FPS)

    if(move_left == True):
        screen.fill((0, 0, 0))
        screen.blit(BG_image,(i, 0))
        screen.blit(BG_image, (W+i, 0))
        if (i == +W):
            screen.blit(BG_image, (W + i, 0))
            i = 0
        i += 1
    else:
        screen.fill((0, 0, 0))
        screen.blit(BG_image,(i, 0))
        screen.blit(BG_image, (W+i, 0))
    if(move_right == True):
        screen.fill((0, 0, 0))
        screen.blit(BG_image,(i, 0))
        screen.blit(BG_image, (W+i, 0))
        if (i == -W):
            screen.blit(BG_image, (W + i, 0))
            i = 0
        i -= 1
    else:
        screen.fill((0, 0, 0))
        screen.blit(BG_image,(i, 0))
        screen.blit(BG_image, (W+i, 0))
    #draw_line()
    pl.draw()
    pl.move(move_left, move_right)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                pl.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            
    pygame.display.update()
pygame.quit()