import numpy as np

''' Calculation of the semiMajorAxis or semiMinorAxis (geometric properties of an ellipse) of an orbit of the entity around the entity.primary'''
def semiMajorAxis(entity):
    return -0.5*entity.primary.SGP/(0.5*(np.linalg.norm(entity.vel-entity.primary.vel))**2 - entity.primary.SGP/np.linalg.norm(entity.primary.pos - entity.pos))
def semiMinorAxis(entity):
    return semiMajorAxis(entity)*np.sqrt(1-eccentricity(entity)**2)



''' Calculation of the apoapsis or periapsis (highest or lowest point) of an orbit of the entity around the entity.primary'''
def apoapsis(entity):
    return semiMajorAxis(entity)*(1+eccentricity(entity))
def periapsis(entity):
    return semiMajorAxis(entity)*(1-eccentricity(entity))



''' Calclulation of the orbital period of an orbit of the entity around the entity.primary'''
def period(entity):
    return 2*np.pi*((semiMajorAxis(entity)**3)/entity.primary.SGP)**(1/2)



''' Calculation of the eccentricity (how elliptical) of an orbit of the entity around the entity.primary'''
def relative(target, entity):
    return target.pos-entity.pos, target.vel - entity.vel
def eccenVec(entity):
        distVec, velVec = relative(entity.primary, entity)
        return ((np.linalg.norm(velVec)**2)/entity.primary.SGP - 1/np.linalg.norm(distVec))*distVec - velVec*(np.dot(distVec, velVec)/entity.primary.SGP)
def eccentricity(entity):
    distVec, velVec = relative(entity, entity.primary)
    return np.linalg.norm(((np.linalg.norm(velVec)**2)/entity.primary.SGP - 1/np.linalg.norm(entity.primary.pos - entity.pos))*distVec - velVec*(np.dot(distVec, velVec)/entity.primary.SGP))



''' Calculations relating to the inclination of entities orbit'''
def planeVec(entity, reference):
    #return np.cross(entity.vel-reference.vel,entity.pos-reference.pos)
    return np.cross(entity.pos-reference.pos,entity.vel-reference.vel)
def vectorAngle(vec1, vec2):
    return np.arccos(np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
def ascendingNodeVec(entity):
    return np.cross(planeVec(entity,entity.primary),np.array([0,0,1]))
    #return np.cross(np.array([0,0,1]),planeVec(entity,entity.primary))



''' Orbital Element Angles '''
def argumentOfPeriapsis(entity):
    ascendingNode = ascendingNodeVec(entity)
    eccentricityVec = eccenVec(entity)
    argumentOfPeriapsis = np.arccos(np.dot(ascendingNode, eccentricityVec)/(np.linalg.norm(ascendingNode)*np.linalg.norm(eccentricityVec)))
    if eccentricityVec[2] > 0:
        argumentOfPeriapsis = 2*np.pi - argumentOfPeriapsis
    return argumentOfPeriapsis
def longitudeOfAscendingNode(entity, referenceBody):
    ascendingNode = ascendingNodeVec(entity)
    longitudeOfAscendingNode = np.arccos(ascendingNode[0]/np.linalg.norm(ascendingNode))
    if ascendingNode[1] < 0:
        longitudeOfAscendingNode = np.pi - longitudeOfAscendingNode
    return longitudeOfAscendingNode


def bodyImportance(entity, verse, rank):
    pass
    #return body, significance

'''
    accelerations = []
    correspondingBodies = []


    accelerations = []
    correspondingBodies = []
    for gravbody in bodies:
        if gravbody is not entity:
            accelerations.append(gravbody.mass/np.linalg.norm(gravbody.pos - entity.pos)**2)
            correspondingBodies.append(gravbody)
    rankedAccelerations = sorted(accelerations, reverse = True)
    body = correspondingBodies[accelerations.index(rankedAccelerations[rank-1])]
    #if rank < len(bodies):
    #    significance = rankedAccelerations[rank]/rankedAccelerations[rank-1]
    #else:
    significance = 1
    return body, significance
'''

''' General tools '''
def unitvec(vec):
    return vec/np.linalg.norm(vec)

def hillsphere(body):
    return(semiMajorAxis(body)*(1-eccentricity(body))*(body.mass/body.primary.mass)**(1/3))
