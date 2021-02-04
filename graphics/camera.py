''' camera.py
Contains all drawing functions, called by scene.py that will display the
spheres, labels, and orbit prediction lines to the screen. It also handles how
the camera moves by default (not including user controls, which are handled in
mechanics/controls.py)
'''


from pyglet import *
import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *
from mechanics.entities import *
from graphics.interface import *
from graphics.labels import *
from graphics.interface import *

class Camera:
    def __init__(self, window):
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.pos = np.array([0., 0., -2.])
        self.horizontal_rot = 0
        self.vertical_rot = 15
        self.tilt = 0
        self.focus = 0
        self.switch = False
        self.window_width = window.width
        self.window_height = window.height
        self.scale_factor = 1/100000000000
        self.screen = (pyglet.canvas.Display()).get_default_screen()
        self.user_interface = UserInterface(window, self.screen)
        self.run_graphics = Functionality(self.user_interface)
        self.fps_display = pyglet.window.FPSDisplay(window=window)

    def drawPlanet(self, body):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(body.pos[0], body.pos[2], body.pos[1])
        glColor3f(body.color[0]/255, body.color[1]/255, body.color[2]/255)
        gluSphere(body.display_obj, body.radius, 64, 32)

    def drawTrace(self, entity, strength):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glColor3f(1, 1, 1)
        glLineWidth(entity.lineWidth)
        glColor3f(entity.color[0]/(strength*255), entity.color[1]/(strength*255), entity.color[2]/(strength*255))
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, entity.update_trace())
        glDrawArrays(GL_LINE_LOOP, 0, entity.trace_detail)
        glDisableClientState(GL_VERTEX_ARRAY)

    def moveCamera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glTranslatef(0, 0, 0)
        gluPerspective(45, self.window_width/self.window_height, 0.00001, 2000.0)
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glRotatef(self.tilt, 0, 0, 1)
        glRotatef(self.vertical_rot, 1, 0, 0)
        glRotatef(self.horizontal_rot, 0, 1, 0)
        glScalef(self.scale_factor, self.scale_factor, self.scale_factor)
        glTranslatef(-self.focus_entity.pos[0], -self.focus_entity.pos[2], -self.focus_entity.pos[1])

    def drawEntityLabel(self, entity, strength):
        glDisable(GL_DEPTH_TEST)
        self.moveCamera()

        projection_matrix = glGetFloatv(GL_PROJECTION_MATRIX)
        vec = np.array([entity.pos[0] + entity.radius*np.sin(np.radians(self.tilt)), entity.pos[2] + entity.radius*np.cos(np.radians(self.tilt)), entity.pos[1], 1])
        b = np.dot(vec, projection_matrix)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        x = b[0]/b[3]
        y = b[1]/b[3]
        z = b[2]/b[3]

        glColor3f(entity.color[0]/(255*strength), entity.color[1]/(255*strength), entity.color[2]/(255*strength))
        glBegin(GL_TRIANGLES)
        glVertex3f(x, y, z)
        glVertex3f(x-0.015, y+0.03, z)
        glVertex3f(x+0.015, y+0.03, z)
        glEnd()
        gluOrtho2D(-self.window_width//2, self.window_width//2, -self.window_height//2, self.window_height//2)

        if z < 1:
            label = pyglet.text.Label(
                entity.name,
                font_name='Arial',
                font_size=12,
                x=x*(self.window_width*0.5),
                y=(y + 0.05)*(self.window_height*0.5),
                color = (int(entity.color[0]/strength), int(entity.color[1]/strength), int(entity.color[2]/strength), 255),
                width=20,
                height=10,
                align='center',
                anchor_x='center', anchor_y='bottom'
            )
            label.content_valign = 'bottom'
            label.draw()

        glEnable(GL_DEPTH_TEST)
