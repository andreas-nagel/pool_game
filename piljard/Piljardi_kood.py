import pygame
import math
from pygame.locals import *


# Klass, kirjeldab mängus kasutatavaid palle. Kõik klassi sees olevad muutujad
# on inglise keelest tõlkides ennast ise seletavad
class ball_class(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.radius = 35 #image.get_width()/2
        self.rect = pygame.Rect(pos, image.get_size())
        self.pos = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 0
        self.direction_x = 1
        self.direction_y = 1


#Klass mis kirjeldab kiid.
class stick_class(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = pygame.Rect(pos, image.get_size())


#Programmi esimene funktsioon, paneb tööle pygame ja kutsub välja järgmise funktsiooni
def main():
    pygame.init()
    load_files()


#Funktsioon, mis leiab palli keskpunkti
def ball_center(white_rect):
    ball_center = (white_rect[0]+25, white_rect[1]+25)
    return ball_center


#Funktsioon, mis laeb sisse pildifailid ning konverteerib need pygamele sobivasse vormi ning kutsub välja järgmise funktsiooni
def load_files():
    screen = pygame.display.set_mode((1440, 768))
    img_pool_table = pygame.image.load('piljardilaud.png')
    img_pool_table.convert_alpha()
    img_white_ball = pygame.image.load('Valgefeil.png').convert()
    img_white_ball.set_colorkey((img_white_ball.get_at((0, 0))), RLEACCEL)
    img_white_ball.convert_alpha()
    img_stick = pygame.image.load('kii_vol2.png').convert()
    img_stick.set_colorkey(img_stick.get_at((0, 0)), RLEACCEL)
    img_stick.convert_alpha()
    ball_images = [None]*15
    for i in range(1, 16):
        ball_images[i-1] = pygame.image.load(str(i) + 'ball.png')
        ball_images[i-1].convert_alpha()
    prepare(img_pool_table, img_white_ball, img_stick, screen, ball_images)


#Ette valmistav funktsioon, mis eelväärtustab vajalikud muutujad ning loob taustapildi mängu esimeseks hetkeks.
# Funktsioon kutsub välja järgmise funktsiooni, mis on mängu töös hoidev kordus.
def prepare(img_pool_table, img_white_ball, img_stick, screen, ball_images):
    pygame.display.set_caption('Thori haamer ei sobi siia üldse')
    screen_size = screen.get_size()
    #background = pygame.transform.scale(imgPoolTable,(math.round(screenSize[0]/1.5),math.round(screenSize[1]/1.5)))
    background = pygame.Surface(screen_size)
    screen_height = screen.get_height()
    screen_width = screen.get_width()
    table_height = img_pool_table.get_height()
    table_width = img_pool_table.get_width()
    background.fill((255, 255, 255))
    background.blit(img_pool_table, (screen_width / 2 - table_width / 2, screen_height / 2 - table_height / 2))
    screen.blit(background, (0, 0))

    #loon siin objekti kii klassi järgi
    stick = stick_class(img_stick, pygame.mouse.get_pos())
    stick_group = pygame.sprite.Group(stick)
    white_position = (int(screen_width/3.185) - img_white_ball.get_width()/2, table_height/2 + img_white_ball.get_height())
    white_ball = ball_class(img_white_ball, white_position)
    white_group = pygame.sprite.GroupSingle(white_ball)
    pressed_pos = (0, 0)
    walls = make_walls()
    balls = make_balls(ball_images)
    ball_group = pygame.sprite.Group(white_ball)
    for i in range(15):
        ball_group.add(balls[i])
    main_loop(stick, background, screen, stick_group, white_ball, white_group,
              img_stick, pressed_pos, walls, ball_group, balls)


# See funktsioon loob pallid vastavalt klassile "ball_class"
def make_balls(images):
    balls = [None]*15
    balls[0] = ball_class(images[0], (857, 364))
    balls[1] = ball_class(images[1], (901, 389))
    balls[2] = ball_class(images[2], (945, 414))
    balls[3] = ball_class(images[3], (989, 439))
    balls[4] = ball_class(images[4], (989, 339))
    balls[5] = ball_class(images[5], (1033, 464))
    balls[6] = ball_class(images[6], (1033, 364))
    balls[7] = ball_class(images[7], (945, 364))
    balls[8] = ball_class(images[8], (1033, 264))
    balls[9] = ball_class(images[9], (901, 339))
    balls[10] = ball_class(images[10], (945, 314))
    balls[11] = ball_class(images[11], (989, 389))
    balls[12] = ball_class(images[12], (989, 289))
    balls[13] = ball_class(images[13], (1033, 414))
    balls[14] = ball_class(images[14], (1033, 314))
    return balls


#See funktsioon loob seinad, millelt pall tagasi põrkab. VAJAB TÄPSUSTAMIST!
def make_walls():
    top_wall = pygame.Rect(300, 0, 850, 150)
    left_wall = pygame.Rect(0, 200, 255, 315)
    bottom_wall = pygame.Rect(300, 567, 850, 200)
    right_wall = pygame.Rect(1134, 190, 255, 390)
    walls = [top_wall, left_wall, bottom_wall, right_wall]
    return walls


# Mängu põhifunktsioon, hoiab mängu töös. See kutsub vastavalt toimuvale välja teised funktsioonid.
def main_loop(stick, background, screen, stick_group, white_ball, white_group,
              img_stick, pressed_pos, walls, ball_group, balls):
    angle = 0.0

    # Mängu juhtiva korduse algus
    while True:
        for event in pygame.event.get():

            # Mängust lahkumine, kui vajutatakse x-le mängu nurgas
            if event.type == QUIT:
                return

            # Tegevused, kui liigutatakse hiirt
            if event.type == MOUSEMOTION:

                # See käsk leiab hiire positsiooni antud hetkel
                mouse_pos = pygame.mouse.get_pos()

                # See käsk tekitab lisab pildile tausta
                screen.blit(background, (0, 0))

                # See käsk leiab kii nurga y telje suhtes
                angle = calc_angle(mouse_pos, white_ball.rect) + 90

                # Kutsub esile funktsiooni, mis pöörab kiid
                rotate_stick(stick, mouse_pos, white_ball.rect, img_stick, angle)

                #Käsud, mis kuvavad kõik liikuvad osad pildile.
                white_group.draw(screen)
                ball_group.draw(screen)
                stick_group.draw(screen)

                # Prindib mängu hetkeseisu ekraanil välja
                pygame.display.update()

            # Paneb mängu kinni, kui vajutatakse Escape nuppu
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            # Suunab tegevusi, kui vajutatakse alla üks hiireklahvidest
            elif event.type == MOUSEBUTTONDOWN:
                pressed_pos = pygame.mouse.get_pos()

                # Kutsub välja funktsiooni, mis määrab kii liikumist, kui seda pallist eemale tõmmatakse ning leiab ka
                # löögi tugevuse vastavalt sellele kui kaugele kii tõmmatakse
                hit_power = pull_stick(angle, pressed_pos, white_ball.rect, stick, stick_group, screen,
                                       background, white_group, ball_group)

                # Funktsioon, mis kutsub esile kii löögi ning liigutab ka palle
                strike(angle, hit_power, stick, white_ball, walls, screen, background,
                       white_group, stick_group, ball_group, balls)

                #Kuvab tausta, pallid ning kii ekraanile
                screen.blit(background, (0, 0))
                white_group.draw(screen)
                ball_group.draw(screen)
                stick_group.draw(screen)
                pygame.display.update()

            # Välistab programmi seisma jäämise kõigil muudel juhtudel
            else:
                pass


# Löögi funktsioon, arvutab kii kauguse pallist ning leiab pallide liikumisi
def strike(angle, hit_power, stick, white_ball, walls, screen, background,
           white_group, stick_group, ball_group, balls):

    # Kirjeldab väljaku pygame Rect muutujana
    game_field = pygame.Rect(245, 140, 960, 585)

    # Juhul kui kiid ei liigutatud, läheb käiku see funktsioon ning pöörab kii vale nurga alla, et näidata
    # vajutuse toimumist kuid löögi mitte toimumist
    if hit_power == 0:

        #Pöörab kiid
        rotate_stick(stick, pygame.mouse.get_pos(), white_ball.rect, stick.image, angle)
        return

    # Juhul, kui kiid tagasi tõmmati toimub löök
    else:

        # Leiab palli kiiruse ning suunad
        white_ball.speed = math.sqrt(hit_power)/1.5
        white_ball.direction_x = 1
        white_ball.direction_y = 1
        moving_balls = pygame.sprite.Group()

        # Alustab kordust, mis kestab, kuni valge pall liigub
        while white_ball.speed > 0:

            #Leiab valge palli uue positsiooni
            white_ball.rect[0] -= white_ball.speed*math.sin(math.radians(angle)) * white_ball.direction_x
            white_ball.rect[1] += white_ball.speed*math.cos(math.radians(angle)) * white_ball.direction_y

            # Vähendab valge palli kiirust
            white_ball.speed -= 0.1

            # Kontrollib, kas valge pall põrkab uues kohas kokku seinaga
            check_wall_collision(white_ball, walls)

            # Kontrollib, kas valge pall on väljakul. Kui ei, siis liigutab edasi teisi palle ning
            # eemaldab valge palli väljakult
            if not game_field.collidepoint(white_ball.rect[0], white_ball.rect[1]):
                white_ball.speed = 0
                moving_balls.remove(white_ball)

                # Liigutab edasi teisi palle
                for ball in moving_balls:
                    while ball.speed > 0:

                        # Kutsub esile funktsiooni, mis liigutab teisi palle, peale valge palli
                        ball_group = move_balls(moving_balls, ball_group, walls, game_field)

                        # Kuvab kogu info ekraanile
                        screen.blit(background, (0, 0))
                        white_group.draw(screen)
                        ball_group.draw(screen)
                        moving_balls.draw(screen)
                        stick_group.draw(screen)
                        pygame.display.update()

                # Laseb valge palli tagasi väljakule asetada
                reset_white_ball(white_ball, white_group, screen, background, ball_group, stick_group)

            #kontrollib kas liikuvad pallid põrkavad kokku seisvate pallidega
            collision = check_ball_collision(ball_group, white_group, white_ball, balls)

            # lisab pallid, mis kokku põrkasid, sobivasse gruppi
            for ball in collision:
                if ball not in moving_balls:
                    moving_balls.add(ball)
                    ball_group.remove(ball)

            # Liigutab tavalisi mängu palle
            ball_group = move_balls(moving_balls, ball_group, walls, game_field)

            #Kuvab kogu mängu pildi ekraanile
            screen.blit(background, (0, 0))
            white_group.draw(screen)
            ball_group.draw(screen)
            moving_balls.draw(screen)
            stick_group.draw(screen)
            pygame.display.update()

        #Liigutab teisi palle, kui nad ei ole oma liikumist lõpetanud selleks hetkeks, kui valge pall seisma jääb
        for ball in moving_balls:
            #print(ball.speed)
            while ball.speed > 0:
                ball_group = move_balls(moving_balls, ball_group, walls, game_field)
                screen.blit(background, (0, 0))
                white_group.draw(screen)
                ball_group.draw(screen)
                moving_balls.draw(screen)
                stick_group.draw(screen)
                pygame.display.update()
        return

#Funktsioon, mis juhib valge palli tagasi väljakule asetamist
def reset_white_ball(white_ball, white_group, screen, background, ball_group, stick_group):

        # Eemaldab valge palli mängust
        ball_group.remove(white_ball)
        screen.blit(background, (0, 0))
        ball_group.draw(screen)
        stick_group.draw(screen)

        # Kordus, mis ootab hiireklõpsu, et pall tagasi väljakule asetada
        while True:
            for event in pygame.event.get():

                #Kui hiir lastakse lahti, siis annab valgele pallile uue positsiooni
                if event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    white_ball.rect[0] = pos[0]
                    white_ball.rect[1] = pos[1]
                    white_group.draw(screen)
                    pygame.display.update()
                    return

                # Kui hiir liigub siis liigutab koos sellega ka valget palli, ning kuvab ta uues asukohas välja
                elif event.type == MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    white_ball.rect[0] = pos[0]
                    white_ball.rect[1] = pos[1]
                    screen.blit(background, (0, 0))
                    ball_group.draw(screen)
                    white_group.draw(screen)
                    stick_group.draw(screen)
                    pygame.display.update()

                # Programmist väljumine, kui vajutatakse x-i üleval nurgas
                elif event.type == QUIT:
                    pygame.quit()

        # Lisab valge palli tagasi pallide hulka, mis on mängus
        ball_group.add(white_ball)


# Funktsioon, mis kontrollib pallide kokkupõrkeid
def check_ball_collision(ball_group, moving_ball_group, white_ball, balls):
    ball_group.remove(white_ball)

    # Käsk, mis leiab omavahel kokkupõrkuvad pallid, kehtib vaid juhul, kui üks pall seisab paigal ja teine liigub.
    colliders = pygame.sprite.groupcollide(ball_group, moving_ball_group, False, False, pygame.sprite.collide_circle)

    # Arvutab vastavalt põrkele pallide kiirused
    calc_speed(colliders)
    for ball in moving_ball_group:
        pass
    ball_group.add(white_ball)
    return colliders


#Kohtrollib palli kokkupõrkeid seinadega.
def check_wall_collision(white_ball, walls):
    wall_collision = -1

    #Kordus, mis kontrollib, millise seinaga, kokkupõrge toimub.
    for i in range(0, len(walls)):
        if walls[i].collidepoint(white_ball.rect[0], white_ball.rect[1]):
            #print("kokkupõrge", i)
            wall_collision = i

    # Kui sein on horisontaalne, siis muudab palli suunda vastavalt kokkupõrkele horisontaalse seinaga
    if wall_collision == 0 or wall_collision == 2:
            white_ball.direction_y *= -1

            # Kokkupõrge ülemise seinaga
            if wall_collision == 0:
                white_ball.rect[1] += walls[0][3] - white_ball.rect[1]

            #Kokkupõrge alumise seinaga
            elif wall_collision == 2:
                #white_ball.rect[1] -= screen - walls[2][]
                pass

    # kui tegu on vertikaalse seinaga siis muudab palli suunda vastavalt sellele kokkupõrkele
    elif wall_collision == 1 or wall_collision == 3:
        white_ball.direction_x *= -1
        if wall_collision == 1:
            white_ball.rect[0] += walls[1][2] - white_ball.rect[0]
        elif wall_collision == 3:
            pass


# Arvutab kokkupõrganud pallide kiirused pärast kokkupõrget
def calc_speed(colliders):
    for item in colliders:

        # Eraldab dictionary tüüpi muutujast esimese palli ja teise palli
        first_collider = item
        second_collider = colliders[first_collider][0]

        # Arvutab välja pallide kiirused enne kokkupõrget
        first_speed = [first_collider.speed*math.sin(math.radians(first_collider.speed)),
                       first_collider.speed*math.cos(math.radians(first_collider.speed))]
        second_speed = [second_collider.speed*math.sin(math.radians(second_collider.speed)),
                        second_collider.speed*math.cos(math.radians(second_collider.speed))]

        # Arvutab välja kokkupõrkel tekkiva kolmnurga küljed, mida kasutatakse, et
        # leida pallide kiirused pärast kokkupõrget
        dx = first_collider.rect[0]-second_collider.rect[0]
        dy = first_collider.rect[1]-second_collider.rect[1]
        dx_dy = math.hypot(dx, dy)

        # Arvutab välja pallide kiirused vastavalt täisnurksele kolmnurgale, nende siinusele ja koosiinusele
        first_speed[0] = second_collider.speed * dx / dx_dy
        first_speed[1] = second_collider.speed * dy / dx_dy

        # Leiab teise palli kiiruse vastavalt impulsi jäävuse seadusele
        second_speed[0] -= first_speed[0]
        second_speed[1] -= first_speed[1]

        # Muudab teise palli suunda juhul, kui see muutub
        if second_speed[0] < 0:
            second_collider.direction_x *= -1
            second_speed[0] = abs(second_speed[0])
        if second_speed[1] < 0:
            second_collider.direction_y *= -1
            second_speed[1] = abs(second_speed[1])

        # Muudab esimese palli suunda juhul, kui see muutub
        if first_speed[0] < 0:
            first_collider.direction_x *= -1
            first_speed[0] = abs(first_speed[0])
        if first_speed[1] < 0:
            first_collider.direction_y *= -1
            first_speed[1] = abs(first_speed[1])

        # Annab väärtused edasi objektile, mida ekraanile kuvatakse, on vajalik, et palli asukoht
        # mängus tegelikult muutuks
        first_collider.speed_x = first_speed[0]
        first_collider.speed_y = first_speed[1]
        second_collider.speed_x = second_speed[0]
        second_collider.speed_y = second_speed[1]

#Variables - mdw: Mouse distance from white
#bdw: Ball distance from white
#angle_beta: angle of mouses alignment against the y-axis subtracted from the angle of the mouses position line

# Funktsioon, mis asub tööle, kui kiid pallist eemale tõmmatakse, enne kordust algväärtustan vajalikud muutujad
def pull_stick(angle, pressed_pos, white_rect, stick, stick_group, screen, background, white_group, ball_group):

    # Valge palli keskkoha leidmine
    white_center = ball_center(white_rect)

    # leiab kii esialgse positsiooni
    stick_base_x = stick.rect[0]
    stick_base_y = stick.rect[1]
    projection = 0
    while True:
        for event in pygame.event.get():

            # Liigutab kiid vastavalt sellele, kui kaugele hiirt tõmmatakse, kuni klahvi all hoitakse
            if event.type == MOUSEMOTION:

                # Leiab hiire hetkepositsiooni
                current_pos = pygame.mouse.get_pos()

                # Leiab hiire kauguse valgest pallist x, y kauguse ja siis kauguse otse
                mdw_x = current_pos[0] - white_center[0]
                mdw_y = current_pos[1] - white_center[1]
                mdw = math.hypot(mdw_x, mdw_y)

                # Leiab teise nurga, mida kasutatakse, et leida kaugus kui kaugele tõmmati kii pallist eemale
                angle_beta = abs(calc_angle(current_pos, white_rect)+90 - angle)

                # Kauguse Muutus x ja y telge pidi
                dx = current_pos[0] - pressed_pos[0]
                dy = current_pos[1] - pressed_pos[1]

                # Leiab kui kaugele kii tõmmati
                projectory_dist = mdw * math.sin(math.radians(angle_beta))
                projectable = math.hypot(dx, dy)
                projection = math.hypot(projectable, projectory_dist)

                # Liigutab kiid graafiliselt
                stick.rect[0] = stick_base_x + math.sin(math.radians(angle)) * projection
                stick.rect[1] = stick_base_y - math.cos(math.radians(angle)) * projection

                # Kuvab kii graafilise liikumise välja
                screen.blit(background, (0, 0))
                white_group.draw(screen)
                ball_group.draw(screen)
                stick_group.draw(screen)
                pygame.display.update()

            # Annab edasi kauguse, kui kaugele kii tõmmati
            elif event.type == MOUSEBUTTONUP:
                return projection

            # Laseb löögi katkestada, kui tahetakse lüüa teise nurga alt
            elif event.type == MOUSEBUTTONDOWN:
                return 0
            elif event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()


# Arvutab välja nurga vastavalt kii asukohale ja valge palli asukohale
def calc_angle(mouse_pos, white_rect):
    white_pos = ball_center(white_rect)
    a = mouse_pos[0] - white_pos[0]
    b = mouse_pos[1] - white_pos[1]
    try:
        angle = math.atan(b/a) / (math.pi/180)
        if mouse_pos[0] < white_pos[0]:
            angle += 180
    except:
        c = math.sqrt(a*a + b*b)
        angle = math.asin(b/c) / (math.pi/180)
    return angle


# Pöörab kiid ümber valge palli
def rotate_stick(stick, mouse_pos, white_rect, image, angle):
    tangent = 1
    white_pos = ball_center(white_rect)

    # Leiab hiire ja valge palli vahel tekkiva täisnurkse kolmnurga külgede pikkused
    a = mouse_pos[0] - white_pos[0]
    b = mouse_pos[1] - white_pos[1]

    # Juhul, kui hiir on valge palli keskel, annab kiile kindla positsiooni
    if a*a + b*b == 0:
        stick.rect[0] = white_pos[0]
        stick.rect[1] = white_pos[1]

    # osa funktsioonist, mis kii pöörlema paneb
    else:
        angle = calc_angle(mouse_pos, white_rect)

        # Funktsioon, mis keerab kii pilti
        stick.image = pygame.transform.rotate(image, -angle)
        #print(-angle)
        # Kui kii peaks olema vasakul siis annab positsiooni, mis on valgest pallist vasakul
        if a < 0:
            stick.rect[0] = white_pos[0] - stick.image.get_width()

        # Juhul, kui kii peaks olema valgest pallist paremal, siis annab sellele pildile koha paremal pool
        else:
            stick.rect[0] = white_pos[0]

        # Juhul, kui kii peaks olema pallist ülevalpool, siis annab vastava positsiooni
        if b < 0:
            stick.rect[1] = white_pos[1] - stick.image.get_height()

        # Kui kii peaks olema pallist allpool, siis annab sellele positsiooni, pallist allpool
        else:
            stick.rect[1] = white_pos[1]

        # Arvutab välja nurga tangensit kii ja palli vahel
        if abs(a) >= abs(b):
            tangent = b/a
        elif abs(a) < abs(b):
            tangent = a/b
        if tangent >= 0:
            tangent -= 1
        elif tangent < 0:
            tangent += 1
        if a + b > 0:
            pass
        else:
            tangent = -tangent
        if tangent == 1:
            tangent = -1

        # Täpsustab kii positsiooni, sest kii pildi algne paksus muudab kii asukoha valeks pygame funktsiooni tõttu
        if abs(a) > abs(b):
            stick.rect[1] += tangent * stick.rect[3]/2
        else:
            stick.rect[0] += tangent * stick.rect[3]/2

# Funktsioon, mis tegeleb pallide liigutamiseg mööda väljakut
def move_balls(moving_balls, balls, walls, game_field):

    # Kordus, mis kontrollib, et kõik pallid käidaks läbi
    for ball in moving_balls:

        # leiab palli kiiruse vastavalt x ja y teljelistele kiirustele
        ball.speed = math.hypot(ball.speed_x, ball.speed_y)

        # Kuni palli kiirus on olemas siis liigutab pall
        if ball.speed > 0:

            # Liidab palli asukohael juurde palli kiiruse õiges suunas
            ball.rect[0] -= ball.speed_x * ball.direction_x
            ball.rect[1] += ball.speed_y * ball.direction_y

            # Vähendab palli kiirust
            new_ball_speed = ball.speed - 0.1

            # Väärtustab palli kiirused objekti juures
            ball.speed_x = new_ball_speed * (ball.speed_x/ball.speed)
            ball.speed_y = new_ball_speed * (ball.speed_y/ball.speed)
            ball.speed = new_ball_speed
            check_wall_collision(ball, walls)

            # Kui pall läheb väljakult välja siis ta eemaldatakse
            if not game_field.collidepoint(ball.rect[0], ball.rect[1]):
                ball.kill()

            # Kui pall jääb seisma siis lisab palli seisvate pallide peale
            if ball.speed <= 0:
                balls.add(ball)
    return balls


# Alustab programmi ja läheb funktsiooni main juurde
if __name__ == '__main__':
    main()
# Lõpetab programmi, kui sellest väljutakse
pygame.quit()
