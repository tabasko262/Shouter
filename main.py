from pygame import*
from random import randint
from time import time as timer

init()

window = display.set_mode((700, 700))#Створюємо вікно
display.set_caption('Schooter')
display.set_icon(image.load('ufo.png'))
background = transform.scale(image.load('galaxy.jpg'), (700, 700))#розтягуємо картинку на вікно

clock = time.Clock()

font.init()
font1 = font.SysFont('Arial', 20)
font2 = font.SysFont('Arial', 50)

#музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_snd = mixer.Sound('fire.ogg')


class GameSprite(sprite.Sprite):#наслідуємо і створюємо новий клас

    def __init__(self, player_img, player_x, player_y, size_x, size_y, player_speed):#конструктор класу
        super().__init__()
        self.image = transform.scale(image.load(player_img), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    
    def reset(self):#Початкові координати персоражів
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):#створюємо клас гравця
    
    def update(self):#рух гравця
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 650:
            self.rect.x += self.speed

    def fire(self):#постріли
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 9)
        bullets.add(bullet)
    


lost = 0

class Enemy(GameSprite):#створюємо клас нло

    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(50, 600)
            lost += 1
        
class Asteroid(GameSprite):#створюємо клас 

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(50, 600)
            

class Bullet(GameSprite):#створюємо клас пуль

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


#додаємо персонажів
player = Player('rocket.png', 310, 590, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(50, 600), -50, 80, 50, randint(1, 3))
    monsters.add(enemy)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(5):
    enemy1 = Asteroid('asteroid.png', randint(50, 600), -50, 80, 50, randint(2, 5))
    asteroids.add(enemy1)


life = 3

score = 0

fps = 60
game = True
finish = False
rel_time = False

life = 3
score = 0
num_fire = 0

while game:#головний цикл гри

    for e in event.get():#цикл гри
        if e.type == QUIT:#кінець гри
            game = False
        if e.type == KEYDOWN:#постріли
            if e.key == K_SPACE:
                if num_fire <= 9 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire_snd.play()
                if num_fire > 9 and rel_time == False:#початок перезарядки
                    rel_time = True
                    last_time = timer()

    if not finish:#персонажі на екрані і взаємодія з ними

        window.blit(background, (0, 0))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets .update()

        if rel_time:#перезарядка
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('Перезарядка 3 секунди...', 1, (255, 0, 0))
                window.blit(reload, (250, 500))
            else:
                rel_time = False
                num_fire = 0

        collides = sprite.groupcollide(bullets, monsters, True, True)#обробка влучань
        for col in collides:
            enemy = Enemy('ufo.png', randint(50, 600), -50, 80, 50, randint(1, 3))
            monsters.add(enemy)
            score += 1

        if sprite.spritecollide(player, asteroids, True):#обробка зіткнення астероідів з персонажем
            enemy1 = Enemy('asteroid.png', randint(50, 600), -50, 80, 50, randint(2, 5))
            asteroids.add(enemy1)
            life -= 1

        if sprite.spritecollide(player, monsters, True):#обробка зіткнення нло з персонажем
            life -= 1

        life1 = font1.render('Життя: ' + str(life), 1, (255, 255, 255))#скільки життів залишилось
        window.blit(life1, (600, 20))

        lost1 = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))#скільки пропущено
        window.blit(lost1, (10, 20))

        score1 = font1.render('Рахунок: ' + str(score), 1, (255, 255, 255))#який рахунок
        window.blit(score1, (10, 50))

        magasine = font1.render('Вистріли: ' + str(num_fire), 1, (255, 255, 255))#який патронів залишилось
        window.blit(magasine, (600, 50))

        if score >= 50:#як перемогти
            finish = True
            win = font2.render('Ти вбив всіх інопланетян!', 1, (0, 255, 0))
            win1 = font2.render('Ти збив ' + str(score) + 'НЛО', 1, (0, 255, 0))
            window.blit(win, (125, 350))
            window.blit(win1, (125, 400))

        if lost >= 5 or life <= 0:#як програти
            finish = True
            lose = font2.render('You is loser)', 1, (255, 0, 0))
            window.blit(lose, (250, 350))

        display.update()

    else:#як зробити рестарт гри
        keys = key.get_pressed()
        if keys[K_q]:
            finish = False
            life = 3
            lost = 0
            score = 0
            for b in bullets:
                b.kill()
            for m in monsters:
                m.kill()
            for a in asteroids:
                a.kill()
            for i in range(5):
                enemy1 = Enemy('asteroid.png', randint(50, 600), -50, 80, 50, randint(2, 5))
                asteroids.add(enemy1)
            for i in range(5):
                enemy = Enemy('ufo.png', randint(50, 600), -50, 80, 50, randint(1, 3))
                monsters.add(enemy)

    display.update()
    clock.tick(fps)










