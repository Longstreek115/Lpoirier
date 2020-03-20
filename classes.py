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
from helperFunc import *

class perspectiveLaser(object):
    def __init__(self, mx, my, endx, endy, startx, starty, endz, startz, thick):
        self.mx = mx
        self.my = my
        self.endx = endx
        self.endy = endy
        self.startx = startx
        self.starty = starty
        self.endz = endz
        self.startz = startz
        self.thick = thick
        self.mz = -100
        self.check = -1
        self.gcd = 0
    
    def drawLaser(self, r, g, b, a): #creates right laser
        verticies = [ #(x, y, z)
            [self.endx+self.thick, self.endy+self.thick, self.endz], #bottom back right
            [self.endx+self.thick, self.endy-self.thick, self.endz], #top back right
            [self.endx-self.thick, self.endy+self.thick, self.endz], #top back left
            [self.endx-self.thick, self.endy-self.thick, self.endz], #bottom back left 
            [self.startx+self.thick, self.starty+self.thick, self.startz], #bottom front right
            [self.startx+self.thick, self.starty-self.thick, self.startz], #top front right 
            [self.startx-self.thick, self.starty+self.thick, self.startz], #bottom front left
            [self.startx-self.thick, self.starty-self.thick, self.startz], #top front left
        ]
        #CITATION: from https://pythonprogramming.net/coloring-pyopengl-surfaces-python-opengl/
        #################################################################################
                #defining edges
        edges = [
            [0, 1], #back right edge
            [0, 3], #back bottom edge
            [0, 4], #right bottom edge
            [2, 1], #top back edge
            [2, 3], #back left edge
            [2, 7], #left top edge
            [6, 3], #left bottom edge
            [6, 4], #front bottom edge
            [6, 7], #front left edge
            [5, 1], #top right edge
            [5, 4], #front right edge
            [5, 7], #top front edge
        ]
 
        surfaces = [
            [0,1,2,3], #back face
            [3,2,7,6], #top face
            [6,7,5,4], #front face
            [4,5,1,0], #right face
            [1,5,7,2], #left face
            [4,0,3,6], #bottom face
        ]
 
        glBegin(GL_QUADS)
        for surface in surfaces:
            for vertex in surface:
                glColor4f(r, g, b, a)
                glVertex3fv(verticies[vertex]) #specifies a vertex 
        glEnd()
 
        glBegin(GL_LINES) #tells what kind of graphics it will be working with(lines)
        for edge in edges:
            for vertex in edge:
                glColor4f(r, g, b, a) #specifies the color
                glVertex3fv(verticies[vertex]) #specifies a vertex 
        glEnd()
        ############################################################################

    def drawTarget(self, r, sides): #creates cursor icon
        glColor3f(255, 0, 0) #red (R,G,B)
        glBegin(GL_LINE_LOOP) 
        for n in range(sides):
            theta = 2*math.pi*n/sides
            if ((theta >= math.pi/6 and theta <=math.pi/3) or 
                (theta >= math.pi*2/3 and theta <= math.pi*5/6) or 
                (theta >= math.pi*7/6 and theta <= math.pi*4/3) or
                (theta >= math.pi*5/3 and theta <= math.pi*11/6)):
                glColor3f(0, 0, 0)
            else:
                glColor3f(255, 0, 0)
            x = r*math.sin(theta)
            y = r*math.cos(theta)
            glVertex3f(x + self.endx, y + self.endy, self.endz)
        glEnd()
    
        glBegin(GL_LINES)
        glVertex3f(self.endx-r, self.endy, self.endz)
        glVertex3f(self.endx-r/5, self.endy, self.endz)
        glVertex3f(self.endx+r, self.endy, self.endz)
        glVertex3f(self.endx+r/5, self.endy, self.endz)
        glVertex3f(self.endx, self.endy-r, self.endz)
        glVertex3f(self.endx, self.endy-r/5, self.endz)
        glVertex3f(self.endx, self.endy+r, self.endz)
        glVertex3f(self.endx, self.endy+r/5, self.endz)
        glEnd()
 
 
