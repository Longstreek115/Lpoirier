#Name: Lee Poirier
#Andrew ID: lpoirier

# CITATION: objloader file
# modified from: http://www.pygame.org/wiki/OBJFileLoader
import pygame
from OpenGL.GL import *

###################################################################
PATH = 'C:'
def MTL(filename):
    contents = {}
    mtl = None
    for line in open(PATH + filename, "r"):
        # Comment line
        if line.startswith('#'):
            continue
        values = line.split()
        # Blank line
        if not values:
            continue
        # newmtl line (name of the material)
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        # no name assign to the material
        elif mtl is None:
            raise(ValueError, "mtl file doesn't start with newmtl stmt")
        # texture line
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(
                    GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                    GL_UNSIGNED_BYTE, image)
        # set all value to float
        else:
            mtl[values[0]] = [float(v) for v in values[1:]]
    return contents


class OBJ(object):
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.smallest = 0
        self.largest = 0
        self.small = 0
        self.large = 0
        self.isFinished = False


        material = None
        
        for line in open(PATH + filename, "r"):
            # Comment line
            if line.startswith('#'):
                continue
            values = line.split()
            # Blank line
            if not values:
                continue
            # Vertices
            if values[0] == 'v':
                v = [float(v) for v in values[1:4]]
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            # Vertice's normal
            elif values[0] == 'vn':
                v = [float(v) for v in values[1:4]]
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            # Vertice's t
            elif values[0] == 'vt':
                self.texcoords.append([float(v) for v in values[1:3]])

            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]

            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            # Face
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
            self.isFinished = True

class runOBJ(object):
    def __init__(self, faces, normals, texcoords, vertices, mtl):
        self.faces = faces
        self.normals = normals
        self.texcoords = texcoords
        self.vertices = vertices
        self.mtl = mtl
    
    def createObj(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
#################################################################