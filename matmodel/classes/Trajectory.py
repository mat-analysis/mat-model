from movelets.classes.MultipleAspectSequence import MultipleAspectSequence
# ------------------------------------------------------------------------------------------------------------
# TRAJECTORY 
# ------------------------------------------------------------------------------------------------------------
class Trajectory(MultipleAspectSequence):
    def __init__(self, tid, label, new_points, attributes_desc):
        MultipleAspectSequence.__init__(self, tid, new_points, attributes_desc)
        self.label = label
        
#    def __repr__(self):
#        return '=>'.join( list(map(lambda x: str(x), self.points)
#
#    def toText(self):
#        return ' >> '.join(list(map(lambda y: "\n".join(list(map(lambda x: "{}: {}".format(x[0], x[1]), y.items()))), self.points)))