class orthoLaser(object):
    def __init__(self, mx, my, endx, endy, startx, starty, endz, startz, thick):
        self.mx = mx
        self.my = my
        self.endx = endx
        self.endy = endy
        self.startx = startx
        self.starty = starty
        self.endz = endz
        self.startz = startz
        self.thick = thick
        self.mz = -100
        self.check = -1
        self.gcd = 0
 
    def drawLaser(self, r, g, b): #creates right laser
        verticies = [ #(x, y, z)
            [self.endx+self.thick, 600-self.endy+self.thick, self.endz], #bottom back right
            [self.endx+self.thick, 600-self.endy-self.thick, self.endz], #top back right
            [self.endx-self.thick, 600-self.endy+self.thick, self.endz], #top back left
            [self.endx-self.thick, 600-self.endy-self.thick, self.endz], #bottom back left 
            [self.startx+self.thick, 600-self.starty+self.thick, self.startz], #bottom front right
            [self.startx+self.thick, 600-self.starty-self.thick, self.startz], #top front right 
            [self.startx-self.thick, 600-self.starty+self.thick, self.startz], #bottom front left
            [self.startx-self.thick, 600-self.starty-self.thick, self.startz], #top front left
        ]
 
        # print('self.endx', self.endx)
        # print('self.endy', self.endy)
        # print('self.endz', self.endz)
        # print('self.startx', self.startx)
        # print('self.starty', self.starty)
        # print('self.startz', self.startz)
        
        #CITATION: from https://pythonprogramming.net/coloring-pyopengl-surfaces-python-opengl/
        #################################################################################
                #defining edges
        edges = [
            [0, 1], #back right edge
            [0, 3], #back bottom edge
            [0, 4], #right bottom edge
            [2, 1], #top back edge
            [2, 3], #back left edge
            [2, 7], #left top edge
            [6, 3], #left bottom edge
            [6, 4], #front bottom edge
            [6, 7], #front left edge
            [5, 1], #top right edge
            [5, 4], #front right edge
            [5, 7], #top front edge
        ]
 
        surfaces = [
            [0,1,2,3], #back face
            [3,2,7,6], #top face
            [6,7,5,4], #front face
            [4,5,1,0], #right face
            [1,5,7,2], #left face
            [4,0,3,6], #bottom face
        ]
 
        glBegin(GL_QUADS)
        for surface in surfaces:
            for vertex in surface:
                glColor3f(255, 255, 255) 
                glVertex3fv(verticies[vertex]) #specifies a vertex 
        glEnd()
 
        glBegin(GL_LINES)#tells what kind of graphics it will be working with(lines)
        for edge in edges:
            for vertex in edge:
                glColor3f(r, g, b) #specifies the color
                glVertex3fv(verticies[vertex]) #specifies a vertex 
        glEnd()
        #############################################################################

    def translateCoor(self, other_gcd):
        self.mx = int(self.mx)
        self.my = int(self.my)
        self.mz = int(self.mz)
        self.endx = int(self.endx)
        self.endy = int(self.endy)
        self.startx = int(self.startx)
        self.starty = int(self.starty)
        self.endz = int(self.endz)
        self.startz = int(self.startz)
        

        # print('mx', mx)
        # print('my', my)
        # print('endx', endx)
        # print('endy', endy)
        # print('startx', startx)
        # print('starty', starty)
        # print('endz', endz)
        # print('startz', startz)
                            
            
        changeX = self.mx-self.endx
        changeY = self.my-self.endy
        changeZ = self.mz-self.endz
 
        # print('self.check', self.check)
        if changeX == 0 and changeY == 0 and changeZ == 0:
            self.check+=1
        
        elif changeX == 0:
            self.gcd = gcdFind(changeY, changeZ)
 
        elif changeY == 0:
            self.gcd = gcdFind(changeX, changeZ)

        elif changeZ == 0:
            self.gcdX = gcdFind(changeX, changeY)
          
        else:
            # print('changeX', changeX)
            # print('changeY', changeY)
            # print('changeZ', changeZ)
 
            self.gcd = gcdFinder(changeX, changeY, changeZ)
            
            # print('self.gcd', self.gcd)
            if abs(self.gcd) >= abs(other_gcd):
                self.endx += changeX/self.gcd
                self.endy += changeY/self.gcd
                self.endz += changeZ/self.gcd
    
                self.startx += changeX/self.gcd
                self.starty += changeY/self.gcd
                self.startz += changeZ/self.gcd
 
            # print('self.endx', self.endx)
            # print('self.endy', self.endy)
            # print('self.endz', self.endz)
            # print('self.startx', self.startx)
            # print('self.starty', self.starty)
            # print('self.startz', self.startz)  

class boundingBox(object):
    def __init__(self, cx, cy, cz, width, rgbString):
        self.cx = cx
        self.cy = cy
        self.cz = cz
        self.width = width
        self.r = rgbString[0]
        self.g = rgbString[1]
        self.b = rgbString[2]

    def drawBox(self):
        verticies = [ #(x, y, z)
            [self.cx+self.width, self.cy+self.width, self.cz-self.width], #bottom back right
            [self.cx+self.width, self.cy-self.width, self.cz-self.width], #top back right
            [self.cx-self.width, self.cy-self.width, self.cz-self.width], #top back left
            [self.cx-self.width, self.cy+self.width, self.cz-self.width], #bottom back left 
            [self.cx+self.width, self.cy+self.width, self.cz+self.width], #bottom front right
            [self.cx+self.width, self.cy-self.width, self.cz+self.width], #top front right 
            [self.cx-self.width, self.cy+self.width, self.cz+self.width], #bottom front left
            [self.cx-self.width, self.cy-self.width, self.cz+self.width], #top front left
        ]
        #CITATION: from https://pythonprogramming.net/coloring-pyopengl-surfaces-python-opengl/
        #################################################################################
        edges = [
            [0, 1], #back right edge
            [0, 3], #back bottom edge
            [0, 4], #right bottom edge
            [2, 1], #top back edge
            [2, 3], #back left edge
            [2, 7], #left top edge
            [6, 3], #left bottom edge
            [6, 4], #front bottom edge
            [6, 7], #front left edge
            [5, 1], #top right edge
            [5, 4], #front right edge
            [5, 7], #top front edge
        ]
 
        surfaces = [
            [0,1,2,3], #back face
            [3,2,7,6], #top face
            [6,7,5,4], #front face
            [4,5,1,0], #right face
            [1,5,7,2], #left face
            [4,0,3,6], #bottom face
        ]

        
        glBegin(GL_LINES)#tells what kind of graphics it will be working with(lines)
        for edge in edges:
            for vertex in edge:
        #########################################################################
                glColor4f(self.r, self.g, self.b, 0.0) # makes it transparent 
        #########################################################################
                glVertex3fv(verticies[vertex]) #specifies a vertex 
        glEnd()
        #############################################################################
 