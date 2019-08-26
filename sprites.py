print('Loading sprite')
import pygame
import os
import defaults as df
import var
import device
import random

class Sprite():
    #first try to defina image  as sprite - obsolete but some obj still need it
    def __init__(self, img, x, y, velx, vely, scalef ):
        self.x = x
        self.y = y
        self.u = velx
        self.v = vely
        self.surface = pygame.image.load (img)
        self.w = self.surface.get_rect().size[0]
        self.h = self.surface.get_rect().size[1] 
        self.scale = scalef
        w = int (float(self.w * scalef))
        h = int(float(self.h * scalef))
        self.surface = pygame.transform.scale(self.surface, (w,h ))
        self.w = self.surface.get_rect().size[0]
        self.h = self.surface.get_rect().size[1] 
        

class Sprite2(pygame.sprite.Sprite):
    #class to define simple image as sprite
    def __init__(self):

        self.file = ''
        self.image = ''
        self.w = 0
        self.h = 0
        self.rect = ''


    def set_image(self):
        self.image = pygame.image.load(self.file)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rect = self.image.get_rect()

class Sprite3(pygame.sprite.Sprite):
#generic class to create a sprite with animation properties, Run&Dead
    def __init__(self, files, x, y, u, v):
        super(Sprite3, self).__init__()
			        
		#loads lived , dead images
        self.imagesRun = self.load_images([files[0],files[1]])
        self.imagesDead = self.load_images([files[2],files[3]])
        self.files = files                        
        self.index = 0
        self.image = self.imagesRun[self.index]
        self.rect = pygame.Rect(x, y, 10, 10)
        self.u = u
        self.v = v
        self.alive = True#declares status
        self.uDefault = u
        self.col = False
        #files[0] images list names
        #files [1] images size tupla

	#load images surfaces from filesDead
    def load_images(self, files):
        imageList = []
        for item in files[0]:
            if not os.path.exists(item):
                print('***No file exists:' + item)
                pygame.quit()
                quit()
            
            images = pygame.image.load(item)
            imageList.append( pygame.transform.scale( images, files[1]))
                
        return (imageList)

    #animation def changes frames 
    def update(self):
        self.index += 1
        if self.alive:#lived animation - Run
            if self.index >= len(self.imagesRun):
                self.index = 0
            self.image = self.imagesRun[self.index]
            self.rect.w = self.files[1][0]
            self.rect.h = self.files[1][1]

        else:#dead animation
            self.u = 0
            if self.index >= len(self.imagesDead):
                self.alive = True
                self.u = self.uDefault
                self.rect.x = 0
            else:
                self.image = self.imagesDead[self.index]            
                self.rect.w = self.files[3][0]
                self.rect.h = self.files[3][1]

    def physics(self):
        if self.rect.x + self.rect.w >= df.display_width:
            if self.u > 0:
                self.rect.x -= self.u
                self.u = -self.u
                if device.audio.sound_enabled:
                    device.audio.sound_hel.play()


        if self.rect.x < 0:
            if self.u < 0:
                self.rect.x -= self.u
                self.u = -self.u
                if device.audio.sound_enabled:
                    device.audio.sound_hel.play()

class Bullet(Sprite2):
    def __init__(self):
        Sprite2.__init__(self)
        self.file = var.assetsDir + 'bullets/bullet1.png'
        self.w = 12
        self.h = 18
        self.u = 0
        self.v = 10
        self.loop_index = 0
        self.fps = 0
        self.free = False

        # newbullet = self.Sprite2(var.assetsDir + 'bullet1.png', xb, yb, 12, 18, hel.u, 9)

