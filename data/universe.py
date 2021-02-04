''' universe.py
Loads the required starting data for the simulation, and initialises variables.
The input starting data for each object is summarised in sol_system.txt, and
was downloaded from JPL's HORIZONS system:
    https://ssd.jpl.nasa.gov/horizons.cgi#top
The raw data files can be found in data/raw_cartesian_data
'''


from analysis.nodes import *
from analysis.profiler import *
import numpy as np
from mechanics.entities import *

def sn(datastr):
    datalist = datastr.replace(',','').lower().split('e')
    return np.float64(datalist[0])*10**int(datalist[1])

class Universe:
    def __init__(self, focus):
        self.time = 1609419600
        self.usertime = 3600.0 *2 #86400.0/2
        self.profile = Profile()
        self.nodes = [Node(False, 32503680000)]
        self.tracecount = 0 #Need to modify this
        self.bodies = []
        self.vessels = []
        self.entities = []
        self.focus = 3

        with open('data/sol_system.txt', 'r') as f:
            for line in f.readlines()[1:]:
                data = line.split()
                primary = False
                if len(self.bodies):
                    for body in self.bodies:
                        if body.name == str(data[1]):
                            primary = body

                newbody = Body(str(data[0]),
                    np.array([sn(data[4]),sn(data[5]),sn(data[6])]) *1000,
                    np.array([sn(data[7]),sn(data[8]),sn(data[9])]) *1000,
                    np.array(data[10].split(","), dtype=np.ubyte),
                    sn(data[2]),
                    int(data[3]),
                    primary)

                self.bodies.append(newbody)
                self.entities.append(newbody)
                if newbody.name == focus:
                    self.focus = self.entities.index(body)+1
                if newbody.primary:
                    newbody.primary.satellites.append(newbody)
                    newbody.orbital_elements()
                    newbody.trace = newbody.calculate_trace()

        self.outerscale = np.linalg.norm(self.bodies[-1].pos-self.bodies[0].pos)/100
