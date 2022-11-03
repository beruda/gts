# GTS project
# master's thesis -> Geodesic Travel Simulator
# surface.Builder -> obj builder
import hashlib
import os.path

import wolframclient.evaluation as kernel
from wolframclient.language import wl, wlexpr
import gts.šlog as šlog
from gts.surface.obj import OBJ

name = __name__


class Parametrization:
    logger = šlog.configure(f"{name}.Parametrization")

    def __init__(self, u: (float, float), v: (float, float), parametrization: str):

        # raise ValueError if parametrization is incorrect or if coordinate function domains don't include U×V
        session = kernel.WolframLanguageSession()
        session.evaluate(wlexpr(f"f[{{u_,v_}}] := {parametrization}"))
        temp = session.evaluate(wlexpr(
            "f[{{{_u},{_v}}}]//N".format(_u=(u[1] - u[0]) / 2, _v=(v[1] - v[0]) / 2)
        ))

        if not any(elem in parametrization for elem in ',[]{}') \
                or not isinstance(temp, tuple) \
                or len(temp) != 3:
            Parametrization.logger.error("stopping Parametrization init")
            raise TypeError(
                "Parametrization.__init__(): "
                "'parametrization' must be a Wolfram Language ordered triple"
                " - {x[u,v], y[u,v], z[u,v]}"
            )
        if not isinstance(temp[0], (int, float)) \
                or not isinstance(temp[1], (int, float)) \
                or not isinstance(temp[2], (int, float)):
            Parametrization.logger.error("stopping Parametrization init")
            raise TypeError(
                "Parametrization.__init__(): "
                "parametrization coordinate function domains don't include U×V"
            )

        Parametrization.logger.info("Parametrization loaded")
        self.value = parametrization
        self._hash = ''
        self.u = u
        self.v = v

    def __repr__(self):
        return f"<Parametrization: {self.value} [{self.u[0]}, {self.u[1]}]×[{self.v[0]}, {self.v[1]}]>"

    def __str__(self):
        return self.value

    def hash(self):
        if self._hash == '':
            self._hash = hashlib.sha1(self.__repr__().encode('utf-8')).hexdigest()
            Parametrization.logger.info(f"{self.__repr__()} hashed: {self._hash}")
        return self._hash


class Builder:
    session = kernel.WolframLanguageSession()
    logger = šlog.configure(f"{name}.Builder")

    def __init__(self, divider: int, parametrization: Parametrization):
        Builder.logger.info("Builder loaded")
        self._divider = divider
        self.parametrization = parametrization

    def __repr__(self):
        return f"<Builder: {self.parametrization.__repr__()} DIVIDER={self._divider}>"

    def __str__(self):
        return f"• Builder for {self.parametrization} •"

    def load(self) -> OBJ:
        Builder.logger.info(f"loading {self.parametrization.hash()}.obj file")
        filename = f"surface/surfaces/{self.parametrization.hash()}.obj"
        if not os.path.exists(filename):
            Builder.logger.warning(".obj file missing, building...")
            self.build()
        return OBJ(filename=filename)

    def build(self):
        """
        Builds surface .obj file
        """
        Builder.logger.info(" ├── build started")

        split = []
        faces = []
        u_step = (self.parametrization.u[1] - self.parametrization.u[0]) / self._divider
        v_step = (self.parametrization.v[1] - self.parametrization.v[0]) / self._divider
        for i in range(0, self._divider + 1):
            for j in range(0, self._divider + 1):
                split.append([
                    self.parametrization.u[0] + i * u_step,
                    self.parametrization.v[0] + j * v_step
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

                if j != self._divider and i != self._divider:
                    faces.append([
                        i * (self._divider + 1) + j + 1,
                        (i + 1) * (self._divider + 1) + j + 1,
                        (i + 1) * (self._divider + 1) + j + 2,
                        i * (self._divider + 1) + j + 2
                    ])
                # Faces are defined by vertices in a counter-clockwise pattern, like so:
                #   4 3
                #   1 2
        Builder.logger.info(" ├── vertices & faces indexed")

        Builder.session.evaluate(wlexpr(f'x[{{u_,v_}}] = {self.parametrization}'))  # Load surface definition
        Builder.session.evaluate(wlexpr('unitnormal[x_][u_, v_] ='
                                        'Module[{U, V, xu, xv},'
                                        'xu = D[x[{U, V}], U];'
                                        'xv = D[x[{U, V}], V];'
                                        'Nx = Cross[xu, xv] /. {U -> u, V -> v};'
                                        'Simplify[Nx/Norm[Nx]]]'))  # Load unit normal expression
        Builder.session.evaluate(wlexpr('xn[{u_,v_}] = unitnormal[x][u,v]//N'))  # Load surface normal map

        vertices = Builder.session.evaluate(wl.Map(wlexpr('x'), split))
        if not all(isinstance(vertex[0], (int, float)) for vertex in vertices) \
                or not all(isinstance(vertex[1], (int, float)) for vertex in vertices) \
                or not all(isinstance(vertex[2], (int, float)) for vertex in vertices):
            Builder.logger.error(" └── vertices aren't all numbers, check your math")
            raise ValueError("some vertices aren't numbers")
        Builder.logger.info(" ├── vertices built")

        vertex_normals = Builder.session.evaluate(wl.Map(wlexpr('xn'), split))
        if not all(isinstance(v_normal[0], (int, float)) for v_normal in vertex_normals) \
                or not all(isinstance(v_normal[1], (int, float)) for v_normal in vertex_normals) \
                or not all(isinstance(v_normal[2], (int, float)) for v_normal in vertex_normals):
            Builder.logger.error(" └── vertex normals aren't all numbers, check your math")
            raise ValueError("some vertex normals aren't numbers")
        Builder.logger.info(" ├── vertex normals built")

        with open(f"surface/surfaces/{self.parametrization.hash()}.obj", mode='w+') as obj_file:
            obj_file.write(f"mtllib mtl.mtl\n")
            obj_file.write('o Cube_Cube.001\n')
            Builder.logger.debug(" ├── .obj file headers written")

            for vertex in vertices:
                obj_file.write(f'v {vertex[0]:f} {vertex[1]:f} {vertex[2]:f}\n')
            Builder.logger.debug(" ├── vertices written")

            for vn in vertex_normals:
                obj_file.write(f'vn {(-1 * vn[0]):f} {(-1 * vn[1]):f} {(-1 * vn[2]):f}\n')
            Builder.logger.debug(" ├── vertex normals written")

            obj_file.write('usemtl None\n')
            obj_file.write('s off\n')
            Builder.logger.debug(" ├── material written")

            for face in faces:
                obj_file.write(
                    f'f {face[0]}//{face[0]}'
                    f' {face[1]}//{face[1]}'
                    f' {face[2]}//{face[2]}'
                    f' {face[3]}//{face[3]}\n'
                )
            Builder.logger.debug(" ├── faces written")

            for i in range(0, self._divider - 1):
                obj_file.write('l')
                for j in range((i + 1) * (self._divider + 1) + 1, (i + 2) * (self._divider + 1) + 1):
                    obj_file.write(f' {j}')
                obj_file.write('\n')
            for j in range(2, self._divider + 1):
                obj_file.write('l')
                for i in range(j, j + self._divider * (self._divider + 1) + 1, self._divider + 1):
                    obj_file.write(f' {i}')
                obj_file.write('\n')
            Builder.logger.debug(" ├── lines written")

        Builder.logger.info(f" └── {self.parametrization.hash()}.obj built")
