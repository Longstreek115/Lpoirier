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

from objloader import *
from classes import *

def text(position, textString, gameOver, fontSize, rgbValue, background):  
    font = pygame.font.Font (None, fontSize)   
    if type(textString) == int:
        if textString >= 80:
            rgbValue = (0,255,0) #green
        elif textString <= 60 and textString > 20:
            rgbValue = (255,255,0) #yelllow
        elif textString <= 20:
            rgbValue = (255,0,0) #red
#CITATION: from https://www.pygame.org/wiki/CrossPlatformTextOpengl
########################################################################################
    textSurface = font.render(str(textString), True, rgbValue, background)     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
#########################################################################################
 
def collisionDetect(bminx, rminx, bmaxx, rmaxx, bminy, rminy, bmaxy, rmaxy, bminz, rminz, bmaxz, rmaxz):
    # print("bminx", bminx)
    # print("rminx", rminx)
    # print("bmaxx", bmaxx)
    # print("rmaxx", rmaxx)
    # print("bminy", bminy)
    # print("rminy", rminy)
    # print("bmaxy", bmaxy)
    # print("rmaxy", rmaxy)
    # print("bminz", bminz)
    # print("rminz", rminz)
    # print("bmaxz", bmaxz)
    # print("rmaxz", rmaxz)

    bminx = abs(bminx)
    bmaxx = abs(bmaxx)
    rminx = abs(rminx)
    rmaxx = abs(rmaxx)

    bminy = abs(bminy)
    bmaxy = abs(bmaxy)
    rminy = abs(rminy)
    rmaxy = abs(rmaxy)

    bminz = abs(bminz)
    bmaxz = abs(bmaxz)
    rminz = abs(rminz)
    rmaxz = abs(rmaxz)
    
    if abs(bminx-rminx) > abs(bmaxx-rminx):
        bminx, bmaxx = bmaxx, bminx
        # print('newbminx', bminx)
        # print('newbmaxx', bmaxx)

    if abs(bminy-rminy) > abs(bmaxy-rminy):
        bminy, bmaxy = bmaxy, bminy
        # print('newbminy', bminx)
        # print('newbmaxy', bmaxy)
 
    x = abs(rmaxx-rminx)
    y = abs(rmaxy-rminy)
    z = abs(rmaxz-rminz)

    # print('x', x)
    # print('y', y)
    # print('z', z)
   
    if x < 4 and y < 4:
        if rmaxx < bminx:
            return False
        if rmaxx > bmaxx:
            return False
        if rmaxy < bminy:
            return False
        if rmaxy > bmaxy:
            return False
        return True

    if x < 4:
        if rmaxx < bminx:
            return False
        if rmaxx > bmaxx:
            return False
        invy = 1/y
        invz = 1/z

        #CITATION: from https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-box-intersection
        ###################################################################################
        tymin = (bminy - rminy) * invy 
        tymax = (bmaxy - rminy) * invy 
        tzmin = (bminz - rminz) * invz 
        tzmax = (bmaxz - rminz) * invz 
        
        if tymin > tzmax or tzmin > tymax:
            return False
 
        if tzmin > tymin:
            tymin = tzmin
    
        if tzmax < tymax:
            tymax = tzmax
    
        return True
        ###############################################################################

    if y < 4:
        if rmaxy < bminy:
            return False
        if rmaxy > bmaxy:
            return False
        invx = 1/x
        invz = 1/z

        #CITATION: from https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-box-intersection
        ###################################################################################
        txmin = (bminx - rminx) * invx 
        txmax = (bmaxx - rminx) * invx 
        tzmin = (bminz - rminz) * invz 
        tzmax = (bmaxz - rminz) * invz 
        
        if txmin > tzmax or tzmin > txmax:
            return False
 
        if tzmin > txmin:
            txmin = tzmin
    
        if tzmax < txmax:
            txmax = tzmax

        return True     
        #############################################################################

    invx = 1/x
    invy = 1/y
    invz = 1/z

    # print('invx', invx)
    # print('invy', invy)
    # print('invz', invz)
    
    #CITATION: from https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-box-intersection
    ###################################################################################
    txmin = (bminx - rminx) * invx 
    txmax = (bmaxx - rminx) * invx 
    tymin = (bminy - rminy) * invy 
    tymax = (bmaxy - rminy) * invy 
    tzmin = (bminz - rminz) * invz 
    tzmax = (bmaxz - rminz) * invz 
 
    if txmin > txmax:
        txmin, txmax = txmax, txmin
 
    if tymin > tymax:
        tymin, tymax = tymax, tymin
 
    if tzmin > tzmax:
        tzmin, tzmax = tzmax, tzmin

    # print('txmin', txmin)
    # print('txmax', txmax)
    # print('tymin', txmin)
    # print('tymax', tymax)
    # print('tzmin', tzmin)
    # print('tzmax', tzmax)

    if ((txmin > tymax) or (tymin > txmax)):
        return False
    
    if tymin > txmin:
        txmin = tymin
        # print('newtxmin', txmin)

    if tymax < txmax:
        txmax = tymax
        # print('newtxmax', txmax)

    if ((txmin > tzmax) or (tzmin > txmax)):
        return False
 
    if tzmin > txmin:
        txmin = tzmin
 
    if tzmax < txmax:
        txmax = tzmax
 
    return True
    #################################################################################


