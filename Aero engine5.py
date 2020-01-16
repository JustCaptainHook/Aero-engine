import random
import pygame
import time
pygame.init()
players = 0 #so that only the menu shows not the ships or the lives
win = pygame.display.set_mode((1000,650)) #how big the screen is
pygame.display.set_caption("Aero engine") #let the title say "Aero engine"
image = pygame.image.load
font = pygame.font.SysFont("comisans", 50)
with open("hisc.txt", 'r') as f:
    highscore = int(f.read())
score = 0
backy1 = 0
backy2 = -650
darthy = 650


class Menu():
    def __init__(self):
        self.OnePlayer = image("1_player.PNG")
        self.TwoPlayers = image("2_Players.PNG")
        self.vel = 2 # what the speed is of the ship is
    def draw(self):
        global players # so that the variable players can be changed here
        mouse = pygame.mouse
        key = pygame.key.get_pressed()
        win.blit(self.OnePlayer,(400,325)) # drawing the buttons
        win.blit(self.TwoPlayers,(400,225))
        if key[pygame.K_DOWN]: # when arrow key down is pressed move to the lower button
            mouse.set_pos(500,345)
        if key[pygame.K_UP]: # when arrow key up is pressed move to the upper button
            mouse.set_pos(500,245)
        if mouse.get_pos()[0]<=614 and mouse.get_pos()[1]<=280 and mouse.get_pos()[0] >= 400 and mouse.get_pos()[1] >= 225: #P2 button coördinations
                if mouse.get_pressed()[0]: # when there is pressed on the button
                    players = 2 # two players will come
                    self.vel = 2 # let the speed be the same
                if key[pygame.K_RETURN]: # if return is pressed while the mouse is on the button
                    players = 2
                    self.vel = 2
        if mouse.get_pos()[0]<=614 and mouse.get_pos()[1]<=380 and mouse.get_pos()[0] >= 400 and mouse.get_pos()[1] >= 325: #P1 button coördinations
                if mouse.get_pressed()[0]: # when there is pressed on the button of P1
                    players = 1 # one player will come
                    self.vel = 6 # make the speed higher so that when you are in one corner you can reach the other before the ship is below the screen
                if key[pygame.K_RETURN]: # if retorn is pressed while the mouse is on the button from P1
                    players = 1
                    self.vel = 6

