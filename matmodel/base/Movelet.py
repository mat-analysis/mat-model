from matmodel.base import Subtrajectory
from matmodel.evaluation import Feature
from matmodel.base import MultipleAspectSequence
# ------------------------------------------------------------------------------------------------------------
# MOVELETS 
# ------------------------------------------------------------------------------------------------------------
class Movelet(Subtrajectory, Feature):
    def __init__(self, trajectory, start, points, attributes_index, quality, mid=0, subset_attribute_desc=None):
        Subtrajectory.__init__(self, trajectory, start, points, attributes_index)
        Feature.__init__(self, quality=quality)
        
        self.sid = mid
        self._subset_attr_desc = subset_attribute_desc
        
    @property
    def mid(self):
        return self.sid
    
    def __repr__(self):
        return self.Miq+' '+MultipleAspectSequence.__repr__(self)
    
    @property
    def Mi(self):
        return '𝓜𐄁{}'.format(self.mid)
    @property
    def Miq(self):
        return '𝓜𐄁{}'.format(self.mid)+'❲{:3.2f}%❳'.format(self.quality.value*100)
    @property
    def m(self):
        return '𝓜⟮{},{}⟯'.format(self.start, (self.start+self.size-1))
    @property
    def M(self):
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
        return len(self._attributes)
    
    @staticmethod
    def fromSubtrajectory(s, quality):
        return Movelet(s.trajectory, s.start, s.size, s.points, s._attributes, quality)
    
#    def diffToString(self, mov2):
#        dd = self.diffPairs(mov2)
#        return ' >> '.join(list(map(lambda x: str(x), dd))) + ' ('+'{:3.2f}'.format(self.quality)+'%)' 
#        
#    def toText(self):
#        return ' >> '.join(list(map(lambda y: "\n".join(list(map(lambda x: "{}: {}".format(x[0], x[1]), x.items()))), self.data))) \
#                    + '\n('+'{:3.2f}'.format(self.quality)+'%)'