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
# ------------------------------------------------------------------------------------------------------------
# BASE for MultipleAspectSequence
# ------------------------------------------------------------------------------------------------------------
from matmodel.base.Aspect import instantiateAspect
from matmodel.descriptor import DataDescriptor

ARROW = ['➜', '↴', '→', '↝', '⇒', '⇢', '⇾', '➡', '⇨', '⇛']

class MultipleAspectSequence:
    """
    Represents a sequence of points with multiple aspects.

    This class is designed to handle sequences of points, where each point may have multiple attributes or aspects associated with it. 
    It provides functionalities to manipulate and analyze these sequences, including the addition of points and extraction of subsequences.

    Parameters
    ----------
    seq_id : int or str
        The identifier for the sequence (or TID - Trajectory ID).
    new_points : list, optional
        A list of new points to initialize the sequence with. Default is None.
    data_desc : DataDescriptor, optional
        An instance of DataDescriptor that describes the attributes of the points in the sequence. Default is None.

    Attributes
    ----------
    tid : int or str
        The sequence identifier.
    points : list
        A list of Point instances representing the points in the sequence.
    data_desc : DataDescriptor
        The DataDescriptor instance associated with the sequence.
    size : int
        The number of points in the sequence.

    Methods
    -------
    readSequence(new_points, data_desc):
        Reads a list of new points and populates the sequence.
    addPoint(aspects, data_desc):
        Adds a new point with specified aspects to the sequence.
    subsequence(start, size=1, attributes_index=None):
        Returns a MultipleAspectSequence subsequence of points from the sequence.
    valuesOf(attributes_index, start=0, size=1):
        Returns the values of the specified attributes from the subsequence.
    pointValue(idx, attribute_name):
        Retrieves the value of a specific attribute from a given point in the sequence.
    """
    def __init__(self, seq_id, new_points=None, data_desc=None):
        self.tid          = seq_id
        
        self.points       = []
        self.data_desc = None
        
        if new_points != None and data_desc != None:
            assert isinstance(new_points, list)
            assert isinstance(data_desc, DataDescriptor)
            
            self.data_desc   = data_desc
            self.readSequence(new_points, data_desc)
                
    def __repr__(self):
        return ARROW[0].join(map(lambda p: str(p), self.points))
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, other):
        if isinstance(other, MultipleAspectSequence):
            return self.__hash__() == other.__hash__()
#        if isinstance(other, Subtrajectory):
#            return self.__hash__() == other.__hash__()
        else:
            return False
        
    @property
    def l(self):
        return len(self.attributes)
    @property
    def attributes(self):
        return self.data_desc.attributes
    
    @property
    def attribute_names(self):
        return list(map(lambda attr: attr.text, self.attributes))
    
    @property
    def size(self):
        return len(self.points)
    
    def readSequence(self, new_points, data_desc):
        assert isinstance(new_points, list)
        assert isinstance(data_desc, DataDescriptor)
        
        if new_points is not None:
            self.points = list(map(lambda seq: 
                                   Point.fromRecord(
                                       seq+self.start if isinstance(self, Subtrajectory) else seq, 
                                   new_points[seq], data_desc), 
                          range(len(new_points))))
    
    def addPoint(self, aspects, data_desc):
        assert isinstance(aspects, tuple)
        self.points.append(Point(self.size, aspects, data_desc))
#        self.size += 1
        
    def subsequence(self, start, size=1, attributes_index=None):
        if attributes_index == None:
            return self.points[start : start+size]
        else:
            return list(map(lambda p: 
                            Point(p.seq, list(map(p.aspects.__getitem__, attributes_index))), 
                            self.points[start : start+size]
                        ))
    
    def valuesOf(self, attributes_index, start=0, size=1):
        return list(map(lambda p: p.valuesOf(attributes_index), self.subsequence(start, size)))
    
    def pointValue(self, idx, attribute_name):
        return self.points[idx].aspects[self.attribute_names.index(attribute_name)]
    
#    def attrByName(self, attribute_name):
#        return self.attributes.find(lambda x: x.text == attribute_name)
#        
#    def asString(self, attributes_index):
#        return ARROW[0].join(map(lambda p: p.asString(attributes_index), self.points))

