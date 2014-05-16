import pygame
import math
from pygame.locals import *
#Testiklass, valge palli jaoks
class whiteBall(pygame.sprite.Sprite):
        def __init__ (self):
                pygame.sprite.Sprite.__init__(self)
                self.image = loadpic("whiteBall")
                self.image.set_colorkey((187,187,187))
                self.rect = self.image.get_rect()
                self.radius=25
        def move(self):
                pass
                
                
#Kontrollib kii tegevusi
class stick(pygame.sprite.Sprite):
        def __init__(self,angle):
                pygame.sprite.Sprite.__init__(self)
                self.image = loadpic("stick")
                self.image = pygame.transform.rotate(self.image,angle)
                self.image.get_size()                
                self.rect = self.image.get_rect()
                self.rect.center = pygame.mouse.get_pos()
#Kii liikumine
        def moveStick(self,angle):
                mousePos=pygame.mouse.get_pos()
                #self.image = pygame.transform.rotate(self.image,angle)
                self.rect.center = mousePos
                stickGroup.add(stick(angle))
                stickGroup.draw(screen)
        def rotateStick(self,angle,speed):
                if self==True:
                        angle -= speed
                        if angle>=-360:
                                angle += 360
                        
                        #print(angle)
                        #stickImg = pygame.transform.rotate(stickImg,-1)
                        return angle
                else:
                        angle += speed
                        if angle<=360:
                                angle += 360
                        #print(angle)
                        #stickImg = pygame.transform.rotate(stickImg,1)
                        return angle
                        
                
                
#Kii löök
        def hitStick(self,mouseClicked,mouseReleased):
                print("lahti lastud ",mouseReleased)
                mouseMovedX=mouseReleased[0]-mouseClicked[0]
                mouseMovedY=mouseReleased[1]-mouseClicked[1]
                print("liikus (",mouseMovedX,",",mouseMovedY,")")                
                return
                        
                        
def loadpic(name):
        if name=="poolTable":
                poolTable = pygame.image.load("piljardilaud.png")
                poolTable.convert()
                return poolTable
        if name=="whiteBall":
                whiteBall = pygame.image.load("ValgePall.png")
                whiteBall.convert()
                return whiteBall
        if name=="stick":
                stick = pygame.image.load("Piljardikii.png")
                stick.set_colorkey((255,255,255))
                stick.convert()
                return stick
#Nagu nimi ütleb. EventLoop+Event handler
def eventLoop():
        angle=0
        rotateRight=False
        rotateLeft=False
        rotSpeed=1
        while 1:
                screen.blit(background(),(0,0))
                whiteBall()
                sprStick=stick(angle)
                sprStick.moveStick(angle)
                mouseCliked=pygame.mouse.get_pos()
                mouseReleased=pygame.mouse.get_pos()                
                
                for event in pygame.event.get():
                        if event.type == QUIT:
                                return
                        #väljumine
                        elif event.type == KEYDOWN and event.key == K_ESCAPE:
                                return
                        #kii pööramine paremale
                        elif event.type == KEYDOWN and event.key == K_RIGHT:
                                rotateRight=True
                                #stickImg = stick.rotateStick(True,stickImg)
                                #angle = stick.rotateStick(True,angle)
                        #kii pööramine vasakule       
                        elif event.type == KEYDOWN and event.key == K_LEFT:
                                rotateLeft=True
                                #angle = stick.rotateStick(False,angle)
                                #stickImg = stick.rotateStick(False,stickImg)
                                
                        #Lõpetab kii pööramise paremale
                        elif event.type == KEYUP and event.key == K_RIGHT:
                                rotateRight=False
                        #Lõpetab kii pööramise vasakule
                        elif event.type == KEYUP and event.key == K_LEFT:
                                rotateLeft=False
                        #Kontrollib hiirenumpu vajutusi
                        elif event.type == MOUSEBUTTONDOWN:
                                #Annab "speed boosti kii pööramisele
                                if pygame.mouse.get_pressed()[2]==True:
                                        rotSpeed=10

                                if pygame.mouse.get_pressed()[0]==True:
                                        mouseClicked = pygame.mouse.get_pos()
                                        print("vajutatud ",mouseClicked)
                        #Kontrollib hiire nupu lahti laskmist
                        elif event.type == MOUSEBUTTONUP:
                                #Kaotab kii kiire pööramise
                                if pygame.mouse.get_pressed()[2]==False:
                                        rotSpeed=1

                                if pygame.mouse.get_pressed()[0]==False:
                                        mouseReleased = pygame.mouse.get_pos()
                                        sprStick.hitStick(mouseClicked,mouseReleased)
                        

                if rotateRight==True:
                        angle = stick.rotateStick(True,angle,rotSpeed)

                if rotateLeft==True:
                        angle = stick.rotateStick(False,angle,rotSpeed)
                
                pygame.display.update()      
        
def main():
        global stickGroup, screen, whiteGroup, BallGroup
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1440, 768))  
        background()
        BallGroup = pygame.sprite.Group()
        whiteGroup = pygame.sprite.GroupSingle()
        stickGroup = pygame.sprite.GroupSingle()
        eventLoop()
        return
        # Event loop
        
def background():
        # Loon ekraani
        pygame.display.set_caption('Kunagi saab sinust Piljard poeg')
        poolTable = loadpic("poolTable")

        # Teen tausta
        
        background = pygame.Surface(screen.get_size())
        background.fill((255,255,255))
        screenHeight = screen.get_height()
        screenWidth = screen.get_width()
        
        tableHeight = poolTable.get_height()
        tableWidth = poolTable.get_width()
        tablePosHeight = (screenHeight-tableHeight)/2
        tablePosWidth = (screenWidth-tableWidth)/2
        background.blit((poolTable),(screenWidth/2-tableWidth/2,screenHeight/2-tableHeight/2))
        #background.blit((whiteBall().image),(430,350))

        # Pealkiri (miks üldse?)
        font = pygame.font.Font(None, 36)
        text = font.render("Vägev piljardilaud", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        return background

if __name__ == '__main__': main()
pygame.quit()


