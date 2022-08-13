# GTS project
# master's thesis -> Geodesic Travel Simulator
# surface.builder -> obj builder

import wolframclient.evaluation as kernel
from wolframclient.language import wl, wlexpr
import gts.šlog as šlog

DIVIDER = 13
logger = šlog.configure(__name__)


def build(x, interval_u, interval_v):
    """
    Builder of surface OBJ file
    :param x: surface parametrization in Wolfram Language notation
    :param interval_u: range of surface parameter u
    :param interval_v: range of surface parameter v
    :return: None
    """
    split = []
    faces = []
    u_step = (interval_u[1] - interval_u[0]) / DIVIDER
    v_step = (interval_v[1] - interval_v[0]) / DIVIDER
    for i in range(0, DIVIDER + 1):
        for j in range(0, DIVIDER + 1):
            split.append([
                interval_u[0] + i * u_step,
                interval_v[0] + j * v_step
            ])
            # Vertices are numbered bottom to top, left to right, in a zig-zag pattern:
            #   *  *  *  *
            #   *  *  *  *
            #   *  *  *  *
            #   *  *  *  *
            # is numbered like so:
            #   04 08 12 16
            #   03 07 11 15
            #   02 06 10 14
            #   01 05 09 13

            if j != DIVIDER and i != DIVIDER:
                faces.append([
                    i * (DIVIDER + 1) + j + 1,
                    (i + 1) * (DIVIDER + 1) + j + 1,
                    (i + 1) * (DIVIDER + 1) + j + 2,
                    i * (DIVIDER + 1) + j + 2
                ])
            # Faces are defined by vertices in a counter-clockwise pattern, like so:
            #   4 3
            #   1 2

    session = kernel.WolframLanguageSession()  # Start up the Wolfram Kernel
    session.evaluate(wlexpr(f'x[{{u_,v_}}] := {x}'))  # Load surface definition
    session.evaluate(wlexpr('unitnormal[x_][u_, v_] :='
                            'Module[{U, V, xu, xv},'
                            'xu = D[x[{U, V}], U];'
                            'xv = D[x[{U, V}], V];'
                            'Nx = Cross[xu, xv] /. {U -> u, V -> v};'
                            'Simplify[Nx/Norm[Nx]]]'))  # Load unit normal expression
    session.evaluate(wlexpr('xn[{u_,v_}] := unitnormal[x][u,v]//N'))  # Load surface normal map
    vertices = session.evaluate(wl.Map(wlexpr('x'), split))
    vertex_normals = session.evaluate(wl.Map(wlexpr('xn'), split))

    with open(f'cube.obj', mode='w') as obj_file:
        # TODO: change from 'cube'
        # TODO: add 'saved' surfaces for faster loading
        obj_file.write('mtllib cube.mtl\n')
        obj_file.write('o Cube_Cube.001\n')
        for vertex in vertices:
            obj_file.write(f'v {vertex[0]:f} {vertex[1]:f} {vertex[2]:f}\n')
        for vn in vertex_normals:
            obj_file.write(f'vn {(-1 * vn[0]):f} {(-1 * vn[1]):f} {(-1 * vn[2]):f}\n')
        obj_file.write('usemtl None\n')
        obj_file.write('s off\n')
        for face in faces:
            obj_file.write(
                f'f {face[0]}//{face[0]}'
                f' {face[1]}//{face[1]}'
                f' {face[2]}//{face[2]}'
                f' {face[3]}//{face[3]}\n'
            )
        for i in range(0, DIVIDER - 1):
            obj_file.write('l')
            for j in range((i + 1) * (DIVIDER + 1) + 1, (i + 2) * (DIVIDER + 1) + 1):
                obj_file.write(f' {j}')
            obj_file.write('\n')
        for j in range(2, DIVIDER + 1):
            obj_file.write('l')
            for i in range(j, j + DIVIDER * (DIVIDER + 1) + 1, DIVIDER + 1):
                obj_file.write(f' {i}')
            obj_file.write('\n')

    print('Done!')
