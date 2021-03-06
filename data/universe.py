''' universe.py
Loads the required starting data for the simulation, and initialises variables.
The input starting data for each object is summarised in sol_system.txt, and
was downloaded from JPL's HORIZONS system:
    https://ssd.jpl.nasa.gov/horizons.cgi#top
'''
import numpy as np
from analysis.nodes import *
from analysis.profiler import *
from mechanics.entities import *

def sn(datastr):
    datalist = datastr.replace(',','').lower().split('e')
    return np.float64(datalist[0])*10**int(datalist[1])

class Universe:
    def __init__(self, focus = 'Earth', profile = False, rate = 1):
        self.time = 1609419600
        self.tracecount = 0
        self.usertime = rate
        self.profile = Profile(profile)
        self.nodes = [Node(False, 32503680000)]
        self.bodies = []
        self.vessels = []
        self.entities = []
        self.focus = 3

        with open('data/sol_system.txt', 'r') as f:
            for line in f.readlines()[1:]:
                data = line.split()

                if data[1] != 'Vessel':
                    if len(self.bodies):
                        for body in self.bodies:
                            if body.name == str(data[1]):
                                primary = body
                    else:
                        primary = False

                    newbody = Body(str(data[0]),
                    np.array([sn(data[4]),sn(data[5]),sn(data[6])]) *1000,
                    np.array([sn(data[7]),sn(data[8]),sn(data[9])]) *1000,
                    np.array(data[10].split(","), dtype=np.ubyte),
                    sn(data[2]), int(data[3]), primary)

                    self.bodies.append(newbody)
                    self.entities.append(newbody)
                    if newbody.name == focus:
                        self.focus = self.entities.index(newbody)
                    if newbody.primary:
                        newbody.primary.satellites.append(newbody)
                        newbody.primary.barySGP += newbody.SGP
                        newbody.orbital_elements()
                        newbody.trace = newbody.calculate_trace()
                        newbody.hill = 1*newbody.semi_major_axis*((newbody.mass/(3*newbody.primary.mass))**(1/3))

                else:
                    newvessel = Vessel(str(data[0]),
                    np.array([sn(data[4]),sn(data[5]),sn(data[6])]) *1000,
                    np.array([sn(data[7]),sn(data[8]),sn(data[9])]) *1000,
                    np.array(data[10].split(","), dtype=np.ubyte),
                    self.bodies[5],1000000)

                    self.vessels.append(newvessel)
                    self.entities.append(newvessel)
                    newvessel.orbital_elements()
                    newvessel.trace = newvessel.calculate_trace()

        self.outerscale = np.linalg.norm(self.bodies[-1].pos-self.bodies[0].pos)/100
        self.entitylength = len(self.entities)
        self.barycentre_table = np.array(5)
        subtract = self.entities[self.focus % self.entitylength].pos
        for entity in self.entities:
            entity.pos = entity.pos - subtract
