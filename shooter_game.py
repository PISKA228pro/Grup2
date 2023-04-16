from pygame import *
from random import randint
from time import time as timer

lost = 0
score = 0
life = 3

width = 900
height = 700
win = display.set_mode((width, height))
display.set_caption("Космическая Одиссея Вити Леннова")
background = image.load("galaxy.jpg")
background = transform.scale(background, (width,height))

clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y    
   
    def reset(self):
        win.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed 
        if key_pressed[K_RIGHT] and self.rect.x < width-80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            lost += 1
            self.rect.x = randint(80,width-160)
            self.rect.y = -40

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.x = randint(80,width-160)
            self.rect.y = -40

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")    

victor = Player("rocket.png", width//2, height-100, 55, 95, 10)
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png", randint(80,width-160), -40, 80, 55, randint(1,4))
    monsters.add(monster)
for i in range(1,3):
    asteroid = Asteroid("asteroid.png", randint(80,width-160), -40, 80, 55, randint(3,6))
    asteroids.add(asteroid) 
bullets = sprite.Group()

font.init()
font1 = font.SysFont("Times New Roman",26)
font2 = font.SysFont("Tahoma",130)

game = True
finish = False

rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    victor.fire()
                    fire.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if finish != True:  
        win.blit(background,(0,0))
        victor.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        victor.reset()
        monsters.draw(win)
        asteroids.draw(win)
        bullets.draw(win)
        text_win = font1.render("Подбито: " + str(score), 1, (255,255,255))
        win.blit(text_win, (10, 10))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255,255,255))
        win.blit(text_lose, (10, 40))
        text_life = font1.render("Жизни: " + str(life), 1, (255,255,255))
        win.blit(text_life, (770, 10))

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                rel_weapon = font1.render("Внимание! Перезарядка оружия...", 1, (150, 0, 0))
                win.blit(rel_weapon, (200, 660))
            else:
                num_fire = 0
                rel_time = False
        if lost >= 3 or life < 1:
            finish = True
            text_lose = font2.render("Ты проиграл!", True, (250,0,0))
            win.blit(text_lose, (50, 300))

        if sprite.spritecollide(victor, monsters, False) or sprite.spritecollide(victor, asteroids, False):
            sprite.spritecollide(victor, monsters, True)
            sprite.spritecollide(victor, asteroids, True)
            life -= 1

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80,width-160), -40, 80, 55, randint(1,4))
            monsters.add(monster)

        if score >= 10:
            finish = True
            text_win = font2.render("Ты выиграл!", True, (0, 250, 0))
            win.blit(text_win, (50, 300))

    else:
        for monster in monsters:
            monster.kill()
        for bullet in bullets:
            bullet.kill()
        for asteroid in asteroids:
            asteroid.kill()
        lost = 0
        score = 0
        life = 3
        num_fire = 0
        rel_time = False
        finish = False
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy("ufo.png", randint(80,width-160), -40, 80, 55, randint(1,4))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Asteroid("asteroid.png", randint(80,width-160), -40, 80, 55, randint(3,6))
            asteroids.add(asteroid) 
    display.update()
    clock.tick(FPS)

        