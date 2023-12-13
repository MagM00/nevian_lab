import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image
import OpenGL.GL as gl
import OpenGL.GLU as glu
from pygame.locals import *
import pygame

class VideoPlayer:
    def __init__(self, window):
        self.window = window
        self.vid = None
        self.texture = None
        
        pygame.init()
        display = (1600, 900)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClearDepth(1.0)  
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glShadeModel(gl.GL_SMOOTH)
            
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, display[0]/display[1], 0.1, 100.0)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        
        # Other UI code
        
        self.update()
        
    def load_video(self, filename):
        self.vid = cv2.VideoCapture(filename)
              
    def update(self):
        if self.vid:
            ret, frame = self.vid.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glLoadIdentity()
            
            # Convert frame to Texture    
            self.texture = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
            gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MAG_FILTER,gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MIN_FILTER,gl.GL_LINEAR)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, frame.shape[1], frame.shape[0], 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, frame)
            
            # Draw texture to screen
            gl.glBegin(gl.GL_QUADS)
            gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0, -1.0,  0.0)
            gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f( 1.0, -1.0,  0.0)
            gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f( 1.0,  1.0,  0.0)
            gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0,  1.0,  0.0)
            gl.glEnd()
            
            pygame.display.flip()

root = tk.Tk()        
player = VideoPlayer(root)
root.mainloop()