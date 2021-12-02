import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

sin = 0.01745240643728351281941898
sin2 = 0.00007615242180438042149422

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
    
    turn = (0,1,0)
    roll = (1,0,0)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            x, y, z = turn
            glRotate(1, x, y, z)
            a, b, c = roll
            roll = (
                (4*sin2*(-y*y -z*z)+1)*a + (4*x*y*sin2-z*sin)*b + (4*x*y*sin2+y*sin)*c,
                (4*x*y*sin2+z*sin)*a + (4*sin2*(-x*x -z*z)+1)*b + (4*y*z*sin2-x*sin)*c,
                (4*x*z*sin2-y*sin)*a + (4*y*z*sin2+x*sin)*b + (4*sin2*(-x*x -y*y)+1)*c
                )
        if pressed[pygame.K_RIGHT]:
            x, y, z = turn
            glRotate(-1, x, y, z)
            a, b, c = roll
            roll = (
                (4*sin2*(-y*y -z*z)+1)*a + (4*x*y*sin2+z*sin)*b + (4*x*y*sin2-y*sin)*c,
                (4*x*y*sin2-z*sin)*a + (4*sin2*(-x*x -z*z)+1)*b + (4*y*z*sin2+x*sin)*c,
                (4*x*z*sin2+y*sin)*a + (4*y*z*sin2-x*sin)*b + (4*sin2*(-x*x -y*y)+1)*c
                )
        if pressed[pygame.K_DOWN]:
            x, y, z = roll
            glRotate(1, x, y, z)
            a, b, c = turn
            turn = (
                (4*sin2*(-y*y -z*z)+1)*a + (4*x*y*sin2+z*sin)*b + (4*x*y*sin2-y*sin)*c,
                (4*x*y*sin2-z*sin)*a + (4*sin2*(-x*x -z*z)+1)*b + (4*y*z*sin2+x*sin)*c,
                (4*x*z*sin2+y*sin)*a + (4*y*z*sin2-x*sin)*b + (4*sin2*(-x*x -y*y)+1)*c
                )
        if pressed[pygame.K_UP]:
            x, y, z = roll
            glRotate(-1, x, y, z)
            a, b, c = turn
            turn = (
                (4*sin2*(-y*y -z*z)+1)*a + (4*x*y*sin2-z*sin)*b + (4*x*y*sin2+y*sin)*c,
                (4*x*y*sin2+z*sin)*a + (4*sin2*(-x*x -z*z)+1)*b + (4*y*z*sin2-x*sin)*c,
                (4*x*z*sin2-y*sin)*a + (4*y*z*sin2+x*sin)*b + (4*sin2*(-x*x -y*y)+1)*c
                )
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)
        

main()
        