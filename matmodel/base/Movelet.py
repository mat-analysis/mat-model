from movelets.classes.Subtrajectory import Subtrajectory
from movelets.classes.Feature import Feature
# ------------------------------------------------------------------------------------------------------------
# MOVELETS 
# ------------------------------------------------------------------------------------------------------------
class Movelet(Subtrajectory, Feature):
    def __init__(self, trajectory, start, size, points, attributes_index, quality):
        Subtrajectory.__init__(self, trajectory, start, size, points, attributes_index)
        Feature.__init__(self, quality=quality)
        
    def __repr__(self):
        return super().__repr__() + ' .Q'+'{:3.2f}'.format(self.quality.value*100)+'%' 
    
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