# ------------------------------------------------------------------------------------------------------------
# BASE for MultipleAspectSequence
# ------------------------------------------------------------------------------------------------------------
from matmodel.base import instantiateAspect
from matmodel.descriptor import DataDescriptor
#from movelets.classes.Subtrajectory import Subtrajectory

ARROW = ['➜', '→', '↝', '⇒', '⇢', '⇾', '➡', '⇨', '⇛']

class MultipleAspectSequence:
    def __init__(self, seq_id, new_points=None, attributes_desc=None):
        self.tid          = seq_id
        
        self.points       = []
        self.attributes_desc = None
        
        if new_points != None and attributes_desc != None:
            assert isinstance(new_points, list)
            assert isinstance(attributes_desc, DataDescriptor)
            
            self.attributes_desc   = attributes_desc
            self.readSequence(new_points, attributes_desc)
                
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
        return self.attributes_desc.attributes
    
    @property
    def attribute_names(self):
        return list(map(lambda attr: attr.text, self.attributes))
    
    @property
    def size(self):
        return len(self.points)
    
    def readSequence(self, new_points, attributes_desc):
        assert isinstance(new_points, list)
        assert isinstance(attributes_desc, DataDescriptor)
        
        if new_points is not None:
            self.points = list(map(lambda seq: Point.fromRecord(seq, new_points[seq], attributes_desc), range(len(new_points))))
    
    def addPoint(self, aspects, attributes_desc):
        assert isinstance(aspects, tuple)
        self.points.append(Point(self.size, aspects, attributes_desc))
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
        return '𝘱'+str(self.seq)+'⟨'+', '.join(map(str,self.aspects))+'⟩'
    
    def valuesOf(self, attributes_index):
        return tuple(map(self.aspects.__getitem__, attributes_index))
    
    def asString(self, attributes_index):
        return '𝘱'+str(self.seq)+'⟨'+', '.join(map(str,self.valuesOf(attributes_index)))+'⟩'
        
    @property
    def l(self):
        return len(self.aspects)
    
    @staticmethod
    def fromRecord(seq, record, attributes_desc):
        assert isinstance(record, tuple)
        assert isinstance(attributes_desc, DataDescriptor) 
        
        aspects = list(map(lambda a, v: instantiateAspect(a, v), attributes_desc.attributes, record))
        return Point(seq, aspects)
    
#    def transpose(self):
#        pts_trans = []
#        def transAux(attr):
#        #for attr in self.attributes:
#            col = {}
#            col['attr'] = attr
#            for i in range(self.size):
#                col['p'+str(i)] = self.points[i][attr]
#            return col
#
#        pts_trans = list(map(lambda attr: transAux(attr), self.attributes()))
#        return pts_trans
# ------------------------------------------------------------------------------------------------------------
