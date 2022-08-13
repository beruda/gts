# GTS project
# master's thesis -> Geodesic Travel Simulator
# test_pathfinder.py -> pathfinder testing program + GTS for plane travel

from gts.test.cube import *
from gts.pathfinder.mogoi import *

import gts.šlog as šlog


logger = šlog.configure(__name__)

# tangent_1, tangent_2, tangent_3 = (1.0, 0.0, 0.0)
# speed = 0.1
# normal_1, normal_2, normal_3 = (0.0, 0.0, 1.0)
# position = (0, 0, 0)


def main_test_pathfinder():
    logger.info("initializing pygame window")
    pygame.init()
    display = (1280, 960)

    logger.info("setting pygame window dimensions")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    logger.info("setting camera")
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)
    glRotate(0, 0, 0, 0)

    logger.info("setting starting direction")
    tangent_1, tangent_2, tangent_3 = (1.0 / np.sqrt(2),
                                       1.0 / np.sqrt(2),
                                       0.0)

    speed = 0.003
    turn_speed = 0.0002
    normal_1, normal_2, normal_3 = (0.0, 0.0, 1.0)
    position = (0, 0, 0)

    logger.info("releasing snake...")
    while True:
        # exit logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info('exiting')
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    logger.info("exiting")
                    pygame.quit()
                    return

        # acceleration reset for each tick
        acceleration_1, acceleration_2, acceleration_3 = (0.0, 0.0, 0.0)
        binormal_1, binormal_2, binormal_3 = \
            (tangent_2 * normal_3 - tangent_3 * normal_2,
             - tangent_1 * normal_3 + tangent_3 * normal_1,
             tangent_1 * normal_2 - tangent_2 * normal_1)

        # turning logic
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            acceleration_1 += -turn_speed * binormal_1
            acceleration_2 += -turn_speed * binormal_2
            acceleration_3 += -turn_speed * binormal_3
        if pressed[pygame.K_RIGHT]:
            acceleration_1 += turn_speed * binormal_1
            acceleration_2 += turn_speed * binormal_2
            acceleration_3 += turn_speed * binormal_3

        # turning math
        direction_1 = speed * tangent_1 + acceleration_1
        direction_2 = speed * tangent_2 + acceleration_2
        direction_3 = speed * tangent_3 + acceleration_3
        norm_dir = np.linalg.norm(
            (direction_1, direction_2, direction_3)
        )
        tangent_1 = direction_1 / norm_dir
        tangent_2 = direction_2 / norm_dir
        tangent_3 = direction_3 / norm_dir
        velocity = (speed * tangent_1,
                    speed * tangent_2,
                    speed * tangent_3)

        # new position + updating travel path
        position = move(position, velocity)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_travel_path()
        pygame.display.flip()
        pygame.time.wait(3)
