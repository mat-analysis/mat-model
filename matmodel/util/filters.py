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
def names2indexes(sel_attributes, attributes_desc):
    """
    Converts a list of selected attribute names into their corresponding indexes
    based on a provided list of attribute descriptors.

    Args:
    -----
    sel_attributes (list): 
        List of selected attribute names (strings).
    attributes_desc (list): 
        List of attribute descriptors, each containing a 'text' field.

    Returns:
    --------
    list: 
        List of indexes corresponding to the selected attribute names within `attributes_desc`.
    """
    return list(map(lambda y: attributes_desc.index(y), filter(lambda x: x['text'] in sel_attributes, attributes_desc)))

def attributes2names(attributes_desc):
    """
    Extracts the names (text field) of all attributes from the provided list of attribute descriptors.

    Args:
    -----
    attributes_desc (list): 
        List of attribute descriptors, each containing a 'text' field.

    Returns:
    --------
    list: 
        List of attribute names (strings).
    """
    return list(map(lambda y: y['text'], attributes_desc))