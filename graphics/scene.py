''' scene.py
This file decides what bodies (planets, moons, Sol) need to be drawn, as well
as labels and orbital prediction ellipses. Then it will call the functions in
camera.py to actually do the drawing. The drawScene function is called every
frame from astraea.py. At the end of the drawScene function, the ui elements
are called to be drawn.
'''

from pyglet import *
import numpy as np
from OpenGL.GL import *
from mechanics.entities import *
from graphics.interface import *
from graphics.labels import *

def drawScene(universe, camera, keys, window):
    window.clear()
    camera.moveCamera()
    camera.focus_entity = universe.entities[universe.focus % universe.entitylength]
    subtract = universe.entities[universe.focus % len(universe.entities)].pos
    for entity in universe.entities:
        entity.pos = entity.pos - subtract
    camera.drawPlanet(universe.entities[0])

    if camera.focus_entity is universe.entities[0]:
        for object in universe.entities[0].satellites:
            camera.drawTrace(object, 1)
        for vessel in universe.vessels:
            if vessel.primary is universe.entities[0]:
                camera.drawTrace(vessel, 1)
        for object in universe.entities[0].satellites:
            camera.drawEntityLabel(object, 1)
        for vessel in universe.vessels:
            if vessel.primary is universe.entities[0]:
                camera.drawEntityLabel(vessel, 1)
    else:
        strength = max(1,np.abs(1/(2*camera.pos[2]+1)))
        local_planet = camera.focus_entity
        if camera.focus_entity.primary.primary:
            local_planet = camera.focus_entity.primary
            if local_planet.primary.primary:
                local_planet = local_planet.primary
        if camera.pos[2] < -0.5:
            for object in universe.entities[0].satellites:
                if object is local_planet:
                    camera.drawTrace(object, 1)
                else:
                    camera.drawTrace(object, strength)
            #camera.drawTrace(universe.vessels[0], 1)
            for object in universe.entities[0].satellites:
                if object is local_planet:
                    camera.drawEntityLabel(object, 1)
                else:
                    camera.drawEntityLabel(object, strength)
        else:
            camera.drawPlanet(local_planet)
            camera.drawTrace(local_planet, 1)
            for object in local_planet.satellites:
                if camera.pos[2] > -0.05:
                    camera.drawPlanet(object)
                camera.drawTrace(object, strength)
            camera.drawTrace(universe.vessels[0], 1)
            for object in local_planet.satellites:
                camera.drawEntityLabel(object, strength)
            camera.drawEntityLabel(local_planet, 1)

    camera.drawEntityLabel(universe.entities[0], 1)
    camera.drawEntityLabel(universe.vessels[0], 1)
    universe.profile.add('objects')
    camera.run_graphics.run()
    camera.user_interface.draw_ui()
    camera.fps_display.draw()
    updateLabels(camera.user_interface, universe)
    universe.profile.add('interface')
    glFlush()
