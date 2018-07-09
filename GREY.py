import pygame
import random
import sys

pygame.init()
screen_w=1366
screen_h=768

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
blue=(0,0,255)

screen=pygame.display.set_mode([screen_w,screen_h],pygame.FULLSCREEN)
icon = pygame.image.load('./images/icon.jpg')
pygame.display.set_icon(icon)
pygame.display.set_caption('Grey')
clock=pygame.time.Clock()

arial_25 = pygame.font.SysFont('arial',25)

ENEMYSPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMYSPAWN, 550)

SNOWSPAWN = pygame.USEREVENT + 2
pygame.time.set_timer(SNOWSPAWN, 500)

bg1 = pygame.image.load('./images/bg1.png').convert_alpha()
bg1 = pygame.transform.scale(bg1,(screen_w,screen_h))
bg2 = pygame.image.load('./images/bg2.png').convert_alpha()
bg2 = pygame.transform.scale(bg2,(screen_w,screen_h))

b1x = b1y = 0
b2x , b2y = 0,-screen_h

op1 = pygame.image.load('./images/intro.png').convert_alpha()
op2 = pygame.image.load('./images/me.png').convert_alpha()
op3 = pygame.image.load('./images/grey.png').convert_alpha()

start_sound = pygame.mixer.Sound('./audio/start.wav')
gameMusic = pygame.mixer.Sound('./audio/gameMusic.wav')
gameeasy = pygame.mixer.Sound('./audio/gameeasy.wav')
gamehard = pygame.mixer.Sound('./audio/gamehard.wav')
gamehard.set_volume(.7)
gameover_music = pygame.mixer.Sound('./audio/gameover.wav')
haha = pygame.mixer.Sound('./audio/haha.wav')
expl_sound = pygame.mixer.Sound('./audio/expl.wav')
expl_sound.set_volume(.2)
impact_sound = pygame.mixer.Sound('./audio/thud.wav')
impact_sound.set_volume(.5)
powerup = pygame.mixer.Sound('./audio/powerup.wav')
gunshot = pygame.mixer.Sound('./audio/gunshot.wav')
gunshot.set_volume(.2)
bomb = pygame.mixer.Sound('./audio/bomb.wav')
shotgun = pygame.mixer.Sound('./audio/shotgun.wav')
shotgun.set_volume(.2)

gtrack = pygame.mixer.Channel(5)

gametrack = gameeasy

muted = False
music_change = True

cloud1=pygame.image.load('./images/cloud (1).png').convert_alpha()
cloud2=pygame.image.load('./images/cloud (2).png').convert_alpha()
cloud3=pygame.image.load('./images/cloud (3).png').convert_alpha()
cloud4=pygame.image.load('./images/cloud (4).png').convert_alpha()

c1x,c1y = 0,-100
c2x,c2y = 200,350
c3x,c3y = 600,100
c4x,c4y = 700,600

all_snow = pygame.sprite.Group()

all_sprites=pygame.sprite.Group()

all_blocks=pygame.sprite.Group()

all_bullets=pygame.sprite.Group()

all_ebullets = pygame.sprite.Group()

upgrade_anim = []
for i in range(1,10):
    filename = './images/Picture{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(black)
    img = pygame.transform.scale(img,(135,135))
    upgrade_anim.append(img)

