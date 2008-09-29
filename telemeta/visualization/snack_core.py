
from telemeta.core import *
from telemeta.visualization.api import IMediaItemVisualizer
from django.conf import settings
from Tkinter import Tk
import tkSnack
from tempfile import NamedTemporaryFile
import os
import random

class SnackCoreVisualizer(Component):
    """Parent class for tkSnack-based visualization drivers"""

    def get_snack_canvas(self):
        #id = "telemeta" + str(random.randrange(0,1000000))
        #self.tk_root = Tk(baseName=id)
        self.tk_root = Tk()
        tkSnack.initializeSnack(self.tk_root)
        canvas = tkSnack.SnackCanvas(height=200)
        canvas.pack()
        return canvas

    def get_snack_sound(self, media_item):        
        self.snd = tkSnack.Sound()
        self.snd.read(media_item.file.path)
        return self.snd
        
    def canvas_to_png_stream(self, canvas):

        psFile = NamedTemporaryFile(suffix='.ps')
        canvas.postscript({'file': psFile.name, 'height': 200, 'width': 300})
        pngFile = NamedTemporaryFile(suffix='.png')
        os.system('convert -resize 300x200 ' + psFile.name + ' ' + pngFile.name)
        psFile.close()

        buffer = pngFile.read(0xFFFF)
        while buffer:
            yield buffer
            buffer = pngFile.read(0xFFFF)

        pngFile.close()            
        self.cleanup()

    def cleanup(self): 
        self.snd.destroy()
        self.tk_root.destroy()

