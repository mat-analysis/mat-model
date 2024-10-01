# -*- coding: utf-8 -*-
"""
MAT-Tools: Python Framework for Multiple Aspect Trajectory Data Mining

The present application offers a tool, to support the user in the modeling of multiple aspect trajectory data. It integrates into a unique framework for multiple aspects trajectories and in general for multidimensional sequence data mining methods.
Copyright (C) 2022, MIT license (this portion of code is subject to licensing from source project distribution)

Created on Apr, 2024
Copyright (C) 2024, License GPL Version 3 or superior (see LICENSE file)

Authors:
    - Tarlis Portela
    - Vanessa Lago Machado
"""
from matmodel.base import Aspect

class Feature:
    """
    <Abstract> 
    Represents a feature that can be associated with a quality.

    Attributes:
    -----------
    quality (Quality, optional): 
        The quality of the feature.
    """
    def __init__(self, quality=None):
        self.quality = quality
        
#class IntervalFeature(Feature):
#    def __init__(self, quality=None):
#        Feature.__init__(self, quality)
#        
#class CellFeature(IntervalFeature):
#    def __init__(self, quality=None):
#        Feature.__init__(self, quality)
#        
#class AspectFeature(Feature):
#    def __init__(self, aspect, quality=None):
#        Feature.__init__(self, quality)
#        self.aspect = aspect
        
class DerrivedFeature(Feature, Aspect):
    """
    Represents a feature derived from an original aspect, extending both Feature and Aspect classes.

    Attributes:
    -----------
    value (any): 
        The value for the derived feature.
    original_aspect (Aspect): 
        The original aspect from which the feature is derived.
    quality (Quality, optional): 
        The quality associated with the feature. Defaults to None.
    """
    def __init__(self, value, original_aspect, quality=None):
        Feature.__init__(self, quality)
        Aspect.__init__(self, value)
        self.aspect = aspect