class Player(pygame.sprite.Sprite):
    def __init__(self, levens, ship,x,y):
        self.ship = ship # give the picture to Player
        self.rect = pygame.Rect(0, 0, 0, 0)# Give the sizes of the ship (but that is not needen because it is a picture)
        self.rect.x, self.rect.y = x, y #start ship in the middle
        self.rect.width, self.rect.height = self.ship.get_size() #start ship in the middle
        self.bullets = [Bullet(self.rect.copy(),40)] #creating bullets
        self.shooting = False #So that the bullet don't fire immediately
        self.shooting2 = False #So that the bullet don't fire immediately
        pygame.sprite.Sprite.__init__(self) #creating a sprite
        self.live = levens # give the quantity of lives to Player
        self.bullet_draw = False # so the the bullets don't draw


    def lives(self,x1,x2,x3):
        global players # so that the variable players can be changed here
        self.Heart = image("Heart.png")
        if self.live >= 1: # if lives is or is above 1 place heart
            win.blit(self.Heart, (x1, 0))
        if self.live >= 2: # if lives is or is above 2 place heart
            win.blit(self.Heart, (x2, 0))
        if self.live >= 3: # if lives is or is above 3 place heart
            win.blit(self.Heart, (x3, 0))
        if PlayerOne.live + PlayerTwo.live <= 0: # if both players have died go back to the menu
            players = 0
        if PlayerOne.live <= 0: # if P1 died take him out of the screen so that he can't lose any more lives.                
            PlayerOne.rect.y = 1000
            self.shooting = False
        if PlayerTwo.live <= 0: # same for P2
            PlayerTwo.rect.y = 1000
            self.shooting2 = False
            
    def move(self):
        sound = pygame.mixer.music.load
        key = pygame.key.get_pressed()
        #movement of the ship
        if key[pygame.K_d] and self.rect.x < 1000 - 85 - menu.vel: # when pressed d move, if the ship in the screen
            self.rect.x += menu.vel
        if key[pygame.K_s] and self.rect.y < 650 - 76 - menu.vel: # when pressed s move, if the ship in the screen
            self.rect.y += menu.vel
        if key[pygame.K_a] and self.rect.x > menu.vel: # when pressed a move, if the ship in the screen
            self.rect.x -= menu.vel
        if key[pygame.K_w] and self.rect.y > menu.vel: # when pressed w move, if the ship in the screen
            self.rect.y -= menu.vel
        # shooting of the ship
        if key[pygame.K_q] and self.shooting == False: # when pressed q and the bullet isn't already firing, fire
            pygame.mixer.init() # so that a music can play
            self.bullet_draw = True
            self.shooting = True
            sound("Blaster.mp3") # load in the music
            pygame.mixer.music.play() # play the music
        if self.shooting == 1: # if the button q has been pressed
            for bullet in self.bullets:
                bullet.rect.y -= 10
                if bullet.rect.y < self.rect.y - 650: # if the bullet is above the screen come back
                    bullet.rect.y = self.rect.y
                    bullet.rect.x = self.rect.x
                    self.shooting = False
        else: # if the bullet hasn't been fired come to the ship
            for bullet in self.bullets:
                bullet.rect.x = self.rect.x
                bullet.rect.y = self.rect.y
                self.bullet_draw = False
            
    
    def move2(self): # same as move 1 but with different inputs
        sound = pygame.mixer.music.load
        key = pygame.key.get_pressed()
        #movement of the ship
        if key[pygame.K_RIGHT] and self.rect.x < 1000 - 85 - menu.vel:
            self.rect.x += menu.vel
        if key[pygame.K_DOWN] and self.rect.y < 650 - 76 - menu.vel:
            self.rect.y += menu.vel
        if key[pygame.K_LEFT] and self.rect.x > menu.vel:
            self.rect.x -= menu.vel
        if key[pygame.K_UP] and self.rect.y > menu.vel:
            self.rect.y -= menu.vel
        # shooting of the ship
        if key[pygame.K_SLASH] and self.shooting2 == False:
            pygame.mixer.init()
            self.bullet_draw = True
            self.shooting2 = True
            sound("Blaster.mp3")
            pygame.mixer.music.play()
        if self.shooting2 == 1:
            for bullet2 in self.bullets:
                bullet2.rect.y -= 10
                if bullet2.rect.y < self.rect.y - 650: # if the bullet is above the screen come back
                    bullet2.rect.y = self.rect.y
                    bullet2.rect.x = self.rect.x
                    self.shooting2 = False      
        else:
            for bullet2 in self.bullets:
                bullet2.rect.x = self.rect.x
                bullet2.rect.y = self.rect.y
                self.bullet_draw = False

    def draw(self):
        global players
        win.blit(self.ship, (self.rect.x, self.rect.y)) # draw ship
        for bullet in self.bullets:
            if self.bullet_draw == True: # if the bullet has been fired
                bullet.draw(255,0) # draw bullet
        if players >= 1:
            PlayerOne.move()
            PlayerOne.lives(0,75,150) # the coördinates of the hearts
        if players > 1:
            PlayerTwo.move2()
            PlayerTwo.lives(925,850,775) # the coördinates of the hearts




