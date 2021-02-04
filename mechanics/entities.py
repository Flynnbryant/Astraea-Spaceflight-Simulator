''' entities.py
Cotnains required variables and methods for entity, body, and vessel classes.
Bodies are objects with significant mass (moons, planets, stars), vessels have
no mass and can be controlled. Entities include both bodies and vessels.
'''

import numpy as np
from OpenGL.GLU import *

class Entity():
    lineWidth = 1
    display_obj = gluNewQuadric()

    def __init__(self, name, pos, vel, color, primary):
        self.name = name
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.color = np.array(color)
        self.primary = primary

    # Wont be needed with metaclass instance iteration
    def remove(self, universe):
        universe.entities.remove(self)
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
        x_translated = self.semi_major_axis * np.cos(2*np.pi * np.arange(0, 1, 1/self.trace_detail, dtype=np.float128)) - self.semi_major_axis + self.periapsis
        y_translated = self.semi_minor_axis * np.sin(2*np.pi * np.arange(0, 1, 1/self.trace_detail, dtype=np.float128))
        x_periapsis_rotation = x_translated * np.cos(self.arg_periapsis) - y_translated * np.sin(self.arg_periapsis)
        y_periapsis_rotation = x_translated * np.sin(self.arg_periapsis) + y_translated * np.cos(self.arg_periapsis)
        y_inclination_rotation = y_periapsis_rotation * np.cos(self.inclination)
        x_longitude_rotation = x_periapsis_rotation * np.cos(self.long_ascending) - y_inclination_rotation * np.sin(self.long_ascending)
        y_longitude_rotation = x_periapsis_rotation * np.sin(self.long_ascending) + y_inclination_rotation * np.cos(self.long_ascending)

        self.points = np.zeros((3, self.trace_detail), dtype=np.float64)
        self.points[0] = x_longitude_rotation
        self.points[2] = y_longitude_rotation
        self.points[1] = y_periapsis_rotation * np.sin(self.inclination)

    def update_trace(self):
        return (np.array([self.points[0] + self.primary.pos[0],
        self.points[1] + self.primary.pos[2],
        self.points[2] + self.primary.pos[1]])).T

class Vessel(Entity):
    def __init__(self, name, pos, vel, color, deltav):
        super().__init__(name, pos, vel, color)
        self.deltav = deltav
        self.radius = 100

class Body(Entity):
    def __init__(self, name, pos, vel, color, mass, radius, primary):
        super().__init__(name, pos, vel, color, primary)
        self.radius = radius
        self.mass = mass
        self.SGP = mass*6.67430*10**-11
        self.satellites = []
        self.deltav = False
        self.trace_detail = 2000 #body radius, orbit radius, camera distance
