# GTS project
# master's thesis -> Geodesic Travel Simulator
# pathfinder.py -> path calculation and drawing library

from OpenGL.GL import *

travel_path = {
    'vertices': [],
    'edges': []
}


def move(position, velocity):
    step = len(travel_path['edges'])

    # add velocity * 1sec = path to position
    destination = (
        position[0] + velocity[0],
        position[1] + velocity[1],
        position[2] + velocity[2]
    )

    if not step:  # if start = not step = no edges in list
        travel_path['vertices'].append(position)

    travel_path['vertices'].append(destination)  # add destination to end of path

    if step < 500:  # add new <VERTEX INDICES> = <EDGE> if short enough path
        travel_path['edges'].append((step, step + 1))
    else:  # remove oldest positional vertex
        travel_path['vertices'].pop(0)

    return destination


def draw_travel_path():
    glBegin(GL_LINES)
    for edge in travel_path['edges']:
        for vertex in edge:
            glVertex3fv(travel_path['vertices'][vertex])
    glEnd()
