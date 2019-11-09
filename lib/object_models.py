import os
import json
from OpenGL.GL import *
from .model_rendering import (GenericObject, Model, TexturedModel,
                              GenericFlyer, GenericCrystallWall, GenericLongLegs, GenericChappy, GenericSnakecrow,
                              GenericSwimmer, Cube)


class ObjectModels(object):
    def __init__(self):
        self.models = {}
        self.generic = GenericObject()
        self.generic_flyer = GenericFlyer()
        self.generic_longlegs = GenericLongLegs()
        self.generic_chappy = GenericChappy()
        self.generic_snakecrow = GenericSnakecrow()
        self.generic_swimmer = GenericSwimmer()
        self.cube = Cube()
        self.redcube = Cube((1.0, 0.0, 0.0, 1.0))
        self.bluecube = Cube((0.1, 0.1, 8.0, 1.0))

        genericmodels = {
            "Chappy": self.generic_chappy,
            "Flyer": self.generic_flyer,
            "Longlegs": self.generic_longlegs,
            "Snakecrow": self.generic_snakecrow,
            "Swimmer": self.generic_swimmer
        }

        with open("resources/enemy_model_mapping.json", "r") as f:
            mapping = json.load(f)
            for enemytype, enemies in mapping.items():
                if enemytype in genericmodels:
                    for name in enemies:
                        self.models[name.title()] = genericmodels[enemytype]

        with open("resources/unitsphere.obj", "r") as f:
            self.sphere = Model.from_obj(f, rotate=True)

        with open("resources/unitcylinder.obj", "r") as f:
            self.cylinder = Model.from_obj(f, rotate=True)

        with open("resources/arrow_head.obj", "r") as f:
            self.arrow_head = Model.from_obj(f, rotate=True, scale=300.0)

    def init_gl(self):
        for dirpath, dirs, files in os.walk("resources/objectmodels"):
            for file in files:
                if file.endswith(".obj"):
                    filename = os.path.basename(file)
                    objectname = filename.rsplit(".", 1)[0]
                    self.models[objectname] = TexturedModel.from_obj_path(os.path.join(dirpath, file), rotate=True)
        for cube in (self.cube, self.redcube, self.bluecube):
            cube.generate_displists()

        self.generic.generate_displists()

        # self.generic_wall = TexturedModel.from_obj_path("resources/generic_object_wall2.obj", rotate=True, scale=20.0)

    def draw_arrow_head(self, frompos, topos):
        glPushMatrix()
        dir = topos-frompos
        dir.normalize()

        glMultMatrixf([dir.x, -dir.z, 0, 0,
                       -dir.z, -dir.x, 0, 0,
                       0, 0, 1, 0,
                       topos.x, -topos.z, topos.y, 1])
        self.arrow_head.render()
        glPopMatrix()
        #glBegin(GL_LINES)
        #glVertex3f(frompos.x, -frompos.z, frompos.y)
        #glVertex3f(topos.x, -topos.z, topos.y)
        #glEnd()



    def draw_sphere(self, position, scale):
        glPushMatrix()

        glTranslatef(position.x, -position.z, position.y)
        glScalef(scale, scale, scale)

        self.sphere.render()
        glPopMatrix()

    def draw_sphere_last_position(self, scale):
        glPushMatrix()

        glScalef(scale, scale, scale)

        self.sphere.render()
        glPopMatrix()

    def draw_cylinder(self,position, radius, height):
        glPushMatrix()

        glTranslatef(position.x, -position.z, position.y)
        glScalef(radius, height, radius)

        self.cylinder.render()
        glPopMatrix()

    def draw_cylinder_last_position(self, radius, height):
        glPushMatrix()

        glScalef(radius, radius, height)

        self.cylinder.render()
        glPopMatrix()

    def render_generic_position(self, position, selected):
        self._render_generic_position(self.cube, position, selected)

    def render_generic_position_colored(self, position, selected, cubename):
        self._render_generic_position(getattr(self, cubename), position, selected)

    def render_generic_position_rotation(self, position, rotation, selected):
        glPushMatrix()
        glTranslatef(position.x, -position.z, position.y)
        mtx = rotation.mtx
        #glBegin(GL_LINES)
        #glVertex3f(0.0, 0.0, 0.0)
        #glVertex3f(mtx[0][0] * 2000, mtx[0][1] * 2000, mtx[0][2] * 2000)
        #glEnd()

        glMultMatrixf(mtx)

        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        glVertex3f(0.0, 0.0, 750.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(1000.0, 0.0, 0.0)
        glEnd()


        #glMultMatrixf(rotation.mtx[])
        self.generic.render(selected=selected)

        glPopMatrix()

    def _render_generic_position(self, cube, position, selected):
        glPushMatrix()
        glTranslatef(position.x, -position.z, position.y)
        cube.render(selected=selected)

        glPopMatrix()

    def render_generic_position_colored_id(self, position, id):
        glPushMatrix()
        glTranslatef(position.x, -position.z, position.y)
        self.cube.render_coloredid(id)

        glPopMatrix()

    def render_generic_position_rotation_colored_id(self, position, rotation, id):
        glPushMatrix()
        glTranslatef(position.x, -position.z, position.y)
        mtx = rotation.mtx
        #glMultMatrixf(rotation.mtx[])
        self.generic.render_coloredid(id)

        glPopMatrix()


    def render_line(self, pos1, pos2):
        pass

    def render_object(self, pikminobject, selected):
        glPushMatrix()

        glTranslatef(pikminobject.position.x, -pikminobject.position.z, pikminobject.position.y)
        if "mEmitRadius" in pikminobject.unknown_params and pikminobject.unknown_params["mEmitRadius"] > 0:
            self.draw_cylinder_last_position(pikminobject.unknown_params["mEmitRadius"]/2, 50.0)

        glRotate(pikminobject.rotation.x, 1, 0, 0)
        glRotate(pikminobject.rotation.y, 0, 0, 1)
        glRotate(pikminobject.rotation.z, 0, 1, 0)

        if pikminobject.name in self.models:
            self.models[pikminobject.name].render(selected=selected)
        else:
            glDisable(GL_TEXTURE_2D)
            self.generic.render(selected=selected)

        glPopMatrix()

    def render_object_coloredid(self, pikminobject, id):
        glPushMatrix()

        glTranslatef(pikminobject.position.x, -pikminobject.position.z, pikminobject.position.y)
        glRotate(pikminobject.rotation.x, 1, 0, 0)
        glRotate(pikminobject.rotation.y, 0, 0, 1)
        glRotate(pikminobject.rotation.z, 0, 1, 0)

        if pikminobject.name in self.models:
            self.models[pikminobject.name].render_coloredid(id)
        else:
            self.generic.render_coloredid(id)


        glPopMatrix()