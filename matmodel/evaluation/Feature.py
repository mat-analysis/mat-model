from matmodel.base import Aspect

class Feature:
    def __init__(self, quality=None):
        self.quality = quality
        
#class IntervalFeature(Feature):
#    def __init__(self, quality=None):
#        Feature.__init__(self, quality)
#        
#class CellFeature(IntervalFeature):
#    def __init__(self, quality=None):
#        Feature.__init__(self, quality)
#        
#class AspectFeature(Feature):
#    def __init__(self, aspect, quality=None):
#        Feature.__init__(self, quality)
#        self.aspect = aspect
        
class DerrivedFeature(Feature, Aspect):
    def __init__(self, value, original_aspect, quality=None):
        Feature.__init__(self, quality)
        Aspect.__init__(self, value)
        self.aspect = aspect