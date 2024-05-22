from matmodel.method.MethodWrapper import MethodWrapper

class MasterMovelets(MethodWrapper):
    
    PROVIDE = {
        'MM':   'MASTERMovelets',
        'MM+Log':  'MASTERMovelets-Log',
        'MMp':  'MASTERPivots',
        'MMp+Log': 'MASTERPivots-Log',
        'MML':  'MASTERMovelets-Log',
        'MMpL': 'MASTERPivots-Log',
    }
    
    NAMES = {
        'MM':   'MM',
        'MM+Log':  'MM-Log',
        'MML':  'MM-Log',
        'MMp':  'MP',
        'MMp+Log': 'MP-Log',
        'MMpL': 'MP-Log',
    }
    
    def __init__(self):
        pass
    