class Weapon():
    def __init__(self):
        self.magazine = []
        self.limit = 10
        self.x = 0
        self.y = 0
        self.uinert = 0
        self.loop_index = 0
        self.fps = 2
        self.bullet_available = 0
        self.freeBullets = []

    def load_bullets(self):
        if self.bullet_available > 0:
            for i in range(0, self.bullet_available):
                b = Bullet()
                random_enemy = int(random.random() * 1000)
                if random_enemy % 2 == 0:
                    b.file = var.assetsDir + 'bullets/bullet2.png'
                elif random_enemy % 3 == 0:
                    b.file = var.assetsDir + 'bullets/bullet3.png'
                else:
                    b.file = var.assetsDir + 'bullets/bullet1.png'

                b.set_image()
                b.rect.x = 0
                b.rect.y = -100
                self.magazine.append(b)

    def load_extra_bullet(self, amount):
        for i in range(0, amount):
            b = Bullet()
            random_enemy = int(random.random() * 1000)
            if random_enemy % 2 == 0:
                b.file = var.assetsDir + 'bullets/bullet2.png'
            elif random_enemy % 3 == 0:
                b.file = var.assetsDir + 'bullets/bullet3.png'
            else:
                b.file = var.assetsDir + 'bullets/bullet1.png'

            b.set_image()
            b.rect.x = 0
            b.rect.y = -100
            self.magazine.append(b)


    def shoot_bullet(self):
        for b in self.magazine:
            b.u = self.uinert
            b.rect.x = self.x
            b.rect.y = self.y
            self.freeBullets.append(b)
            self.magazine.remove(b)

            if device.audio.sound_enabled:
                device.audio.sound_bullet.play()

            break

        if len(self.magazine) == 0:
            print('No Ammo')


    def get_loc(self,hel):
        self.x = hel.rect.x + hel.rect.w * 0.7
        self.y = hel.rect.y + hel.rect.h * 0.9
        self.uinert = hel.u*0.85

    def moveBullets(self, dt):
        # print(len(self.magazine))
        if len(self.magazine)>0:
            # print(self.magazine)
            if self.freeBullets:
                for bullet in self.freeBullets:

                    if bullet.loop_index > bullet.fps:
                        # print(bullet.rect.x, bullet.u)
                        # bullet.u = self.uinert
                        bullet.rect.x += bullet.u * dt/10
                        bullet.rect.y += bullet.v * dt/10
                        bullet.loop_index = 0
                    else:
                        bullet.loop_index += 1

                    if bullet.rect.y + bullet.h > df.display_height:
                        # del bullet1
                        self.freeBullets.remove(bullet)
                        continue
                    var.gameDisplay.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
        
class Asprite(Sprite2):
    def __init__(self):
        Sprite2.__init__(self)

        self.files_run = []
        self.files_dead = []
        self.fileSizeDead = (0,0)
        self.fileSizeRun = (0, 0)

        self.index = 0

        # pygame.image.load(self.files_run[0])
        # self.rect = self.image.get_rect()

        self.u = 0
        self.v = 0
        self.alive = True  # declares status
        self.uDefault = 9
        self.col = False
        self.imagesRun = []
        self.imagesDead = []
        self.imagesAttack = []
        # self.rect = self.image.get_rect()
        # self.rect.x = 20
        # self.rect.y = df.display_height*0.1
        # self.rect.w = 0
        # self.rect.h = 0
        self.sound = device.audio.sound_hel
        self.loop_index = 0
        self.fps = 2
        self.life = 100

    def load_images(self):

        self.set_image()
        self.rect.x = 20
        self.rect.y = df.display_height * 0.1

        for item in self.files_run:
            images = pygame.image.load(item)
            self.imagesRun.append(pygame.transform.scale(images, self.fileSizeRun))

        if self.files_dead:
            for item in self.files_dead:
                images = pygame.image.load(item)
                self.imagesDead.append(pygame.transform.scale(images, self.fileSizeDead))


    def animate(self, dt):

        if self.alive:  # lived animation - Run
            if self.loop_index > self.fps:
                if self.files_run:
                    if self.index < len(self.files_run):
                        self.image = self.imagesRun[self.index]
                        self.index += 1
                    else:
                        self.index = 0

                self.loop_index = 0
            else:
                self.loop_index += 1

            # if self.w != self.fileSizeRun[0]:
            #     self.rect.w = self.fileSizeRun[0]
            #
            # if self.h != self.fileSizeRun[1]:
            #     self.rect.h = self.fileSizeRun[1]
        else:
            if self.u!=0:
                self.index = 0
                self.u = 0
            # print(self.files_dead,len(self.files_dead),self.index,'index')
            if self.files_dead:
                if self.loop_index > self.fps:
                    if self.index < len(self.files_dead):
                        self.image = self.imagesDead[self.index]
                        self.index += 1
                    # else:
                    #     self.index = 0
                    #     self.col = True

                    if self.rect.w != self.fileSizeDead[0]: self.rect.w = self.fileSizeDead[0]
                    if self.rect.h != self.fileSizeDead[0]: self.rect.h = self.fileSizeDead[1]
                    self.loop_index = 0
                else:
                    self.loop_index += 1

        self.move(dt)
        self.draw()

    def move(self, dt):
        # print(self.u)
        if self.rect.x + self.rect.w >= df.display_width:
            if self.u > 0:
                self.rect.x -= self.u
                self.u = -self.u
                if device.audio.sound_enabled: self.sound.play()

        if self.rect.x < 0:
            if self.u < 0:
                self.rect.x -= self.u
                self.u = -self.u
                if device.audio.sound_enabled: self.sound.play()

        if self.rect.y + self.rect.h + 100 >= df.display_height:
            if self.v > 0:
                self.rect.y -= self.v

                if device.audio.sound_enabled: self.sound.play()
        if self.rect.y < 0:
            if self.v < 0:
                self.rect.y -= self.v
                self.v = -self.v
                if device.audio.sound_enabled: self.sound.play()

        self.rect.x += self.u * dt/10
        self.rect.y += self.v * dt/10

    def draw(self):
        var.gameDisplay.blit(self.image, (self.rect.x, self.rect.y))


    def decrease_life(self,damage_rate):
        print('under attack!')
        self.life -= damage_rate