def largestSize3(x,y,z):
    secondBig = max(y,z)
    biggest = max(x, secondBig)
    return biggest

def gcdFind(x, other):
    x = abs(x)
    other = abs(other)
    largest = max(x, other)
    for divisor in range(largest, 0, -1):
        if ((x%divisor == 0) and (other%divisor == 0)):
            return divisor

def gcdFinder(x, y, z):
    x = abs(x)
    y = abs(y)
    z = abs(z)
 
    largest = largestSize3(x,y,z)
    for divisor in range(largest, 0, -1):
        if ((x%divisor == 0) and (y%divisor == 0) and (z%divisor == 0)):
            return divisor

def health(cx, cy, cz, hp, gameOver): #creates health bar
    text((cx, cy, cz,), hp, gameOver, 64, (0, 255, 0), (0, 0, 0))
 
def score(cx, cy, cz, points, gameOver): #Creates score bar
    text((cx, cy, cz), points, gameOver, 64, (0, 0, 255), (0, 0, 0))


def detect(rx, ry, rz, bxmin, bxmax, bymin, bymax, bzmin, bzmax):
    if rx < bxmin or rx > bxmax:
        return False
    if ry < bymin or ry > bymax:
        return False
    if rz < bzmin or rz > bzmax:
        return False
    return True

def loadingScreen(width, height):
    verticies = ( #(x, y, z)
            (width, height, 0), #bottom front right
            (width, 0, 0), #top front right 
            (0, height, 0), #bottom front left
            (0, 0, 0), #top front left
            )
 
    surfaces = (
            (0,1,2,3), #front face
            (0,2,3,1)
        )
    #CITATION: from https://pythonprogramming.net/coloring-pyopengl-surfaces-python-opengl/
    #################################################################################
    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3f(0, 0, 0) #specifies the color
        for vertex in surface:
            glVertex3fv(verticies[vertex]) #specifies a vertex 
    glEnd()
    #################################################################################

def flash(width, height):
    verticies = ( #(x, y, z)
            (width, height, 0), #bottom front right
            (width, 0, 0), #top front right 
            (0, height, 0), #bottom front left
            (0, 0, 0), #top front left
            )
 
    surfaces = (
            (0,1,2,3), #front face
            (0,2,3,1)
        )
    #CITATION: from https://pythonprogramming.net/coloring-pyopengl-surfaces-python-opengl/
    #################################################################################
    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3f(255, 255, 255) #specifies the color
        for vertex in surface:
            glVertex3fv(verticies[vertex]) #specifies a vertex 
    glEnd()
    #################################################################################
    
def restart():
    return False, 100

def endScreen(gameOver, width, height, points):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    flash(width, height)
    text((width/5, height*2/3, 0), 'Game Over', gameOver, 128, (255,191,0), (255, 255, 255))
    text((width/3, height/2.5, 0), 'Score:', gameOver, 128, (0, 0, 0), (255, 255, 255))
    text((width/3.5, height*1/4, 0), points, gameOver, 128, (0, 0, 0), (255, 255, 255))