class Power_up(pygame.sprite.Sprite):
        def __init__(self,x,y,image):
            self.power_up = image
            self.rect = pygame.Rect((x,y),self.power_up.get_rect().size)
            pygame.sprite.Sprite.__init__(self) # making a sprite of the class
            self.Power_Up_Go = False # so that the power_up doesn't go emediatly
            self.Power_Up2_Go = False

        def draw(self):
            win.blit(self.power_up, (self.rect.x,self.rect.y)) # draw the power_up
            power_up.move()
            power_up2.move2()
        def move2(self):
            if players == 2:
                if Enemy2.deaths2 + Enemy.deaths2 >= 20: # when power_up should move
                    if Enemy.speed >= 3: #when the speed is very high the power up should go
                        self.Power_Up2_Go = True
                    Enemy.deaths2 = 0 # so that the cycle beggins again
                    Enemy2.deaths2 = 0 # so that the cycle beggins again
            if players == 1:
                if Enemy2.deaths2 + Enemy.deaths2 >= 10: # when power_up should move
                    if Enemy.speed >= 3: #when the speed is very high the power up should go
                        self.Power_Up2_Go = True
                    Enemy.deaths2 = 0 # so that the cycle beggins again
                    Enemy2.deaths2 = 0 # so that the cycle beggins again
            if self.Power_Up2_Go == 1:
                power_up2.rect.y += 2
            if power_up2.rect.y >= 726: # if power_up is below the screen
                power_up2.rect.y = -76
                power_up2.rect.x = random.randint(0,915)
                power_up2.Power_Up2_Go = False
            if pygame.sprite.collide_rect(power_up2, PlayerOne) == 1: # if PlayerOne hits it
                if menu.vel < 10:
                    menu.vel += 0.50
                power_up2.rect.y = -76
                power_up2.rect.x = random.randint(0,915)
                self.Power_Up2_Go = False
                if Enemy.speed >= 3:
                    menu.vel += 0.5
            if pygame.sprite.collide_rect(power_up2, PlayerTwo) == 1: # if PlayerTwo hits it
                if menu.vel < 10:
                    menu.vel += 0.50
                self.Power_Up2_Go = False
                power_up2.rect.y = -76
                power_up2.rect.x = random.randint(0,915)
        def move(self):
            if players == 2:
                if Enemy2.deaths + Enemy.deaths >= 10: # when power_up should move
                    if Enemy.speed >= 2: #when the speed is very high the power up should go
                        self.Power_Up_Go = True
                    Enemy.deaths = 0 # so that the cycle beggins again
                    Enemy2.deaths = 0 # so that the cycle beggins again
                    Enemy2.speed += 0.25 # so that the speed changes
                    Enemy.speed += 0.25 # so that the speed changes
            if players == 1:
                if Enemy2.deaths + Enemy.deaths >= 5: # when power_up should move
                    if Enemy.speed >= 2: #when the speed is very high the power up should go
                        self.Power_Up_Go = True
                    Enemy.deaths = 0 # so that the cycle beggins again
                    Enemy2.deaths = 0 # so that the cycle beggins again
                    Enemy2.speed += 0.25 # so that the speed changes
                    Enemy.speed += 0.25 # so that the speed changes
            if self.Power_Up_Go == 1:
                power_up.rect.y += 1
            if self.rect.y == 726: # if power_up is below the screen
                power_up.rect.y = -76
                power_up.rect.x = random.randint(0,915)
                power_up.Power_Up_Go = False
            if pygame.sprite.collide_rect(power_up, PlayerOne) == 1: # if PlayerOne hits it
                if PlayerOne.live < 3: # if the lives of player one are lower than 3 give a hearth
                    PlayerOne.live += 1
                power_up.rect.y = -76
                power_up.rect.x = random.randint(0,915)
                self.Power_Up_Go = False
            if pygame.sprite.collide_rect(power_up, PlayerTwo) == 1: # if PlayerTwo hits it
                if PlayerTwo.live < 3: # if the lives of player two are lower than 3 give a hearth
                    PlayerTwo.live += 1
                self.Power_Up_Go = False
                power_up.rect.y = -76
                power_up.rect.x = random.randint(0,915)

