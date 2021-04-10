''' nodes.py
Nodes are a method of making a once-off change to a spacevraft at some point in
the future. Each node has a time corresponding to the simulation time when it
should be executed. These nodes will actually execute at the first frame that
passes this time. (universe.time)

Nodes can either be points to recalculate the current orbit and apply course
corrections, or to calculate when to later perform a maneuver, and then set a
new node to execute that maneuver.
'''

import numpy as np

def sort_node(new, nodes):
    for existing_index in range(len(nodes)):
        if new.time < nodes[existing_index].time:
            nodes.insert[existing_index, new]
            break
    return nodes

class Node:
    def __init__(self, vessel, time):
        self.vessel = vessel
        self.time = time

    def run(universe):
        universe.nodes.pop(0)

class Plan(Node):
    def __init__(self, vessel, time, data):
        super().__init__(vessel, time)
        self.data = data

    def execute(universe):
        pass

class Maneuver(Node):
    def __init__(self, vessel, time, prograde, normal, radial):
        super().__init__(vessel, time)
        self.prograde = prograde
        self.normal = normal
        self.radial = radial

    def execute(universe):
        prograde(universe, self.vessel, self.prograde)
        normal(universe, self.vessel, self.normal)
        radial(universe, self.vessel, self.radial)

def prograde(universe, vessel, value):
    progradeVec = vessel.vel - vessel.primary.vel
    vessel.vel += value*(progradeVec/np.linalg.norm(progradeVec))

def normal(universe, vessel, value):
    progradeVec = vessel.vel - vessel.primary.vel
    normalVec = np.cross(vessel.pos - vessel.primary.pos, progradeVec)
    vessel.vel += value*(normalVec/np.linalg.norm(normalVec))

def radial(unvierse, vessel, value):
    radialVec = vessel.pos - vessel.primary.pos
    vessel.vel += value*(radialVec/np.linalg.norm(radialVec))