class Upgrade_anim(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = upgrade_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        self.rect.center = player.rect.center
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(upgrade_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = upgrade_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center



explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['Xlg'] = []

for i in range(9):
    filename = './images/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(black)
    img_Xlg = pygame.transform.scale(img, (210,210))
    explosion_anim['Xlg'].append(img_Xlg)
    img_lg = pygame.transform.scale(img, (95, 95))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center




class Block(pygame.sprite.Sprite):
    def __init__(self,hp,speed):
        super().__init__()
        self.image = pygame.image.load('./images/e_jet.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.radius = (self.rect.centerx - self.rect.x)
        self.hp= hp
        self.speed = speed
        self.birth = pygame.time.get_ticks()
        self.shoot = 1500

    def update(self):
        self.rect.move_ip(0,self.speed)
        if self.rect.top>screen_h:
            self.kill()
        if pygame.time.get_ticks() - self.birth > self.shoot:
            if not muted: shotgun.play()
            ebullet = Bullet(1,15,'ejet')
            ebullet.rect.centerx=self.rect.centerx
            ebullet.rect.centery=self.rect.centery
            all_ebullets.add(ebullet)
            all_sprites.add(ebullet)
            self.birth = pygame.time.get_ticks()

class Snow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./images/snow.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speedy = random.randrange(1,5)
        self.speedx = random.randrange(-2,2)
        
    def update(self):
        self.rect.centery += self.speedy
        self.rect.centerx += self.speedx
        if self.rect.right>screen_w or self.rect.left<0 or self.rect.bottom>screen_h:
            self.kill()
      

class Player(pygame.sprite.Sprite):
    def __init__(self,hp):
        super().__init__()
        self.image = pygame.image.load('./images/jet.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.radius = (self.rect.centerx - self.rect.x)
        self.hp = hp
        self.speed = 10
        self.shoot_delay = 100
        self.last_shot = pygame.time.get_ticks()
        self.machinegun = False
        
    def update(self):
        key = pygame.mouse.get_pressed()
        mouse_pos=pygame.mouse.get_pos()
        
        self.rect.centerx=mouse_pos[0]
        self.rect.centery=mouse_pos[1]

        if self.machinegun:
            if key[0] == 1:
                if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
                    if not muted:
                        gunshot.play()
                    self.last_shot = pygame.time.get_ticks()
                    bullet=Bullet(-1,50,'jet')
                    bullet.rect.centerx=player.rect.centerx
                    bullet.rect.centery=player.rect.centery
                    all_sprites.add(bullet)
                    all_bullets.add(bullet)
                
            
                

class Bullet(pygame.sprite.Sprite):
    def __init__(self,direction,speed,btype):
        super().__init__()
        self.type = btype
        if self.type == 'jet':
            if player.machinegun:
                self.image = pygame.image.load('./images/bullet2.png').convert_alpha()
            else:
                self.image=pygame.image.load('./images/bullet.png').convert_alpha()
        if self.type == 'ejet':
            self.image = pygame.image.load('./images/ebullet.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.direction = direction
        self.speed = speed

        
        
    def update(self):
        self.rect.y+=(self.direction)*self.speed
        if self.rect.bottom<0:
            self.kill()
        if self.rect.top>screen_h:
            self.kill()

class Image(pygame.sprite.Sprite):
    def __init__(self,image,center):
        super().__init__()
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center


player=Player(6)
all_sprites.add(player)
score = 0
blockspeed1 = 3
blockspeed2 = 6
barHP = 3
upgrade = 0
increment = 10


def button(msg,x,y,w,h,ap,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(screen,ac,(x-ap,y-ap,w+2*ap,h+2*ap))
        if click[0] == 1 and action != None:
            action()
            
    else:
        pygame.draw.rect(screen,ic,(x,y,w,h))
    txt = arial_25.render(msg,True,black)
    txt_rect = txt.get_rect()
    txt_rect.center = ((x+w/2),(y+h/2))
    screen.blit(txt,txt_rect)

def mute():
    global muted
    pygame.mixer.pause()
    muted = True

def unmute():
    global muted
    pygame.mixer.unpause()
    muted = False


def op():
    start = pygame.time.get_ticks()
    
    cinematic = True
    if not muted: start_sound.play(-1)
    while cinematic:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN:
                cinematic = False
        if pygame.time.get_ticks()-start<3500:
            screen.blit(op1,(0,0))
        elif 2000<pygame.time.get_ticks()-start<7000:
            screen.blit(op2,(0,0))
        else:
            screen.blit(op3,(0,0))
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                break
        pygame.display.update()
        clock.tick(60)
    if not muted: start_sound.fadeout(500)
    gameMusic.play(-1)
        



def pause():
    if not muted: 
        pygame.mixer.fadeout(1000)
        gameMusic.play()
    paused = True
    pygame.mouse.set_visible(1)
    pauseimg = pygame.image.load('./images/pauseimg.png').convert_alpha()
    pauseimg = pygame.transform.scale(pauseimg,(screen_w,screen_h))
    pause_snow = pygame.sprite.Group()
    paused = pygame.image.load('./images/paused.png')
    paused = Image(paused,(screen_w/2-400,150))
    pause_images = pygame.sprite.Group()
    pause_images.add(paused)
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == SNOWSPAWN:
                snow = Snow()
                snow.rect.centery = random.randint(0,10)
                snow.rect.centerx = random.randint(screen_w/2+300,screen_w-5)
                pause_snow.add(snow)

        screen.blit(pauseimg,(0,0))

        pause_snow.draw(screen)
        pause_snow.update()

        button('Main Menu',1050,600,300,40,3,(140,140,140),(191,191,191),menu)
        button('Resume Game',1050,650,300,40,3,(140,140,140),(191,191,191),innergame)
        button('Quit',1050,700,300,40,3,(140,140,140),(191,191,191),quitgame)
              
        pause_images.draw(screen)


        pygame.display.update()
        clock.tick(60)

def menu():

    player.kill()

    intro = True
    menu_snow = pygame.sprite.Group()
    menuimg = pygame.image.load('./images/menu.jpg').convert()

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == SNOWSPAWN:
                snow = Snow()
                snow.rect.centery = random.randint(0,10)
                snow.rect.centerx = random.randint(screen_w/2+300,screen_w-5)
                menu_snow.add(snow)


        screen.blit(menuimg,(0,0))

        menu_snow.draw(screen)
        menu_snow.update()
                
        

        #buttons#
        button('Start Game',50,450,300,40,3,(140,140,140),(191,191,191),game)
        button('Mute',50,500,300,40,3,(140,140,140),(191,191,191),mute)
        button('Un Mute',50,550,300,40,3,(140,140,140),(191,191,191),unmute)
        button('Credits',50,600,300,40,3,(140,140,140),(191,191,191),credit)
        button('Game Guide',50,650,300,40,3,(140,140,140),(191,191,191),guide)
        button('Quit',50,700,300,40,3,(140,140,140),(191,191,191),quitgame)
        ###

        pygame.display.update()
        clock.tick(60)
    if not muted: gameMusic.fadeout(500)

def credit():
    credits1=True

    menu2 = pygame.image.load('./images/menu2.jpg').convert_alpha()
    credit_snow = pygame.sprite.Group()

    creditimg = pygame.image.load('./images/credits.png')
    creditimg = Image(creditimg,(screen_w/2,400))

    credit_images = pygame.sprite.Group()
    credit_images.add(creditimg)
    
    while credits1:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == SNOWSPAWN:
                snow = Snow()
                snow.rect.centery = random.randint(0,10)
                snow.rect.centerx = random.randint(screen_w/2+300,screen_w-5)
                credit_snow.add(snow)

        screen.blit(menu2,(0,0))

        credit_snow.draw(screen)
        credit_snow.update()

        credit_images.draw(screen)

        button('Back',1050,700,300,40,3,(140,140,140),(191,191,191),menu)

        pygame.display.update()
        clock.tick(60)

        
def guide():
    guide1 = True
    guide_snow = pygame.sprite.Group()

    menu2 = pygame.image.load('./images/menu2.jpg').convert_alpha()

    guideimg = pygame.image.load('./images/guide.png')
    guideimg = Image(guideimg,(screen_w/2,350))
    guide_images = pygame.sprite.Group()
    guide_images.add(guideimg)
    
    while guide1:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == SNOWSPAWN:
                snow = Snow()
                snow.rect.centery = random.randint(0,10)
                snow.rect.centerx = random.randint(screen_w/2+300,screen_w-5)
                guide_snow.add(snow)

        screen.blit(menu2,(0,0))

        guide_snow.draw(screen)
        guide_snow.update()
            
        guide_images.draw(screen)

        button('Back',1050,700,300,40,3,(140,140,140),(191,191,191),menu)

        pygame.display.update()
        clock.tick(60)

    
def quitgame():
    pygame.quit()
    sys.exit()


def gameover():

    global score,muted

    if not muted:
        pygame.mixer.fadeout(1000)
        gameover_music.play(-1)

    EMBERSPAWN = pygame.USEREVENT + 3
    pygame.time.set_timer(EMBERSPAWN,100)

    gameoverimg = pygame.image.load('./images/died.png')
    gameoverimg = Image(gameoverimg,(screen_w/2,100))
    over_images = pygame.sprite.Group()
    over_images.add(gameoverimg)
    
    skull = pygame.image.load('./images/skull.jpg').convert_alpha()
    skull = pygame.transform.scale(skull,(1366,768))
    all_embers = pygame.sprite.Group()
    over = True
    while over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == EMBERSPAWN:
                ember = Snow()
                ember.image = pygame.image.load('./images/ember.png').convert_alpha()
                ember.rect.centery = random.randint(-5,10)
                ember.rect.centerx = random.randint(screen_w/2+300,screen_w-5)
                
                all_embers.add(ember)

        screen.blit(skull,(0,0))

        all_embers.draw(screen)
        all_embers.update()

        over_images.draw(screen)

        button('Main Menu',1050,600,300,40,3,(140,140,140),(191,191,191),menu)
        button('Try Again',1050,650,300,40,3,(140,140,140),(191,191,191),game)
        button('Quit',1050,700,300,40,3,(140,140,140),(191,191,191),quitgame)


        s_font = pygame.font.SysFont('arial',30)
        s = s_font.render("score :  "+str(score),True,(140,140,140))
        s_rect = s.get_rect()
        s_rect.center = (screen_w/2,150)
        screen.blit(s,s_rect)

        pygame.display.update()
        clock.tick(60)
    

def game():

    global player,blockspeed1,blockspeed2,barHP,upgrade,score,increment,increment,gametrack,music_change,muted
    
    all_blocks.empty()

    all_bullets.empty()

    all_ebullets.empty()

    all_sprites.empty()

    player=Player(6)
    all_sprites.add(player)
    blockspeed1 = 3
    blockspeed2 = 6
    barHP = 3
    upgrade = 0
    score = 0
    increment = 10
    gametrack = gameeasy
    pygame.time.set_timer(ENEMYSPAWN, 550)
    music_change = True
    
    innergame()


def innergame():

    global player,blockspeed1,blockspeed2,barHP,upgrade,score,increment,b1x,b1y,b2x,b2y,c1x,c2x,c3x,c4x,c1y,c2y,c3y,c4y ,gametrack,music_change,muted

    pygame.mouse.set_visible(0)
    
    hp_color = blue
    crash=False
    kill = False
    up = False
    up_flashbool = False
    expl_large = False
    machinegun = False
    smg_not = False
    g_start = True

    smg = pygame.image.load('./images/machinegun.png')
    smg = Image(smg,(screen_w/2,400))
    upgraded = pygame.image.load('./images/upgraded.png')
    upgraded = Image(upgraded,(screen_w/2,200))
    upg_images = pygame.sprite.Group()
    upg_images.add(upgraded)

    if not muted:
        pygame.mixer.fadeout(1000)
        gtrack.play(gametrack)
      

    while not crash:

        if not gtrack.get_busy():
            gtrack.play(gametrack)

        if score==increment:
            if not muted: powerup.play()
            blockspeed1 +=1
            blockspeed2 +=1
            up = True
            timer = pygame.time.get_ticks()
            upgrade +=1
            if player.hp <= 10:
                player.hp += 2
            up_flash = Upgrade_anim(player.rect.center)
            all_sprites.add(up_flash)
            if upgrade == 1:
                player.image = pygame.image.load('./images/jet2.png').convert_alpha()
                player.rect = player.image.get_rect()
                player.radius = (player.rect.centerx - player.rect.x)
            if upgrade == 2:
                player.image = pygame.image.load('./images/jet3.png').convert_alpha()
                player.rect = player.image.get_rect()
                player.radius = (player.rect.centerx - player.rect.x)
            if upgrade == 3:
                player.machinegun = True
                smg_not = True
                player.image = pygame.image.load('./images/jet4.png').convert_alpha()
                player.rect = player.image.get_rect()
                player.radius = (player.rect.centerx - player.rect.x)
            increment = score+10
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crash=True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause()

            if event.type == ENEMYSPAWN:
                block = Block(3,random.randint(blockspeed1,blockspeed2))
                
                if 60 > score >= 30:
                    block.image = pygame.image.load('./images/e_jet2.png').convert_alpha()
                    block.rect = block.image.get_rect()
                    block.radius = (block.rect.centerx - block.rect.x)
                    block.hp = 5
                
                if score>=60:
                    if music_change:
                        pygame.mixer.fadeout(1000)
                        if not muted:
                            print('music played')
                            haha.play()
                            gametrack = gamehard
                            gtrack.play(gametrack)
                        music_change = False
                    expl_large = True
                    block.image = pygame.image.load('./images/e_jet3.png').convert_alpha()
                    block.rect = block.image.get_rect()
                    block.radius = (block.rect.centerx - block.rect.x)-55
                    block.hp = 10    
                    block.speed = random.randint(3,6)
                    pygame.time.set_timer(ENEMYSPAWN,1500)
                    block.shoot = 800
                    
                
                block.rect.centerx = random.randrange(screen_w)
                block.rect.centery = random.randint(-140,-90)
                all_blocks.add(block)
                all_sprites.add(block)
                
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button == 1 and not player.machinegun:
                if not muted: gunshot.play()
                bullet=Bullet(-1,50,'jet')
                bullet.rect.centerx=player.rect.centerx
                bullet.rect.centery=player.rect.centery
                all_sprites.add(bullet)
                all_bullets.add(bullet)

        all_sprites.update()
        
        for bullet in all_bullets:
            block_hit_list=pygame.sprite.spritecollide(bullet,all_blocks,False,pygame.sprite.collide_circle)
            for block in block_hit_list:
                if not muted: impact_sound.play()
                expl = Explosion(bullet.rect.center,'sm')
                all_sprites.add(expl)
                block.hp -= 1
                bullet.kill()
                if block.hp<=0:
                    pygame.sprite.spritecollide(bullet, all_blocks, True)
                    if not muted: expl_sound.play()
                    if expl_large:
                        expl = Explosion(block.rect.center,'Xlg')
                    else:
                        expl = Explosion(block.rect.center,'lg')
                    all_sprites.add(expl)
                    bullet.kill()
                    if expl_large: score +=2
                    else: score+=1

        for ebullet in all_ebullets:
            ebullet_hit_list = pygame.sprite.spritecollide(player,all_ebullets,False,pygame.sprite.collide_circle)
            for ebullet in ebullet_hit_list:
                if not muted: impact_sound.play()
                expl = Explosion(player.rect.center,'sm')
                all_sprites.add(expl)
                player.hp -= 1
                ebullet.kill()
                if player.hp <= 0:
                    if not muted: bomb.play()
                    interval = 200
                    expl = Explosion(player.rect.center,'lg')
                    all_sprites.add(expl)
                    timi = pygame.time.get_ticks()
                    kill = True

        for bullet in all_bullets:
            bullet_ebullet_hits = pygame.sprite.spritecollide(bullet,all_ebullets,True)
            for bullet in bullet_ebullet_hits:
                expl = Explosion(bullet.rect.center,'sm')
                all_sprites.add(expl)
                bullet.kill()

        for blocks in all_blocks:
            jet_block_hit = pygame.sprite.spritecollide(player,all_blocks,True,pygame.sprite.collide_circle)
            for block in jet_block_hit:
                if not muted: expl_sound.play()
                if expl_large: expl = Explosion(block.rect.center,'Xlg')
                else: expl = Explosion(block.rect.center,'lg')
                all_sprites.add(expl)
                if expl_large:
                    player.hp -= 2
                else:
                    player.hp -= 1
                if player.hp <= 0:
                    if not muted: bomb.play()
                    interval = 200
                    expl = Explosion(player.rect.center,'lg')
                    all_sprites.add(expl)
                    timi = pygame.time.get_ticks()
                    kill = True
                   


        if kill == True:
            
            if pygame.time.get_ticks() - timi > interval:
                expl = Explosion(player.rect.center,'lg')
                all_sprites.add(expl)
                interval += 200
                
            if pygame.time.get_ticks() - timi > 1000:
                kill = False
                player.kill()
                crash = True
                pygame.mouse.set_visible(1)
                gameover()

        screen.blit(bg1,(b1x,b1y))
        screen.blit(bg2,(b2x,b2y))

        b1y += 2
        b2y += 2
        
        if b1y > screen_h : b1y = -screen_h
        if b2y > screen_h : b2y = -screen_h

        screen.blit(cloud1,(c1x,c1y))
        screen.blit(cloud2,(c2x,c2y))
        screen.blit(cloud3,(c3x,c3y))
        screen.blit(cloud4,(c4x,c4y))

        c1x+=1
        c2x+=3
        c3x+=4
        c4x+=2

        if c1x>screen_w+10: c1x = -700     
        if c2x>screen_w+10: c2x = -700
        if c3x>screen_w+10: c3x = -700
        if c4x>screen_w+10: c4x = -700
        
        
        all_snow.draw(screen)        
        all_sprites.draw(screen)


        ####  hp - bar  ####     
        if g_start:
            if not barHP>=player.hp*67:
                barHP += 7
            else:
                g_start = False
        else:
            if not barHP<=player.hp*67:
                barHP -= 5
            if not barHP>player.hp*67:
                barHP += 5
            if player.hp<=2:
                hp_color = red
            if barHP<=3:
                barHP = 3
        pygame.draw.rect(screen,hp_color,(10,10,barHP,10))
        hp_surf = arial_25.render('HP',True,white)
        screen.blit(hp_surf,(10,25))
        ####################

        #score#
        s_surf = arial_25.render("Score: "+str(score),True,white)
        screen.blit(s_surf,(10,50))
        ###

        if up:
            if smg_not:
                upg_images.add(smg)
            if pygame.time.get_ticks()-timer < 2000:
                hp_color = (191,191,191)
                upg_images.draw(screen)
            else:
                hp_color = blue
                up = False
                smg_not = False
                upg_images.remove(smg)
        
        clock.tick(60)
        pygame.display.update()
    pygame.mouse.set_visible(1)


op()
menu()

pygame.quit()
