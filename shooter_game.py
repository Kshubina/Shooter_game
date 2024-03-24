from pygame import *
from random import *

mixer.init()
mixer.music.load("Cool_song_forever.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

score = 0
lost = 0

max_lost = 15
goal = 75

img_back = 'bacround.jpg'
img_hero = 'Pains.png'
img_enemy = '8_Ball.png'
img_bullet = 'Cat.png'
img_enemy1 = 'monster1.png'


font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 35)
win = font1.render('БИЛЛ ПОВЕРЖАН', True, (255, 182, 193))
lose = font1.render('БИЛЛ ПОБЕДИЛ', True, (89, 89, 89))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 30, 30, -15)
        bullets.add(bullet)
    
    

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_widht-80)
            self.rect.y = 0
            lost = lost + 1

class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()




win_widht = 1000
win_height = 700
display.set_caption("ТОП ИГРА")
window = display.set_mode((win_widht, win_height))
background = transform.scale(image.load(img_back), (win_widht, win_height))
ship = Player(img_hero, 5, win_height-100, 90, 115, 20)
finish = False
game = True
clock = time.Clock()
FPS = 100

monsters = sprite.Group()
for i in range(2):
    monster = Enemy(img_enemy, randint(50, win_widht - 80), -40, 80, 90, randint(1,5))
    monster1 = Enemy(img_enemy1, randint(80, win_widht - 80), -40, 80, 90, randint(1,5))
    monsters.add(monster)
    monsters.add(monster1)

bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if finish != True:
        window.blit(background, (0, 0))

        text = font2.render('Счёт: '  + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущенно: '+ str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        monsters.update()
        monsters.draw(window)



        ship.update()
        ship.reset()

        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score = score+1
            monster = Enemy(img_enemy, randint(80, win_widht - 80), -40, 80, 90, randint(1,5))
            monster1 = Enemy(img_enemy1, randint(80, win_widht - 80), -40, 80, 90, randint(1,5))
            monsters.add(monster)
            monsters.add(monster1)
            
        if sprite.spritecollide(ship, monsters, False) or lost>=max_lost:
            finish = True
            window.blit(lose, (295, 340))
        if score >= goal:
            finish = True
            window.blit(win, (295, 340))
        

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        time.delay(3000)
        for i in range(1, 3):
            monster = Enemy(img_enemy, randint(80, win_widht - 80), -40, 80, 90, randint(1,5))
            monster1 = Enemy(img_enemy1, randint(80, win_widht - 80), -40, 80, 90, randint(1,5))
            monsters.add(monster)
            monsters.add(monster1)

    #Пухля краш:) 
    time.delay(50)