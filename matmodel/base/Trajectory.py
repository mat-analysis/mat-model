from matmodel.base.MultipleAspectSequence import MultipleAspectSequence
from matmodel.base.Subtrajectory import Subtrajectory
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