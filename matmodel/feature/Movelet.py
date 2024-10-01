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
from matmodel.base import Subtrajectory
from matmodel.base import MultipleAspectSequence

from matmodel.feature.Feature import Feature
# ------------------------------------------------------------------------------------------------------------
# MOVELETS 
# ------------------------------------------------------------------------------------------------------------
class Movelet(Subtrajectory, Feature):
    """
    Represents a movelet, inherits from Subtrajectory and Feature.

    Inherits from:
        - Subtrajectory: Represents a part of a trajectory with specific attributes.
        - Feature: Represents a feature that can be associated with a quality.

    Attributes:
    -----------
    sid (int): 
        The ID of the movelet.
    _subset_attr_desc (list): 
        Subset of attribute descriptors.
    splitpoints (list of floats): 
        Vector of distance values where the dataset might be split for this subset of attributes.
    distances (list of floats): 
        Stores the distances for the movelet to all other trajectories.
    """
    def __init__(self, trajectory, start, points, attributes_index, quality, mid=0, subset_attribute_desc=None):
        """
        Initializes a Movelet object.

        Args:
        -----
        trajectory (Trajectory or subclasses): 
            The trajectory this movelet belongs to.
        start (int): 
            The starting index point of the subtrajectory.
        points (int): 
            The points in the movelet.
        attributes_index (list): 
            The list of attribute indices used in the movelet.
        quality (Quality): 
            The quality associated with this movelet.
        mid (int, optional): 
            Movelet ID. Defaults to 0.
        subset_attribute_desc (any, optional): 
            Subset of attribute descriptions. Defaults to None.
        """
        
        Subtrajectory.__init__(self, trajectory, start, points, attributes_index)
        Feature.__init__(self, quality=quality)
        
        self.sid = mid
        self._subset_attr_desc = subset_attribute_desc
        
        self.splitpoints = None
        self.distances = None
        
    @property
    def mid(self):
        return self.sid
    
    def __repr__(self):
        """
        Provides a string representation of the movelet.

        Returns:
            str: Representation of the movelet with its quality and trajectory details.
        """
        return self.Miq+' '+MultipleAspectSequence.__repr__(self)
    
    @property
    def Mi(self):
        """
        Returns the movelet's identifier formatted with special characters.
        """
        return '𝓜𐄁{}'.format(self.mid)
    @property
    def Miq(self):
        """
        Returns the movelet's identifier along with its quality percentage.
        """
        return '𝓜𐄁{}'.format(self.mid)+'❲{:3.2f}%❳'.format(self.quality.value*100)
    @property
    def m(self):
        """
        Returns the movelet's range formatted as a string (start and end).
        """
        return '𝓜⟮{},{}⟯'.format(self.start, (self.start+self.size-1))
    @property
    def M(self):
        """
        Returns the movelet's range (start and end) along with its quality percentage formatted as a string.
        """
        return '𝓜⟮{},{}⟯'.format(self.start, (self.start+self.size-1))+'{'+','.join(map(lambda x: str(x), self._attributes))+'}'
    
    @property
    def attributes(self):
        if self.trajectory.data_desc:
            return Subtrajectory.super(self).attributes #list(map(lambda index: self.trajectory.attributes[index], self._attributes))
        else:
            return self._subset_attr_desc
        
    @property
    def subset_attr_desc(self):
        return self._subset_attr_desc

    @subset_attr_desc.setter
    def subset_attr_desc(self, value):
        self._subset_attr_desc = value
    
    @property
    def l(self):
        """
        Returns the number of attributes in the movelet.
        """
        return len(self._attributes)
    
    @staticmethod
    def fromSubtrajectory(s, quality):
        """
        <Static>
        Creates a Movelet from an existing subtrajectory and quality.

        Args:
        -----
        s (Subtrajectory): 
            The subtrajectory object.
        quality (Quality): 
            The quality associated with the movelet.

        Returns:
        --------
            Movelet: A new Movelet object.
        """
        return Movelet(s.trajectory, s.start, s.size, s.points, s._attributes, quality)
    
#    def diffToString(self, mov2):
#        dd = self.diffPairs(mov2)
#        return ' >> '.join(list(map(lambda x: str(x), dd))) + ' ('+'{:3.2f}'.format(self.quality)+'%)' 
#        
#    def toText(self):
#        return ' >> '.join(list(map(lambda y: "\n".join(list(map(lambda x: "{}: {}".format(x[0], x[1]), x.items()))), self.data))) \
#                    + '\n('+'{:3.2f}'.format(self.quality)+'%)'