#Create your own shooter

from pygame import *
from random import *
from time import time as timer

window_width = 700
window_height = 500

window = display.set_mode((window_width, window_height))

display.set_caption("Shooter Game")

background = transform.scale(image.load("galaxy.jpg"), (window_width, window_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

clock = time.Clock()

# run = input("Do you want to play a game? yes/no")
run = True
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
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
        if keys[K_RIGHT] and self.rect.x < window_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        # pass
        bullet = Bullet("bullet.png", self.rect.centerx - 4.5, self.rect.top, 10, 20, 10)
        bullets.add(bullet)

lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > window_height:
            self.rect.y = 0
            self.rect.x = randint(80, window_width - 80)
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > window_height:
            self.rect.y = 0
            self.rect.x = randint(80, window_width - 80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0 :
            self.kill()

spaceship = Player('rocket.png', 5, 380, 80, 100, 5)
finish = False

font.init()
style = font.Font(None, 36)

image_list = ["ufo.png", "rocket.png", "bullet.png"]

monsters = sprite.Group()
for i in range(1, 6):
    ufo = Enemy('ufo.png', randint(80, window_width - 80), -50, 80, 50, randint(1, 3))
    monsters.add(ufo)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid('asteroid.png', randint(80, window_width - 80), -50, 80, 50, random() + 1)
    asteroids.add(asteroid)

bullets = sprite.Group()

font1 = font.Font(None, 80)
# font2 = font.Font(None, 80)

win_message = font1.render("YOU WIN!", True, (255, 255, 255))
lose_message = font1.render("YOU LOSE!", True, (255, 0, 0))

spaceship_collision = False

lives = 3
bullets_magazine = 5
bullets_fired = 0

rel = False # Reload Flag
print(timer())
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if bullets_fired < 5 and rel == False:

                    bullets_fired += 1
                    fire_sound.play()
                    spaceship.fire()
                
                if bullets_fired >= 5 and rel == False:
                    reload_time = timer()
                    rel = True
                

    if not finish:
        window.blit(background, (0, 0))
        score_text = style.render('Score: ' + str(score), 1, (255, 255, 255))
        window.blit(score_text, (10, 20))

        loss = style.render('Missed: ' + str(lost), 1, (255, 255, 255))
        window.blit(loss, (10, 50))

        spaceship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        if rel == True:
            current_time = timer()

            if current_time - reload_time < 3:
                reload_text = style.render("Wait, reloading...", 1, (200, 0, 0))
                window.blit(reload_text, (250, 450))
            else:
                rel = False
                bullets_fired = 0


        # for monster in monsters:
        #     if monster.rect.y > window_height:
        #         monster.rect.y = 0
        #         monster.rect.x = randint(80, window_width - 80)
        #         lost = lost + 1
        #         ufo = Enemy(image_list[randint(0, len(image_list) - 1)], randint(80, window_width - 80), -50, 80, 50, randint(1, 5))
        #         monsters.add(ufo)
        #         monster.kill()
            

        spaceship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        # if spaceship_collision == True:
        #     finish = True

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for collission in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, window_width - 80), -50, 80, 50, randint(1, 3))
            monsters.add(monster)

        if score >= 10:
            finish = True
            window.blit(win_message, (200, 200))
        
        if sprite.spritecollide(spaceship, monsters, False) or sprite.spritecollide(spaceship, asteroids, False):
            sprite.spritecollide(spaceship, monsters, True)
            sprite.spritecollide(spaceship, asteroids, True)
            lives -= 1
            pass

        if lost >= 5 or lives == 0:
            # if spaceship_collision != True:

            spaceship.image = transform.scale(image.load('ufo.png'), (80, 100))
            # spaceship_collision = True
            # sleep(3)
            
            finish = True
            window.blit(lose_message, (200, 200))
        
        if lives == 3:
            lives_color = (0, 200, 0)
        
        if lives == 2:
            lives_color = (200, 200, 0)
        
        if lives == 1:
            lives_color = (200, 0, 0)

        text_lives = font1.render(str(lives), True, lives_color)
        window.blit(text_lives, (650, 10))

        display.update()
    clock.tick(FPS)