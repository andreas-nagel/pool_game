import pygame
import math
from pygame.locals import *
#Testiklass, valge palli jaoks
class whiteBall(pygame.sprite.Sprite):
        def __init__ (self,imgWhiteball):
                pygame.sprite.Sprite.__init__(self)
                self.image = imgWhiteball
                self.rect = self.image.get_rect()
                self.radius=25
                self.rect.center = 452,373
                self.mask = pygame.mask.from_surface(self.image)
        def draw(self,colPoint):
                whiteGroup.add(whiteBall(self.image))
                whiteGroup.draw(screen)

        def whiteHit(self,colPoint):
                length=math.hypot(colPoint[0],colPoint[1])
                thing=(23*23+35.35533905*35.35533905-length*length)/(2*23*35.35533905)
                print(thing)
                angle=math.acos(thing)
                angle=math.degrees(angle)
                print(angle)
                
                
#Kontrollib kii tegevusi
class stick(pygame.sprite.Sprite):
        def __init__(self,angle):
                pygame.sprite.Sprite.__init__(self)
                self.image = loadpic("stick")
                self.image = pygame.transform.rotate(self.image,angle)
                self.image.get_size()                
                self.rect = self.image.get_rect()
                self.rect.center = pygame.mouse.get_pos()
                self.mask = pygame.mask.from_surface(self.image)
#Kii liikumine
        def moveStick(self,angle):
                mousePos=pygame.mouse.get_pos()
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
        def hitStick(self,mouseMoved,mouseReleased):
                #print("lahti lastud ",mouseReleased)
                #print("liikus (",mouseMoved[0],",",mouseMoved[1],")")
                        
                addPos=(2*mouseMoved[0]/2,2*mouseMoved[1]/2)

                newPos=(mouseReleased[0]-addPos[0],mouseReleased[1]-addPos[1])
                mouseReleased=newPos
                print("palju liigutati",mouseMoved)
                print("edasi liikus ",addPos)
                pygame.mouse.set_pos(newPos)
                return
                        
                        
def loadpic(name):
        if name=="poolTable":
                poolTable = pygame.image.load("piljardilaud.png")
                poolTable.convert()
                return poolTable
        if name=="whiteBall":
                whiteBall = pygame.image.load("ValgePall.png")
                whiteBall.set_colorkey((187,187,187))
                whiteBall.convert()
                return whiteBall
        if name=="stick":
                stick = pygame.image.load("Piljardikii.png")
                stick.set_colorkey((255,255,255))
                stick.convert()
                return stick
#Nagu nimi ütleb. EventLoop+Event handler
def eventLoop():
        #viimased ettevalmistused enne mängu ahela käivitamist
        imgWhiteball=loadpic("whiteBall")
        angle=0
        rotateRight=False
        rotateLeft=False
        rotSpeed=1
        mouseCliked=pygame.mouse.get_pos()
        mouseReleased=pygame.mouse.get_pos()
        leftClicked=False
        sprWhiteball=whiteBall(imgWhiteball)
        mouseCliked=pygame.mouse.get_pos()
        mouseReleased=pygame.mouse.get_pos()
        stickHit=2
        point=(0,0)

        mouseMoved=0
        #if stickHit != 10:
                #pass
                
        
        
        while 1:
                screen.blit(background(),(0,0))
                sprWhiteball.draw(point)
                sprStick=stick(angle)
                sprStick.moveStick(angle)
                
                if stickHit != 2:
                        stickHit += 1
                        print(stickHit)
                        mouseReleased=pygame.mouse.get_pos()
                        
                        sprStick.hitStick(mouseMoved,mouseReleased)
                        if stickHit==4:
                                print("Real lõpp pos",pygame.mouse.get_pos())

                #tagastab esimese punkti palli maskil, kus kokkupõrge toimus
                point = pygame.sprite.collide_mask(sprWhiteball,sprStick)
                if point != None:
                        print(point)
                        whiteBall.whiteHit(whiteBall,point)
                
                
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
                        #Kontrollib hiirenupu vajutusi
                        elif event.type == MOUSEBUTTONDOWN:
                                #Annab "speed boosti kii pööramisele
                                if pygame.mouse.get_pressed()[2]==True:
                                        rotSpeed=10

                                if pygame.mouse.get_pressed()[0]==True:
                                        mouseClickedAt = pygame.mouse.get_pos()
                                        leftClicked = True
                                        print("vajutatud ",mouseClickedAt)
                        #Kontrollib hiire nupu lahti laskmist
                        elif event.type == MOUSEBUTTONUP:
                                #Kaotab kii kiire pööramise
                                if pygame.mouse.get_pressed()[2]==False:
                                        rotSpeed=1

                                if pygame.mouse.get_pressed()[0]==False and leftClicked == True:
                                        #print("jõudsin siia")
                                        mouseReleased = pygame.mouse.get_pos()
                                        #print("lahti lastud ",mouseReleased)
                                        mouseMovedX=mouseReleased[0]-mouseClickedAt[0]
                                        mouseMovedY=mouseReleased[1]-mouseClickedAt[1]
                                        #print("liikus (",mouseMovedX,",",mouseMovedY,")")
                                        
                                        endPosX=mouseClickedAt[0]-mouseMovedX
                                        endPosY=mouseClickedAt[1]-mouseMovedY
                                        
                                        endPos=(endPosX,endPosY)
                                        mouseMoved=(mouseMovedX,mouseMovedY)
                                        print("CALCULATED lõpp pos",endPos)
                                        sprStick.hitStick(mouseMoved,mouseReleased)

                                        stickHit=-1
                                        leftClicked = False
                        
                #Viib paremale pööramise funktsioonini
                if rotateRight==True:
                        angle = stick.rotateStick(True,angle,rotSpeed)
                #Viib vasakule pööramise funktsioonini
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
        pygame.display.set_caption('Oliiviõli production aastal 20XX')
        poolTable = loadpic("poolTable")

        # Teen tausta
        
        background = pygame.Surface(screen.get_size())
        background.fill((255,255,255))
        screenHeight = screen.get_height()
        screenWidth = screen.get_width()
        
        tableHeight = poolTable.get_height()
        tableWidth = poolTable.get_width()
        #tablePosHeight = (screenHeight-tableHeight)/2
        #tablePosWidth = (screenWidth-tableWidth)/2
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