# ------------------------------------------------------------------------------------------------------------
class Point:
    """
    Represents a point in a multiple-aspect sequence.

    Each point is characterized by its index in the sequence and a set of aspects associated with it.

    Parameters
    ----------
    seq : int
        The index of the point in the sequence.
    aspects : list
        A list of Aspect (or derrived types) representing the attributes or aspects of the point.

    Attributes
    ----------
    seq : int
        The index of the point.
    aspects : tuple
        The aspects associated with the point.

    Methods
    -------
    valuesOf(attributes_index):
        Retrieves the values of specified attributes from the aspects.
    asString(attributes_index):
        Returns a string representation of the point's aspects.
    """
    def __init__(self, seq, aspects):
        self.seq   = seq
        
        self.aspects = aspects
    
    def __repr__(self):
        return self.p+'⟨'+', '.join(map(str,self.aspects))+'⟩'
    
    def valuesOf(self, attributes_index):
        return tuple(map(self.aspects.__getitem__, attributes_index))
    
    def asString(self, attributes_index):
        return self.p+'⟨'+', '.join(map(str,self.valuesOf(attributes_index)))+'⟩'
        
    @property
    def l(self):
        return len(self.aspects)
    
    @property
    def p(self):
        return '𝘱'+str(self.seq+1)
    
    @staticmethod
    def fromRecord(seq, record, data_desc):
        assert isinstance(record, tuple)
        assert isinstance(data_desc, DataDescriptor) 
        
        aspects = list(map(lambda a, v: instantiateAspect(a, v), data_desc.attributes, record))
        return Point(seq, aspects)

# ------------------------------------------------------------------------------------------------------------
# TRAJECTORY 
# ------------------------------------------------------------------------------------------------------------
class Trajectory(MultipleAspectSequence):
    """
    Represents a trajectory composed of multiple points.

    A trajectory is a special type of MultipleAspectSequence that includes a label 
    for identification purposes.

    Parameters
    ----------
    tid : int or str
        The identifier for the trajectory (ID).
    label : str
        A label associated with the trajectory.
    new_points : list
        A list of initial points for the trajectory.
    data_desc : DataDescriptor
        An instance describing the attributes of the points in the trajectory.

    Attributes
    ----------
    T : str
        A formatted string representation of the trajectory identifier.
    label : str
        The label of the trajectory.

    Methods
    -------
    display():
        Prints a detailed representation of the trajectory.
    subtrajectory(start, size=1, attributes_index=None):
        Returns a Subtrajectory object representing a subsequence of the trajectory.
    """
    def __init__(self, tid, label, new_points, data_desc):
        MultipleAspectSequence.__init__(self, tid, new_points, data_desc)
        self.label = label
           
    @property
    def T(self):
        return '𝘛𐄁{}'.format(self.tid)
    
    def __repr__(self):
        return self.T+' '+MultipleAspectSequence.__repr__(self)
    
    def display(self):
        print( self.T+' '+ (ARROW[1]+'\n').join(map(lambda p: '\t'+str(p), self.points)) )
    
    def subtrajectory(self, start, size=1, attributes_index=None):
        return Subtrajectory(self, start, self.subsequence(start, size, attributes_index), attributes_index)
    
# ------------------------------------------------------------------------------------------------------------
# SUBTRAJECTORY
# ------------------------------------------------------------------------------------------------------------
class Subtrajectory(MultipleAspectSequence):
    """
    Represents a subsequence of a trajectory.

    A Subtrajectory is derived from a Trajectory and contains a subset of points 
    along with information about the attributes being analyzed.

    Parameters
    ----------
    trajectory : Trajectory
        The original trajectory from which this subsequence is derived.
    start : int
        The starting index of the point of the subsequence in the original trajectory.
    points : list
        A list of points that constitute the subsequence.
    attributes_index : list
        The indices of attributes being analyzed in this subsequence.

    Attributes
    ----------
    attributes_index : list
        The indices of attributes that belong to the analysis.
    s : str
        A formatted string representation of the subsequence.

    Methods
    -------
    attribute(index):
        Retrieves an attribute by its index.
    values():
        Returns the values of the specified attributes from the subsequence.
    """
    def __init__(self, trajectory, start, points, attributes_index):
        MultipleAspectSequence.__init__(self, trajectory.tid)
        self.sid     = 0 # TODO generate unique sid
        self.start   = start
#        self.size   = size
        self.trajectory   = trajectory
        self.points       = points # list contains instances of Point class
        self._attributes   = attributes_index # Just the index of attributes (from points) that belong to the analysis
        
    @property
    def attributes_index(self):
        return self._attributes
    
    @property
    def s(self):
        return '𝓈⟨{},{}⟩'.format(self.start, (self.start+self.size-1))
    @property
    def S(self):
        return '𝓈⟨{},{}⟩'.format(self.start, (self.start+self.size-1))+'{'+','.join(map(lambda x: str(x), self._attributes))+'}'
    
    def __repr__(self):
        return self.S+'𐄁'+self.trajectory.T+' '+MultipleAspectSequence.__repr__(self)
        
    def attribute(self, index):
        return self.trajectory.attributes[index]

    @property
    def attributes(self):
        return list(map(lambda index: self.trajectory.attributes[index], self._attributes))
    
    def values(self):
        return super().valuesOf(self._attributes)
    
    def valuesOf(self, attributes_index):
        return super().valuesOf(attributes_index)