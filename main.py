#Name: Lee Poirier
#Andrew ID: lpoirier

import sys, pygame, math, random
from pygame import mixer
 
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import OpenGL.GL as ogl  

#import additional files
from objloader import *
from classes import *
from helperFunc import *
 
def main():
    pygame.init()
    display = (800,600)
    width, height = display
    clipClose = 0.0
    clipFar = 100.0
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    hp = 100
    gameOver = False
    isFinishedLoading = False
    points = '00000000'
    attack = False
    check = 0

    #CITATION: from https://www.youtube.com/watch?v=aHQrcyerVQQ
    mixer.music.load("The Battle Of Yavin.wav") #command for loading the music 
    mixer.music.play(-1) #if no param, the file will play once, -1 means it will play on loop

    #citation: from https://github.com/valcat/Learning-PyOpenGL/blob/master/mouse-controlled_rectangle.py
    ########################################################################
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0.0, display[0], 0.0, display[1], -1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
#####################################################################################

    while (not isFinishedLoading):
        loadingScreen(width, height)
        text((width/5, height/2, 0), 'Firing Up The Engines', gameOver, 128, (255, 255, 255), (0, 0, 0))
        text((width/5, height/4, 0), 'Firing Up The Engines', gameOver, 128, (255, 255, 255), (0, 0, 0))

        #citation: from https://github.com/valcat/Learning-PyOpenGL/blob/master/mouse-controlled_rectangle.py
        ##################################################
        glEnable(GL_DEPTH_TEST)    
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        ############################################################################
 
        #Citation: from http://www.pygame.org/wiki/OBJFileLoader
        ###############################################################
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
    
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glShadeModel(GL_SMOOTH)
        glDepthRange(0.0,1.0)
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0]/display[1]), 0.1, clipFar)
    
        glMatrixMode(GL_MODELVIEW)
        
        glLoadIdentity()
        glOrtho(0.0, display[0], 0.0, display[1], -1.0, 1.0)
        
        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
        ################################################################################
        
        # loading objects (.obj) from folder with all vertices
        #CITATION: from https://sketchfab.com/3d-models/imperial-tie-fighter-star-wars-66c78dc00f044934b416f85c304437b0
        tie = OBJ('TieFighter_Upload.blend.obj', swapyz=False)
        if tie.isFinished:
            isFinishedLoading = True
    
    #creates object from loaded vertices
    t1 = runOBJ(tie.faces, tie.normals, tie.texcoords, tie.vertices, tie.mtl)
    t1.createObj()

    #4 hitbox objects
    hitBox1 = boundingBox(0, 0, 0, 4, (255, 0, 0))
    hitBox2 = boundingBox(0, 0, 0, 4, (255, 255, 0))
    hitBox3 = boundingBox(0, 0, 0, 4, (0, 255, 255))
    hitBox4 = boundingBox(0, 0, 0, 4, (0, 0, 255))
 
    #citation: from https://github.com/valcat/Learning-PyOpenGL/blob/master/mouse-controlled_rectangle.py
#########################################################################
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    gluPerspective(90.0, width/float(height), 1.0, clipFar)
    glTranslatef(0, 0, -5) #zoom in and out
    glMatrixMode(GL_MODELVIEW)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable( GL_BLEND )
