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

class Quality:
    """
    Represents the quality of a feature, including its value, size, and other dimensional properties.

    Attributes:
    -----------
    value (any): 
        The value of the quality.
    size (int, optional): 
        The size of the feature. Defaults to 1.
    start (int, optional): 
        The starting point index of the extracted feature. Defaults to 0.
    dimensions (int, optional): 
        The number of dimensions for the feature. Defaults to 1.
    """
    def __init__(self, value, size=1, start=0, dimensions=1):
        self.value = value
        self.size = size
        self.start = start
        self.dimensions = dimensions