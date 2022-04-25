from pygame.locals import *
import pygame
import os

pygame.init()

W = 1000
H = 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Zombie shooter")


BG_image = pygame.image.load('BG.webp')
BG_image = pygame.transform.scale(BG_image,(W, H))




move_left = False
move_right = False

def set_image(self, filename = None):
    if(filename != None):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()


class player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img,(img.get_width() * scale, img.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, move_left, move_right):
        dx = 0
        dy = 0

        if move_left:
            dx = -self.speed
        if move_right:
            dy = self.speed

        self.rect.x += dx
        self.rect.x += dy

    def draw(self):
        screen.blit(self.image, self.rect)

pl = player(200, 200, 0.2, 1)
pl2 = player(300, 350, 0.3, 1)

run = True

def move_BG(i, BG_image):
    screen.fill((0, 0, 0))
    screen.blit(BG_image,(i, 0))
    screen.blit(BG_image, (W+i, 0))
    if (i == -W):
        screen.blit(BG_image, (W + i, 0))
        i = 0
    i -= 1

i = 0

while run:

    pl2.draw()
    pl2.move(move_left, move_right)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            
    pygame.display.update()
pygame.quit()