#########################################################
 
 
    clock = pygame.time.Clock()
 
    tz1 = -100
    tz2 = -100
    tz3 = -100
    tz4 = -100
    zmove = -100

    tx1 = 0
    tx2 = -10
    tx3 = 10
    tx4 = 0
    xmove = 0
 
    ty1 = 0
    ty2 = -5
    ty3 = -5
    ty4 = 10
    ymove = 0

    dx = 2
    dy = 2

    moveBack1 = False
    moveBack2 = False
    moveBack3 = False
    moveBack4 = False

    pygame.mouse.set_visible( False )

    while not gameOver:   
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        mX, mY = pygame.mouse.get_pos()
        persX = 107.5*mX/width-53.75
        persY = -82.5*mY/height+41.25
        # print(persX, persY)

        rSideTurret1 = perspectiveLaser(mX, mY, 9, 3, 9.8, 4, -5, 0, 0.05)
        rSideTurret1.drawLaser(105, 105, 105, 1)

        rSideTurret2 = perspectiveLaser(mX, mY, 9, -3, 9.8, -4, -5, 0, 0.05)
        rSideTurret2.drawLaser(105, 105, 105, 1)

        lSideTurret1 = perspectiveLaser(mX, mY, -9, 3, -9.8, 4, -5, 0, 0.05)
        lSideTurret1.drawLaser(105, 105, 105, 1)

        lSideTurret2 = perspectiveLaser(mX, mY, -9, -3, -9.8, -4, -5, 0, 0.05)
        lSideTurret2.drawLaser(105, 105, 105, 1)

        pointer = perspectiveLaser(mX, mY, persX, persY, 0, 0, zmove, 0, 0.05)
        pointer.drawTarget(1, 100)

        # test = perspectiveLaser(mX, mY, persX, persY, 0, 0, zmove, 0, 0.05)
        # test.drawLaser(255, 0, 0, 0.0)
        
        coor = glGetDoublev(GL_MODELVIEW_MATRIX)
        camZ = coor[3][2]
        camY = coor[3][1]
        camX = coor[3][0]

        tz1+=0.5
        tz2+=0.5
        tz3+=0.5
        tz4+=0.5
        zmove+=0.5

        tx1+=0.03
        tx2-=0.02
        tx3+=0.03
        tx4-=0.04

        ty1+=0.02
        ty2-=0.04
        ty3-=0.05
        ty4+=0.03
 
        glTranslatef(xmove,ymove,0) #moves all objects
       
        hitBox1.cx=tx1
        hitBox1.cy=ty1
        hitBox1.cz=tz1
        hitBox1.drawBox()

        hitBox2.cx=tx2
        hitBox2.cy=ty2
        hitBox2.cz=tz2
        hitBox2.drawBox()

        hitBox3.cx=tx3
        hitBox3.cy=ty3
        hitBox3.cz=tz3
        hitBox3.drawBox()

        hitBox4.cx=tx4
        hitBox4.cy=ty4
        hitBox4.cz=tz4
        hitBox4.drawBox()
        
        glPushMatrix()
        glTranslatef(tx1, ty1, tz1)
        glCallList(t1.gl_list) #makes object appear
        glPopMatrix()

        glPushMatrix()
        glTranslatef(tx2, ty2, tz2)
        glCallList(t1.gl_list) 
        glPopMatrix()

        glPushMatrix()
        glTranslatef(tx3, ty3, tz3)
        glCallList(t1.gl_list) 
        glPopMatrix()


        glPushMatrix()
        glTranslatef(tx4, ty4, tz4)
        glCallList(t1.gl_list) 
        glPopMatrix()
        
        #resets object coordinates when it flies past camera
        if tz1 == 0 or tz2 == 0 or tz3 == 0 or tz4 == 0:
            attack = True
 
        if tz1 > 10 or moveBack1:
            tx1 = random.randrange(-15, 15)
            ty1 = random.randrange(-15, 15)
            tz1 = 11
            hitBox1.cx=tx1
            hitBox1.cy=ty1
            hitBox1.cz=tz1
            moveBack1 = False
 
        if tz2 > 10 or moveBack2:
            tx2 = random.randrange(-15, 15)
            ty2 = random.randrange(-15, 15)
            tz2 = 11
            hitBox2.cx=tx2
            hitBox2.cy=ty2
            hitBox2.cz=tz2
            moveBack2 = False

 
        if tz3 > 10 or moveBack3:
            tx3 = random.randrange(-15, 15)
            ty3 = random.randrange(-15, 15)
            tz3 = 11
            hitBox3.cx=tx3
            hitBox3.cy=ty3
            hitBox3.cz=tz3
            moveBack3 = False

 
        if tz4 > 10 or moveBack4:
            tx4 = random.randrange(-15, 15)
            ty4 = random.randrange(-15, 15)
            tz4 = 11
            hitBox4.cx=tx4
            hitBox4.cy=ty4
            hitBox4.cz=tz4
            moveBack4 = False
        
        if tz1 == 11 and tz2 == 11 and tz3 == 11 and tz4 == 11:
                zmove = -108
                tx1 = random.randrange(-15, 15)
                ty1 = random.randrange(-15, 15)
                tz1 = -108
                hitBox1.cx=tx1
                hitBox1.cy=ty1
                hitBox1.cz=tz1

                tx2 = random.randrange(-15, 15)
                ty2 = random.randrange(-15, 15)
                tz2 = -108
                hitBox2.cx=tx2
                hitBox2.cy=ty2
                hitBox2.cz=tz2

                tx3 = random.randrange(-15, 15)
                ty3 = random.randrange(-15, 15)
                tz3 = -108
                hitBox3.cx=tx3
                hitBox3.cy=ty3
                hitBox3.cz=tz3

                tx4 = random.randrange(-15, 15)
                ty4 = random.randrange(-15, 15)
                tz4 = -108
                hitBox4.cx=tx4
                hitBox4.cy=ty4
                hitBox4.cz=tz4
 
        #citation: from https://github.com/valcat/Learning-PyOpenGL/blob/master/mouse-controlled_rectangle.py
        ########################################################################
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, display[0], 0.0, display[1], -1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        ############################################################################
        glDisable(GL_DEPTH_TEST)
 
        health(width/8*7, height/6*5, 0, hp, gameOver)
        score(width/8, height/6*5, 0, points, gameOver)
 
        mX, mY = pygame.mouse.get_pos()
        lStartX = 0
        rStartX = width
        startY = height/2
        endZ = -30
        startZ = 0
        thick = 5
        rOffsetX = ((rStartX-mX)*1/3)+mX
        lOffsetX = mX-((mX-lStartX)*1/3)
        uOffsetY = mY+((startY-mY)*1/3)
        dOffsetY = mY-((mY-startY)*1/3)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    gameOver, hp = restart(gameOver, hp)
                if event.key == pygame.K_LEFT:
                    xmove += dx
                if event.key == pygame.K_RIGHT:
                    xmove += -1*dx
                if event.key == pygame.K_UP:
                    ymove += -1*dy
                if event.key == pygame.K_DOWN:
                    ymove += dy

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xmove += 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ymove += 0

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    persX = 107.5*mX/width-53.75
                    persY = -82.5*mY/height+41.25
                    # print(persX, persY)
                    
                    #CITATION: from https://www.youtube.com/watch?v=UfFiQ-gtLv4&list=PLDgv8nHxCzL2h_tGwhPL5HSR9xWq5tXIU&index=9
                    laserFire = mixer.Sound("tie_blaster.wav")
                    laserFire.play() #only need the last part
                    
                    if mY < startY:
                        rRedLaser = orthoLaser(mX, mY, rOffsetX, uOffsetY, rStartX, startY, endZ, startZ, thick)
                        rRedLaser.drawLaser(255, 0, 0)
                        check = 1
                                
                        lRedLaser = orthoLaser(mX, mY, lOffsetX, uOffsetY, lStartX, startY, endZ, startZ, thick)
                        lRedLaser.drawLaser(255, 0, 0)
                        check = 1
                         
                    elif mY > startY:
                        rRedLaser = orthoLaser(mX, mY, rOffsetX, dOffsetY, rStartX, startY, endZ, startZ, thick)
                        rRedLaser.drawLaser(255, 0, 0)
                        check = 1
                                            
                        lRedLaser = orthoLaser(mX, mY, lOffsetX, dOffsetY, lStartX, startY, endZ, startZ, thick)
                        lRedLaser.drawLaser(255, 0, 0)
                        check = 1
 
                    elif mY == startY:
                        rRedLaser = orthoLaser(mX, mY, rOffsetX, startY, rStartX, startY, endZ, startZ, thick)
                        rRedLaser.drawLaser(255, 0, 0)
                        check = 1

                        lRedLaser = orthoLaser(mX, mY, lOffsetX, startY, lStartX, startY, endZ, startZ, thick)
                        lRedLaser.drawLaser(255, 0, 0)
                        check = 1
                                            
                    #CITATION: from https://www.youtube.com/watch?v=PpRVyBbBD5k                        
                    explosion = mixer.Sound("sw_explosion.wav")
                    if collisionDetect(hitBox1.cx-hitBox1.width, 0, hitBox1.cx+hitBox1.width, persX, hitBox1.cy-hitBox1.width, 0, hitBox1.cy+hitBox1.width, persY, hitBox1.cz+hitBox1.width, -2.8,  hitBox1.cz-hitBox1.width, hitBox1.cz-2*hitBox1.width):
                        print("1 it's a hit!")
                        explosion.play() 
                        points = str(int(points)+100).zfill(7)
                        moveBack1 = True
                       
                    elif collisionDetect(hitBox2.cx-hitBox2.width, 0, hitBox2.cx+hitBox2.width, persX, hitBox2.cy-hitBox2.width, 0, hitBox2.cy+hitBox2.width, persY, hitBox2.cz+hitBox2.width, -2.8,  hitBox2.cz-hitBox2.width, hitBox2.cz-2*hitBox2.width):
                        print("2 it's a hit!")
                        explosion.play() 
                        points = str(int(points)+100).zfill(7)
                        moveBack2 = True
 
                    if collisionDetect(hitBox3.cx-hitBox3.width, 0, hitBox3.cx+hitBox3.width, persX, hitBox3.cy-hitBox3.width, 0, hitBox3.cy+hitBox3.width, persY, hitBox3.cz+hitBox3.width, -2.8,  hitBox3.cz-hitBox3.width, hitBox3.cz-2*hitBox3.width):
                        print("3 it's a hit!")
                        explosion.play() 
                        points = str(int(points)+100).zfill(7)
                        moveBack3 = True
 
                    elif collisionDetect(hitBox4.cx-hitBox4.width, 0, hitBox4.cx+hitBox4.width, persX, hitBox4.cy-hitBox4.width, 0, hitBox4.cy+hitBox4.width, persY, hitBox4.cz+hitBox4.width, -2.8,  hitBox4.cz-hitBox4.width, hitBox4.cz-2*hitBox4.width):
                        print("4 it's a hit!")
                        explosion.play() 
                        points = str(int(points)+100).zfill(7)
                        moveBack4 = True
                    
                    # print('mX', mX)
                    # print('mY', mY)
                    # print('rOffsetX', rOffsetX)
                    # print('lOffsetX', lOffsetX)
                    # print('uOffsetY', uOffsetY)
                    # print('dOffsetY', dOffsetY)
                    # print('rStartX', rStartX)
                    # print('startY', startY)
                    # print('endZ', endZ)
                    # print('startZ', startZ)
                    # print('newEndX', rNewEndX)
                    # print('newEndY', rNewEndY)
                    # print('newStartX', rNewStartX)
                    # print('newStartY', rNewStartY)
                    # print('newEndZ', rNewEndZ)
                    # print('newStartZ', rNewStartZ)

        if check == 1:            
            rRedLaser.translateCoor(lRedLaser.gcd)
            rRedLaser.drawLaser(255, 0, 0)
 
            lRedLaser.translateCoor(rRedLaser.gcd)
            lRedLaser.drawLaser(255, 0, 0)
 
            if lRedLaser.check != -1 and rRedLaser.check != -1:
                check = 0                    
 
        while(attack):
            #CITATION: from https://www.youtube.com/watch?v=UfFiQ-gtLv4&list=PLDgv8nHxCzL2h_tGwhPL5HSR9xWq5tXIU&index=9
            hit = mixer.Sound("tie_blaster.wav") 
            hit.play() 

            rGreenLaser = orthoLaser(width/2, height/2, width/2+100, height/3*2, 800, 300, -30, 0, 5)
            lGreenLaser = orthoLaser(width/2, height/2, width/2-100, height/3*2, 0, 300, -30, 0, 5)
            rGreenLaser.drawLaser(0, 255, 0)
            lGreenLaser.drawLaser(0, 255, 0)
 
            flash(width, height)
            glTranslatef(0,0,-150)
            hp-=20
            if hp <= 0:
                #CITATION: from https://www.youtube.com/watch?v=6yisws5rKoo
                die = mixer.Sound("lego_yoda.wav") 
                die.play() 
                gameOver = True
                endScreen(gameOver, width, height, points)
            attack = False 
        
        glEnable(GL_DEPTH_TEST)
        #citation: from https://github.com/valcat/Learning-PyOpenGL/blob/master/mouse-controlled_rectangle.py
        #############################################################################
 
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
 
        ###################################################################
        pygame.display.flip()
main()
 
 
 
 
 

