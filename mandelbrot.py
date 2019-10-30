#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 20:50:52 2019

@author: daniel
"""

from numba import jit, vectorize, guvectorize, float64, complex64, int32, float32, int64
import numpy as np


@jit(int32(complex64, int32))
def mandelbrot(c,maxiter):
    nreal = 0
    real = 0
    imag = 0
    for n in range(maxiter):
        nreal = real*real - imag*imag + c.real
        imag = 2* real*imag + c.imag
        real = nreal;
        if real * real + imag * imag > 4.0:
            return n
    return 0

@guvectorize([(complex64[:], int32[:], int32[:])], '(n),()->(n)',target='parallel')
def mandelbrot_numpy(c, maxit, output):
    maxiter = maxit[0]
    for i in range(c.shape[0]):
        output[i] = mandelbrot(c[i],maxiter)


def calculate_mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
    r1 = np.linspace(xmin, xmax, width, dtype=np.float32)
    r2 = np.linspace(ymin, ymax, height, dtype=np.float32)
    c = r1 + r2[:,None]*1j
    n3 = mandelbrot_numpy(c,maxiter)
    return (n3)


@jit
def calculate_mandelbrot_set_slow(x_min = -2, x_max = 2, y_min = -2, y_max = 2, width = 800, height = 600, n_iter = 50):
    
    x_values = np.linspace(x_min, x_max, width)
    y_values = np.linspace(y_min, y_max, height)
    mandelbrotset = np.empty((len(x_values), len(y_values)))
    for i in range(width):
        for j in range(height):
            mandelbrotset[i,j] = mandelbrot_slow(x_values[i] + 1j*y_values[j],n_iter)
    return mandelbrotset.T
@jit
def mandelbrot_slow(c,n_iter):
    z = c
    for n in range(n_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return 0

def calculate_mandelbrot_set_very_slow(x_min = -2, x_max = 2, y_min = -2, y_max = 2, width = 800, height = 600, n_iter = 50):
    x_values = np.linspace(x_min, x_max, width, np.float128)
    y_values = np.linspace(y_min, y_max, height, np.float128)
    mandelbrotset = np.empty((len(x_values), len(y_values)))
    for i in range(width):
        for j in range(height):
            mandelbrotset[i,j] = mandelbrot_very_slow(x_values[i] + 1j*y_values[j],n_iter)
    return mandelbrotset.T


def mandelbrot_very_slow(c,n_iter):
    z = c
    for n in range(n_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return 0