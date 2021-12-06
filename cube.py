import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from numpy import cross, dot, eye
from scipy.linalg import expm, norm

import numpy as np
import math

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7),
    )

theta = 2 * np.pi / 360


def M(axis, direction):
    axis = np.asarray(axis)
    axis = direction * axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    glTranslatef(0.0, 0.0, -5)
    
    glRotate(0, 0, 0, 0)
    
    turn = [0,1,0]
    roll = [1,0,0]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            x, y, z = turn
            glRotate(-1, x, y, z)
            roll = dot(M(turn, 1),roll)
        if pressed[pygame.K_RIGHT]:
            x, y, z = turn
            glRotate(1, x, y, z)
            roll = dot(M(turn, -1),roll)
        if pressed[pygame.K_DOWN]:
            x, y, z = roll
            glRotate(1, x, y, z)
            turn = dot(M(roll, -1),turn)
        if pressed[pygame.K_UP]:
            x, y, z = roll
            glRotate(-1, x, y, z)
            turn = dot(M(roll, 1),turn)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)
        

if __name__ == "__main__":
    main()        