''' labels.py
Class for fixed labels as part of the user interface
'''

import pyglet
from datetime import datetime
from graphics.interface import *

class Text():
    def __init__(self, batch_information, label_position, label_dimensions, text_size = 14, color = [0, 255, 255, 255], text_bold = False, text = ''):
        self.x = label_position[0]
        self.y = label_position[1]
        self.width = label_dimensions[0]
        self.height = label_dimensions[1]
        self.initial_text = text
        self.final_output = text
        self.label_text = pyglet.text.Label(
            self.final_output,
            batch = batch_information.ui_batch,
            group = batch_information.foreground,
            font_name = "Arial",
            font_size = text_size,
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            anchor_x = "left",
            anchor_y = "bottom",
            align = "center",
            color = color,
            bold = text_bold,
            multiline = True)
        self.label_text.content_valign = "center"

    def edit_text(self, new):
        self.label_text.text = self.initial_text.replace('', new)

def updateLabels(user_interface, verse):
    user_interface.timestep_text.edit_text(str(round(verse.usertime,3)) + ' x time')
    #user_interface.periapsis_text.edit_text(str(round(verse.entities[verse.focus].periapsis)) + 'm')
    user_interface.time_text.edit_text(str(datetime.fromtimestamp(verse.time).strftime("%Y, %b %d, %H:%M:%S.%f"))[:-3] + ' UTC')
