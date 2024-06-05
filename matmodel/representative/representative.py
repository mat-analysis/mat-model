from matmodel.base.MultipleAspectSequence import Trajectory, Point

class RepresentativeTrajectory(Trajectory):
    def __init__(self, tid, label, new_points, data_desc):
        Trajectory.__init__(self, tid, label, new_points, data_desc)


# ------------------------------------------------------------------------------------------------------------
class RepresentativePoint(Point):
    def __init__(self, seq, aspects, cell=None, points=None):
        Point.__init__(self, seq, aspects)
        
        self.cell = cell
        self.points = points
        
        
class RepresentativeCell:
    def __init__(self, points=None):
        self.points = points