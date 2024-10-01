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
from matmodel.base.MultipleAspectSequence import Trajectory, Point

class RepresentativeTrajectory(Trajectory):
    """
    Represents a trajectory that serves as a representative of a group or cluster of trajectories.

    Inherits from:
        - Trajectory: A sequence of points, each described by multiple aspects.

    Attributes:
    -----------
        Inherits all attributes from the Trajectory class.
    """
    def __init__(self, tid, label, new_points, data_desc):
        """
        Initializes a RepresentativeTrajectory object.

        Args:
        -----
        tid (int): 
            The trajectory ID.
        label (str): 
            The label of the trajectory.
        new_points (list): 
            List of new points representing the RepresentativeTrajectory.
        data_desc (DataDescriptor): 
            Descriptor providing metadata about the trajectory.
        """
        Trajectory.__init__(self, tid, label, new_points, data_desc)


# ------------------------------------------------------------------------------------------------------------
class RepresentativePoint(Point):
    """
    Represents a point within a representative trajectory, optionally linked to a cell and multiple points.

    Inherits from:
        - Point: Represents a single point in the trajectory described by multiple aspects.

    Attributes:
    -----------
    cell (RepresentativeCell, optional): 
        The cell associated with this point.
    points (list, optional): 
        List of points that this representative point represents.
    """
    def __init__(self, seq, aspects, cell=None, points=None):
        """
        Initializes a RepresentativePoint object.

        Args:
        -----
        seq (int): 
            The index sequence position of the point within the trajectory.
        aspects (list): 
            List of aspects describing the point (e.g., spatial, temporal, etc.).
        cell (RepresentativeCell, optional): 
            The representative cell that contains this point. Defaults to None.
        points (list, optional): 
            List of points this representative point represents. Defaults to None.
        """
        Point.__init__(self, seq, aspects)
        
        self.cell = cell
        self.points = points
        
        
class RepresentativeCell:
    """
    Represents a cell that contains multiple points, possibly grouped into representative points.

    Attributes:
    -----------
    points (list, optional): 
        List of points that belong to this cell.
    """
    def __init__(self, points=None):
        self.points = points