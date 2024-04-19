# ------------------------------------------------------------------------------------------------------------
# SUBTRAJECTORIES 
# ------------------------------------------------------------------------------------------------------------
from matmodel.base.MultipleAspectSequence import MultipleAspectSequence

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