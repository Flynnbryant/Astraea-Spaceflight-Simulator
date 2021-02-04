''' interface.py
'''

from pyglet import *
import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from graphics.labels import *

class BatchInformation():
    def __init__(self):
        self.ui_batch = pyglet.graphics.Batch()
        self.polygon_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.midground = pyglet.graphics.OrderedGroup(1)
        self.foreground = pyglet.graphics.OrderedGroup(2)

class Functionality():
	def __init__(self, ui_instance):
		self.ui = ui_instance

	def run(self):
		pass

	def ui_mouse_press(self, x, y, button, modifiers):
		pass

class UserInterface():
    def __init__(self, window, screen):
        self.time_text = Text(batch_information,
            [screen.width * 0.54, screen.height * -0.0],
            [screen.width * 0.5, screen.height * 0.1])

        self.timestep_text = Text(batch_information,
            [screen.width * 0.77, screen.height * 0.05],
            [screen.width * 0.3, screen.height * 0.1])

        self.periapsis_text = Text(batch_information,
            [screen.width * 0.25, screen.height * 0.8],
            [screen.width * 0.3, screen.height * 0.1])

        self.window_width = window.width
        self.window_height = window.height

    def draw_ui(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        gluOrtho2D(0, self.window_width, 0, self.window_height)
        batch_information.polygon_batch.draw()
        pyglet.gl.glLineWidth(2) #needed for other graphics apparently
        batch_information.ui_batch.draw()

    def ui_mouse_press(self, x, y, button, modifiers):
        self.check_button_press(x, y, button)

batch_information = BatchInformation()
