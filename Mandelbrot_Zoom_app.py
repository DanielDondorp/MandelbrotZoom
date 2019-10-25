#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 21:01:40 2019

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt
from mandelbrot import calculate_mandelbrot_set


class Mandelbrot_Zoom:
    def __init__(self):
        self.x_min = -2
        self.x_max = 0.5
        self.y_min = -1.25
        self.y_max = 1.25
        self.side = 1000
        self.n_iter = 100
        
        self.x_span = np.abs(self.x_max - self.x_min)
        self.y_span = np.abs(self.y_max - self.y_min)
        
        self.mb = self.get_mandelbrot()
        self.fig, self.ax = plt.subplots(figsize = (10,10))
        self.cmap = "nipy_spectral"
        self.img = self.ax.imshow(self.mb, cmap = self.cmap)
        
        self.fig.canvas.mpl_connect("key_press_event", self.handle_keypress_event)
        self.fig.canvas.mpl_connect("button_press_event", self.handle_mouse_event)
    
    def map_value(self, x, in_min, in_max, out_min, out_max):
        return (x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min
    
    def get_mandelbrot(self):
        return calculate_mandelbrot_set(self.x_min, self.x_max,
                                           self.y_min, self.y_max,
                                           self.side, self.side, self.n_iter)
    
    def draw(self):
        self.mb = self.get_mandelbrot()
        self.img.set_data(self.mb)
        self.img.autoscale()
        plt.draw()
        
    def zoom_in(self, x, y):
        self.x_span = np.abs(self.x_max - self.x_min) * 0.5
        self.y_span = np.abs(self.y_max - self.y_min) * 0.5
        self.x_min = x - self.x_span / 2
        self.x_max = x + self.x_span / 2
        self.y_min = y - self.y_span / 2
        self.y_max = y + self.y_span / 2
        self.draw()
        
    def zoom_out(self):
        self.x_span = np.abs(self.x_max - self.x_min) * 1.5
        self.y_span = np.abs(self.y_max - self.y_min) * 1.5
        self.x_min = self.map_value(self.x_min, self.x_min, self.x_max, 
                                    self.x_min - self.x_span/2, self.x_max + self.x_span/2)
        self.x_max = self.map_value(self.x_max, self.x_min, self.x_max, 
                                    self.x_min - self.x_span/2, self.x_max + self.x_span/2)
        self.y_min = self.map_value(self.y_min, self.y_min, self.y_max, 
                                    self.y_min - self.y_span/2, self.y_max + self.y_span/2)
        self.y_max = self.map_value(self.y_max, self.y_min, self.y_max, 
                                    self.y_min - self.y_span/2, self.y_max + self.y_span/2)
        self.draw()
        
    
        
    
    def handle_keypress_event(self, event):
        if event.key == "pageup":
            self.n_iter += 100
            self.draw()
        elif event.key == "pagedown":
            self.n_iter -= 100
            self.draw()
        elif event.key == "backspace":
            self.zoom_out()
        elif event.key == "enter":
            x = (self.x_min + self.x_max)/2
            y = (self.y_min + self.y_max)/2
            self.zoom_in(x, y)
        elif event.key == "left":
            self.x_min -= self.x_span/10
            self.x_max -= self.x_span/10
            self.draw()
        elif event.key == "right":
            self.x_min += self.x_span/10
            self.x_max += self.x_span/10
            self.draw()
        elif event.key == "up":
            self.y_min -= self.y_span/10
            self.y_max -= self.y_span/10
            self.draw()
        elif event.key == "down":
            self.y_min += self.y_span/10
            self.y_max += self.y_span/10
            self.draw()
        elif event.key == "x":
            self.savefig()
                
    def handle_mouse_event(self, event):
        if event.dblclick:
            x = self.map_value(event.xdata, 0, self.side, self.x_min, self.x_max)
            y = self.map_value(event.ydata, 0, self.side, self.y_min, self.y_max)            
            self.zoom_in(x,y)
            
    def savefig(self):
        plt.imsave("mb_img.png", self.mb, dpi = 600, cmap = self.cmap)
        
if __name__ == "__main__":
    mz = Mandelbrot_Zoom()
    plt.show()
