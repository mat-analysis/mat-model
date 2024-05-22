# ------------------------------------------------------------------------------------------------------------
# BASE for MultipleAspectSequence
# ------------------------------------------------------------------------------------------------------------
from matmodel.base.Aspect import instantiateAspect
from matmodel.descriptor import DataDescriptor

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
            self.points = list(map(lambda seq: 
                                   Point.fromRecord(
                                       seq+self.start if isinstance(self, Subtrajectory) else seq, 
                                   new_points[seq], attributes_desc), 
                          range(len(new_points))))
    
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

# ------------------------------------------------------------------------------------------------------------
# TRAJECTORY 
# ------------------------------------------------------------------------------------------------------------
class Trajectory(MultipleAspectSequence):
    def __init__(self, tid, label, new_points, attributes_desc):
        MultipleAspectSequence.__init__(self, tid, new_points, attributes_desc)
        self.label = label
           
    @property
    def T(self):
        return '𝘛𐄁{}'.format(self.tid)
    
    def __repr__(self):
        return self.T+' '+MultipleAspectSequence.__repr__(self)
    
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
    
#    def asString(self):
#        return self.__repr__()+':'+super().asString(self._attributes)
#    
#    def attributes(self):
#        return self.data[0].keys()
#    
#    def add_point(self, point):
#        assert isinstance(point, dict)
#        self.data.append(self.point_dict(point))
#        
#    def point_dict(self, point):
#        assert isinstance(point, dict)
#        points = {}    
#        
#        def getKV(k,v):
#            px = {}
#            if isinstance(v, dict):
#                if k == 'lat_lon' or k == 'space':
#                    px['lat'] = v['x']
#                    px['lon'] = v['y']
#                else:
#                    px[k] = v['value']
#            else:
#                if k == 'lat_lon' or k == 'space':
#                    v = v.split(' ')
#                    px['lat'] = v[0]
#                    px['lon'] = v[1]
#                elif k == 'space3d':
#                    v = v.split(' ')
#                    px['x'] = v[0]
#                    px['y'] = v[1]
#                    px['z'] = v[2]
#                else:
#                    px[k] = v
#            return px
#        
#        list(map(lambda x: points.update(getKV(x[0], x[1])), point.items()))
#                
#        return points
#        
#    def toString(self):
#        return str(self)   
#    
#    def diffToString(self, mov2):
#        dd = self.diffPairs(mov2)
#        return ' >> '.join(list(map(lambda x: str(x), dd)))
#        
#    def toText(self):
#        return ' >> '.join(list(map(lambda y: "\n".join(list(map(lambda x: "{}: {}".format(x[0], x[1]), x.items()))), self.data)))
#    
#    def commonPairs(self, mov2):
#        common_pairs = set()
#        
#        for dictionary1 in self.data:
#            for dictionary2 in mov2.data:
#                for key in dictionary1:
#                    if (key in dictionary2 and dictionary1[key] == dictionary2[key]):
#                        common_pairs.add( (key, dictionary1[key]) )
#                        
#        return common_pairs
#      
#    def diffPairs(self, mov2):
#        diff_pairs = [dict() for x in range(self.size)]
#        
#        for x in range(self.size):
#            dictionary1 = self.data[x]
#            for dictionary2 in mov2.data:
#                for key in dictionary1:
#                    if (key not in dictionary2):
#                        diff_pairs[x][key] = dictionary1[key]
#                    elif (key in dictionary2 and dictionary1[key] != dictionary2[key]):
#                        diff_pairs[x][key] = dictionary1[key]
#                    elif (key in dictionary2 and key in diff_pairs[x] and dictionary1[key] == dictionary2[key]):
#                        del diff_pairs[x][key]
#                        
#        return diff_pairs