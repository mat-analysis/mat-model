# ------------------------------------------------------------------------------------------------------------
# BASE for MultipleAspectSequence
# ------------------------------------------------------------------------------------------------------------
from movelets.classes.Aspect import instantiateAspect
#from movelets.classes.Subtrajectory import Subtrajectory

class MultipleAspectSequence:
    def __init__(self, seq_id, new_points=None, attributes_desc=None):
        self.tid          = seq_id
        
        self.points       = []
        if new_points and attributes_desc:
            self.readSequence(new_points, attributes_desc)
                
    def __repr__(self):
        return '=>'.join(map(lambda p: str(p), self.points))
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
    def attributes(self):
        return self.attributes_desc['attributes']
    
    def readSequence(self, new_points, attributes_desc):
        assert isinstance(new_points, list)
        assert isinstance(attributes_desc, dict)
        
        self.attributes_desc   = attributes_desc
        self.size         = len(new_points)
        if new_points is not None:
            self.points = list(map(lambda seq, point: Point(seq, point, attributes_desc), range(self.size), new_points))
    
    def addPoint(self, aspects, attributes_desc):
        assert isinstance(aspects, tuple)
        self.points.append(Point(self.size, aspects, attributes_desc))
        self.size += 1
        
    def subsequence(self, start, size=1):
        return self.points[start : start+size]
    
    def size(self):
        return len(self.points)
    
    def valuesOf(self, attributes_index):
        return list(map(lambda p: p.valuesOf(attributes_index), self.points))
        
    def asString(self, attributes_index):
        return '=>'.join(map(lambda p: p.asString(attributes_index), self.points))
        #return ' >> '.join(list(map(lambda y: "\n".join(list(map(lambda x: "{}: {}".format(x[0], x[1]), y.items()))), self.points)))

# ------------------------------------------------------------------------------------------------------------
class Point:
    def __init__(self, seq, record, attributes_desc):
        self.seq   = seq
        
        assert isinstance(record, tuple)
        assert isinstance(attributes_desc, dict) 

        self.aspects =  list(map(lambda a, v: instantiateAspect(a, v), attributes_desc['attributes'], record))
    
    def __repr__(self):
        return 'p'+str(self.seq)+str(self.aspects)
    
    def valuesOf(self, attributes_index):
        return list(map(self.aspects.__getitem__, attributes_index))
    
    def asString(self, attributes_index):
        return 'p'+str(self.seq)+str(self.valuesOf(attributes_index))
        
    @property
    def l(self):
        return len(self.aspects)
    
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
