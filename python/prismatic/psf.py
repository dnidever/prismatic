import os
import numpy as np

# How do I make this completely generalized, i.e.
# not assuming that the trace is "along" a certain axis

# what's the generalized way of making a path/curve in the x-y
# plane?  it's basically a set of (x,y) points

        
class SpectrumPSF():

    def __init__(self,mode='optimal'):
        if mode not in ['optimal']:
            return ValueError('mode '+str(mode)+' not supported')
        self.mode = mode
        self._tracepars = None
        
    def __call__(self,pars=None):
        """ Generate the PSF."""
        pass

        # Default is to return the entire model 2D PSF 
        
    def train(self,data):
        """ Define the PSF using the input data and parameters."""
        pass

    def fit(self,data):
        """ Fit the 2D PSF on an image."""
        pass

    def trace(self,x=None):
        """ Return the trace for the input x-range."""
        if self._tracepars is None:
            raise ValueError('Trace parameters not set yet')
        
    def model(self,x=None):
        """ Return the 2D model for the input x-range."""
        pass
