# import sys

from OpenGL.GLU import *
from pygame.constants import *

from gts.surface.obj import *
from gts.surface import Builder, Parametrization
import gts.šlog as šlog

logger = šlog.configure(__name__)


def main():
    pygame.init()
    viewport = (1600, 900)

    # LOAD OBJECT AFTER PYGAME INIT
    (u0, u1) = (float(input("u0 = ")), float(input("u1 = ")))
    (v0, v1) = (float(input("v0 = ")), float(input("v1 = ")))
    p = input("parametrization: ")
    logger.info(f"inputs loaded: [{u0}, {u1}]×[{v0}, {v1}] {p}")
    try:
        parametrization = Parametrization(u=(u0, u1), v=(v0, v1), parametrization=p)
    except TypeError as e:
        logger.error(f"bad inputs: {e}")
        return
    builder = Builder(divider=13, parametrization=parametrization)
    obj = builder.load()

    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width / float(height), 0.1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth(1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, (-5, -2, -1, 4.0))
    glLightfv(GL_LIGHT0, GL_POSITION, (3, 5, 7, 4.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (2, 0.6, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.3, 0.3, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded
    logger.info("OpenGL settings loaded")

    rx, ry = (0, 0)
    tx, ty = (0, 0)
    z_pos = 5
    rotate = move = False
    while 1:
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                return
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4:
                    z_pos = max(1, z_pos - .3)
                elif e.button == 5:
                    z_pos += 1
                elif e.button == 1:
                    rotate = True
                elif e.button == 3:
                    move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    rotate = False
                elif e.button == 3:
                    move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # RENDER OBJECT
        glTranslate(tx / 20., ty / 20., - z_pos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        glCallList(obj.gl_list)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        for line in obj.contours:
            for i in range(0, len(line) - 1):
                glVertex3fv(obj.vertices[line[i] - 1])
                glVertex3fv(obj.vertices[line[i+1] - 1])
        glEnd()

        pygame.display.flip()