class X_wing(pygame.sprite.Sprite):
    def __init__(self,X_wing,x,y):
        self.X_wing = X_wing
        self.rect = pygame.Rect((x,y), self.X_wing.get_rect().size)
        pygame.sprite.Sprite.__init__(self) # making a sprite of the class
        self.bullets = Bullet(self.rect.copy(),40) # so that the two rects don't collide
        self.deaths = 0
        self.deaths2 = 0
        self.speed = 1
        self.bullets = [Bullet(self.rect.copy(),40)]
        self.X_wing_Go = True
        
    def draw(self):
        global players, score
        if self.X_wing_Go == True:
            win.blit(self.X_wing, (self.rect.x, self.rect.y))# draw x wing
        if players == 1 or players == 2: # if there are 1 or 2 players, move
            Enemy.move()
        if players == 2: # if there are 2 players, move
            Enemy2.move2()
        for bullet in self.bullets:
            bullet.draw(0,255)
    def move(self):
        global players, score
        self.rect.y += self.speed# X_wing move
        if self.rect.y >= 650: # when X_wing is below screen take a life of both players
            PlayerOne.live -= 1
            PlayerTwo.live -= 1
            self.rect.y = -76
            self.rect.x = random.randint(50,915)
        if pygame.sprite.collide_rect(Enemy,PlayerOne) == 1: # when PlayerOne hits it take a live
            PlayerOne.live -= 1
            self.rect.y = -76
            self.rect.x = random.randint(50,915)
        if players > 1:
            if pygame.sprite.collide_rect(Enemy,PlayerTwo) == 1: # when PlayerTwo hits it take a live
                PlayerTwo.live -= 1
                self.rect.y = -76
                self.rect.x = random.randint(50,915)
        if pygame.sprite.collide_rect(Enemy,PlayerOne.bullets[0]) == 1: # when bullet from PlayerOne hits it, mark a death
            self.deaths += 1
            self.deaths2 += 1
            home_one.score += 1
            score += 1
            PlayerOne.shooting = False
            self.rect.y = -76
            self.rect.x = random.randint(50,915)
        if players > 1:
            if pygame.sprite.collide_rect(Enemy,PlayerTwo.bullets[0]) == 1: # when bullet from PlayerTwo hits it, mark a death
                self.deaths += 1
                self.deaths2 += 1
                home_one.score += 1
                score += 1
                PlayerOne.shooting = False
                self.rect.y = -76
                self.rect.x = random.randint(50,915)
        
    def move2(self):# same as move 1 but with different inputs
        global score
        self.rect.y += self.speed # X_wing move
        if self.rect.y >= 650: # when X_wing is below screen
            PlayerOne.live -= 1 
            PlayerTwo.live -= 1
            self.rect.y = -76
            self.rect.x = random.randint(50,915)
        if pygame.sprite.collide_rect(Enemy2,PlayerOne) == 1: # when PlayerOne hits it
            PlayerOne.live -= 1
            self.rect.y = -76
            self.rect.x = random.randint(50,915)
        if pygame.sprite.collide_rect(Enemy2,PlayerTwo) == 1: # when PlayerTwo hits it
            PlayerTwo.live -= 1
            self.rect.y = -76
            self.rect.x = random.randint(50,915)
        if pygame.sprite.collide_rect(Enemy2,PlayerOne.bullets[0]) == 1: # when bullet from PlayerOne hits it
            self.deaths += 1
            self.deaths2 += 1
            home_one.score += 1
            score += 1
            PlayerTwo.shooting2 = False
            self.rect.y = -76
            self.rect.x = random.randint(50,915)
        if pygame.sprite.collide_rect(Enemy2,PlayerTwo.bullets[0]) == 1: # when bullet from PlayerTwo hits it
            self.deaths += 1
            self.deaths2 += 1
            home_one.score += 1
            score += 1
            PlayerTwo.shooting2 = False
            self.rect.y = -76
            self.rect.x = random.randint(50,915)