class Vehicle(Asprite):
    def __init__(self):
        Asprite.__init__(self)
        self.files_run = [var.assetsDir + 'helicopter1.png']
        self.files_run.append(var.assetsDir + 'helicopter2.png')
        self.files_run.append(var.assetsDir + 'helicopter3.png')
        self.files_run.append(var.assetsDir + 'helicopter4.png')
        self.fileSizeRun = (210, 62)
        self.fileSizeDead = (0, 0)
        self.file = self.files_run[0]
        self.w = 210
        self.h = 62



class House (Asprite):
    def __init__(self):
        Asprite.__init__(self)
        asset_path = var.assetsDir + "/house"

        file_name = ['alive_01.png', 'alive_02.png', 'alive_03.png', 'alive_04.png', 'alive_05.png', 'alive_06.png',
                     'alive_07.png', 'alive_08.png', 'alive_09.png','alive_10.png', 'alive_11.png','alive_12.png',
                     'alive_13.png','alive_14.png']
        self.files_run = [asset_path + '/' + e for e in file_name]
        self.fileSizeRun = (300, 250)

        file_name = ['dead_01.png', 'dead_02.png', 'dead_03.png', 'dead_04.png', 'dead_05.png', 'dead_06.png',
                     'dead_07.png', 'dead_08.png', 'dead_09.png','dead_10.png', 'dead_11.png','dead_12.png',
                     'dead_13.png','dead_14.png','dead_14.png']
        self.files_dead = [asset_path + '/' + e for e in file_name]
        self.fileSizeDead = (300, 250)

        self.w = self.fileSizeRun[0]
        self.h = self.fileSizeRun[1]

        self.u = 0
        self.y = 0
        self.index = 0
        self.buffer_index = -1
        self.life = 100
        self.file = self.files_run[0]

    def set_position(self):
        self.rect.x = df.display_width - self.rect.w
        self.rect.y = df.display_height - self.rect.h - self.gap

    def animate(self):
        if self.alive:
            if self.life > 90:
                self.index = 0
            elif self.life > 80:
                self.index = 1
            elif self.life > 60:
                self.index = 2
            elif self.life > 40:
                self.index = 3
            elif self.life > 30:
                self.index = 4
            elif self.life > 28:
                self.index = 5
            elif self.life > 26:
                self.index = 6
            elif self.life > 24:
                self.index = 7
            elif self.life > 22:
                self.index = 8
            elif self.life > 20:
                self.index = 9
            elif self.life > 15:
                self.index = 10
            elif self.life > 10:
                self.index = 11
            elif self.life > 5:
                self.index = 12
            else:
                self.index = 13

            if self.index != self.buffer_index: #optimization
                self.image = self.imagesRun[self.index]
                self.buffer_index = self.index

            # if device.stats.life <= 0:
            if self.life <= 0:
                self.index = 0
                self.alive = False
        else:

            if self.index < len(self.imagesDead):
                self.image = self.imagesDead[self.index]
                self.index += 1
            # else:
                # device.stats.dead_player = True
        # device.stats.life = self.life
        self.draw()

class Ammo(Sprite2):
    def __init__(self):

        Sprite2.__init__(self)

        self.file = 'assets/bullets/box5.png'
        self.w = 50
        self.h = 50

    def draw(self):
        var.gameDisplay.blit(self.image, (self.rect.x, self.rect.y))


