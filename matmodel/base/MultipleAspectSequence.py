# ------------------------------------------------------------------------------------------------------------
# BASE for MultipleAspectSequence
# ------------------------------------------------------------------------------------------------------------
from matmodel.base.Aspect import instantiateAspect
from matmodel.descriptor import DataDescriptor

ARROW = ['➜', '↴', '→', '↝', '⇒', '⇢', '⇾', '➡', '⇨', '⇛']

class MultipleAspectSequence:
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
        self.size += 1
        
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