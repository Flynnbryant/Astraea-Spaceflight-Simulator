''' entities.py
Cotnains required variables and methods for entity, body, and vessel classes.
Bodies are objects with significant mass (moons, planets, stars), vessels have
no mass and can be controlled. Entities include both bodies and vessels.
'''

import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from mechanics.simulation import *
from graphics.textures import *
from graphics.camera import *

class Entity():
    lineWidth = 1
    display_obj = gluNewQuadric()

    def __init__(self, name, pos, vel, color, primary):
        self.name = name
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.color = np.array(color)
        self.colorsmall = self.color/255
        self.primary = primary
        if self.primary == 'Sol':
            self.trace_detail = 2000
        else:
            self.trace_detail = 500

    def remove(self, universe):
        universe.entities.remove(self)
        universe.entitylength -= 1
        if self in universe.bodies:
            universe.bodies.remove(self)
        elif self in universe.vessels:
            universe.vessels.remove(self)

    def orbital_elements(self):
        rel_pos = self.pos - self.primary.pos
        rel_vel = self.vel - self.primary.vel
        self.eccentricity_vec = ((np.linalg.norm(rel_vel)**2)/self.primary.SGP - 1/np.linalg.norm(rel_pos))*rel_pos - rel_vel*(np.dot(rel_pos, rel_vel)/self.primary.SGP)
        self.eccentricity = np.linalg.norm(self.eccentricity_vec)
        self.semi_major_axis = -0.5*self.primary.SGP/(0.5*(np.linalg.norm(rel_vel))**2 - self.primary.SGP/np.linalg.norm(rel_pos))
        self.semi_minor_axis = self.semi_major_axis*np.sqrt(1-self.eccentricity**2)
        self.periapsis = self.semi_major_axis*(1-self.eccentricity)
        self.plane_vec = np.cross(rel_pos,rel_vel)
        self.inclination = np.arccos(self.plane_vec[2]/np.linalg.norm(self.plane_vec))
        self.ascending_node = np.cross(np.array([0,0,1]),np.cross(rel_pos, rel_vel))
        self.long_ascending = np.arccos(self.ascending_node[0]/np.linalg.norm(self.ascending_node))
        self.arg_periapsis = np.arccos(np.dot(self.ascending_node, self.eccentricity_vec)/(np.linalg.norm(self.ascending_node)*np.linalg.norm(self.eccentricity_vec)))
        if self.eccentricity_vec[2] <0:
            self.arg_periapsis = 2*np.pi - self.arg_periapsis
        if self.ascending_node[1] < 0:
            self.long_ascending = 2*np.pi - self.long_ascending

    def calculate_trace(self):
        x_translated = self.semi_major_axis * np.cos(2*np.pi * np.arange(0, 1, 1/self.trace_detail, dtype=np.float32)) - self.semi_major_axis + self.periapsis
        y_translated = self.semi_minor_axis * np.sin(2*np.pi * np.arange(0, 1, 1/self.trace_detail, dtype=np.float32))
        x_periapsis_rotation = x_translated * np.cos(self.arg_periapsis) - y_translated * np.sin(self.arg_periapsis)
        y_periapsis_rotation = x_translated * np.sin(self.arg_periapsis) + y_translated * np.cos(self.arg_periapsis)
        y_inclination_rotation = y_periapsis_rotation * np.cos(self.inclination)
        x_longitude_rotation = x_periapsis_rotation * np.cos(self.long_ascending) - y_inclination_rotation * np.sin(self.long_ascending)
        y_longitude_rotation = x_periapsis_rotation * np.sin(self.long_ascending) + y_inclination_rotation * np.cos(self.long_ascending)

        self.points = np.zeros((3, self.trace_detail), dtype=np.float32)
        self.points[0] = x_longitude_rotation
        self.points[2] = y_longitude_rotation
        self.points[1] = y_periapsis_rotation * np.sin(self.inclination)

    def update_trace(self):
        return (np.array([self.points[0] + self.primary.pos[0],
        self.points[1] + self.primary.pos[2],
        self.points[2] + self.primary.pos[1]])).T

class Vessel(Entity):
    def __init__(self, name, pos, vel, color, primary, deltav):
        super().__init__(name, pos, vel, color, primary)
        self.deltav = deltav
        self.radius = 100

class Body(Entity):
    def __init__(self, name, pos, vel, color, mass, radius, primary):
        super().__init__(name, pos, vel, color, primary)
        self.radius = radius
        self.mass = mass
        self.SGP = mass*6.67430*10**-11
        self.barySGP = self.SGP
        self.satellites = []
        self.satellite_table = np.array(5)
        self.deltav = False
        self.hill = 1*10**20
        #self.texture_id = self.read_texture('graphics/textures/jupiter_test.png')

    def drawPlanet(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.pos[0], self.pos[2], self.pos[1])
        glColor3f(self.colorsmall[0], self.colorsmall[1], self.colorsmall[2])
        gluSphere(self.display_obj, self.radius, 32, 16)

    def drawPlanetTexture(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
        glutSolidSphere(self.radius, 50, 50)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        glutSwapBuffers()

    def read_texture(self, filename):
        img = Image.open(filename)
        img_data = np.array(list(img.getdata()), np.int8)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return texture_id