class Home_one(pygame.sprite.Sprite):
    def __init__(self):
        self.image = image("Home one.png")
        self.rect = pygame.Rect((225,-450), self.image.get_rect().size)
        self.score = 0
        self.Ho_go = False
        self.Ho_x = 1
    def draw(self):
        win.blit(self.image,(self.rect.x,self.rect.y))
        home_one.move()
    def move(self):
        if self.score == 1:
            Enemy.X_wing_Go = False
            Enemy2.X_wing_Go = False
            self.Ho_go = True
            self.score = 0
        if self.Ho_go == True:
            Enemy2.rect.y = -76
            Enemy.rect.y = -76
            self.rect.y += 2
            self.Ho_x = 2
            if self.rect.y == 0:
                self.Ho_go = False
        if self.rect.y == 0:
            if self.Ho_x == 2:
                if self.rect.x <= 670:
                    self.rect.x += 2
                if self.rect.x == 669:
                    self.Ho_x = 3
            if self.Ho_x == 3:
                if self.rect.x >= 0:
                    self.rect.x -= 2
                if self.rect.x == 0:
                    self.Ho_x = 2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect, X_offset):
        pygame.sprite.Sprite.__init__(self) #making a sprite of the class
        self.rect = rect # the x and the y from the bullet
        self.X_offset = X_offset #how far the bullet is from the x of the ship

    def draw(self,G,R):
        pygame.draw.rect(win, (R,G,0),(self.rect.x+self.X_offset, self.rect.y,5,50)) #draw the bullet







PlayerOne = Player(3, image("Tiefighter1.png"),425,325)
PlayerTwo = Player(3,image("Tiefighter1.png"),525,325)
Enemy = X_wing(image("X_wing.PNG"),random.randint(50,915),-200)
Enemy2 = X_wing(image("X_wing.PNG"),random.randint(50,915),-200)
home_one = Home_one()
power_up2 =  Power_up(random.randint(0,915), -76,pygame.image.load("Power_up2.PNG"))
power_up =  Power_up(random.randint(0,915), -76,pygame.image.load("Power_up.PNG"))
menu = Menu()


run = True
while run:
    scoretext = font.render(str(score),True,(255,255,255))
    highscoretext = font.render(str(highscore),True,(255,255,255))
    key = pygame.key.get_pressed()
    win.blit(pygame.image.load("Background.png"),(0,backy1)) # make the background black
    win.blit(pygame.image.load("Background.png"),(0,backy2))
    win.blit(pygame.image.load("darth-vader-helmet.png"),(500,darthy))
    home_one.draw()
    if players >= 1: # if there are one or two players draw them
        PlayerOne.draw()
        Enemy.draw()
        power_up.draw()
        power_up2.draw()
    if players == 1:
        PlayerTwo.live = 0
    if players > 1: # if there are two players draw them
        Enemy2.draw()
        PlayerTwo.draw()
    if players == 0: # when they both died put them back on their former posisions.
        menu.draw()
        PlayerOne.live = 3
        PlayerTwo.live = 3
        Enemy.deaths = 0
        Enemy2.deaths = 0
        Enemy.rect.y = -200
        Enemy2.rect.y = -200
        PlayerOne.rect.y = 325
        PlayerOne.rect.x = 425
        PlayerTwo.rect.y = 325
        PlayerTwo.rect.x = 525
        Enemy.speed = 1
        Enemy2.speed = 1
        power_up.rect.y = -76
        score = 0
    if score > highscore:
        highscore = score
    win.blit(highscoretext,(0,620))
    win.blit(scoretext,(950,620))
    backy1 += 1
    backy2 += 1
    if backy1 == 650:
        backy1 = -650
    if backy2 == 650:
        backy2 = -650
    if key[pygame.K_j] and key[pygame.K_h]:
        if darthy >= 380:
            darthy -= 10
    else:
        if darthy <= 650:
            darthy += 10
    if key[pygame.K_0] and key[pygame.K_MINUS]:
        menu.vel = 15

    for event in pygame.event.get(): # when pressed quit
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            with open("hisc.txt", 'w') as f:
                f.write(str(highscore))
            run = False
    pygame.display.update()