''' controls.py
Every frame, astraea.py in the update function will call this function.
simulation_controls will then check if any keys are being pressed, and move
the camera, or adjust the simulation or vessel accordingly. In the case of
controls that produce a thrust on the vessel (prograde, normal, and radial
functions) these are run from analysis/nodes.py
'''
import numpy as np
import pyglet

def simulation_controls(universe, camera, window, keys):
    window.push_handlers(keys)
    if any(keys):
        if keys[pyglet.window.key.P]:
            universe.usertime *= 1.1
        elif keys[pyglet.window.key.O]:
            universe.usertime *= 0.9
        if  keys[pyglet.window.key.EQUAL]:
            camera.pos[2] *= 0.9001
            camera.pos[2] = np.clip(camera.pos[2], -100, -camera.focus_entity.radius*camera.scale_factor*3)
        elif keys[pyglet.window.key.MINUS]:
            camera.pos[2] *= 1.1001
            camera.pos[2] = np.clip(camera.pos[2], -100, -camera.focus_entity.radius*camera.scale_factor*3)
        if keys[pyglet.window.key.UP] or keys[pyglet.window.key.W]:
            camera.vertical_rot += 2
            camera.vertical_rot = np.clip(camera.vertical_rot, -90, 90)
        elif keys[pyglet.window.key.DOWN] or keys[pyglet.window.key.S]:
            camera.vertical_rot -= 2
            camera.vertical_rot = np.clip(camera.vertical_rot, -90, 90)
        if keys[pyglet.window.key.A] or keys[pyglet.window.key.LEFT]:
            camera.horizontal_rot += 2
        elif keys[pyglet.window.key.D] or keys[pyglet.window.key.RIGHT]:
            camera.horizontal_rot -= 2
        if keys[pyglet.window.key.F]:
            if camera.switch == False:
                universe.focus += -1
                camera.switch = True
        elif keys[pyglet.window.key.G]:
            if camera.switch == False:
                universe.focus += 1
                camera.switch = True
        else:
            camera.switch = False
    #universe.profile.add('controls')
