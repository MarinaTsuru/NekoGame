from pygame import *
from random import randint
from time import time as timer
import pygame

pygame.font.init()
font1 = pygame.font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = pygame.font.SysFont('Arial', 36)

pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound('fire.ogg')
img_back = "galaxy.jpg"
img_laser = "laser.png"
img_hero = "neko.png"
img_enemy = "kurage.png"
img_ast = "asteroid.png"
 
score = 0
goal = 20
lost = 0
max_lost = 10
life = 3
 

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        laser = Laser(img_laser, self.rect.centerx, self.rect.top, 50, 100, -20)
        lasers.add(laser)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 

class Laser(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
  

win_width = 700
win_height = 500
pygame.display.set_caption("Shooter")
window = pygame.display.set_mode((win_width, win_height))
background = pygame.transform.scale(pygame.image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 

monsters = pygame.sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
    

asteroids = pygame.sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
 
lasers = pygame.sprite.Group()

finish = False
run = True
 
rel_time = False

num_fire = 0  
 
while run:
    for e in pygame.event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire()
                        
                    if num_fire  >= 5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                
    if not finish:
        window.blit(background,(0,0))
    
        ship.update()
        monsters.update()
        asteroids.update()
        lasers.update()

        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        lasers.draw(window)

        if rel_time == True:
            now_time = timer()
        
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = pygame.sprite.groupcollide(monsters, lasers, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if pygame.sprite.spritecollide(ship, monsters, False) or pygame.sprite.spritecollide(ship, asteroids, False):
            pygame.sprite.spritecollide(ship, monsters, True)
            pygame.sprite.spritecollide(ship, asteroids, True)
            life = life -1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
    
    
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
    
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
    

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
    
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
    
        pygame.display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in lasers:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()   
        
        pygame.time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)   
    
    pygame.time.delay(50)