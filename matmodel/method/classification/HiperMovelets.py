from matmodel.method.MethodWrapper import MethodWrapper, Param

class HiperMovelets(MethodWrapper):
    
    PROVIDE = {
        'hiper': 'HiPerMovelets', 
        'hiper-pivots': 'HiPerPivots', 
        'hiper+Log': 'HiPerMovelets-Log',
        'hiper-pivots+Log': 'HiPerPivots-Log',
    }
    
    NAMES = {
        'H': 'HiPerMovelets τ=90%', 
        'HL': 'HiPerMovelets τ=90%',
        'HTR75': 'HiPerMovelets τ=75%', 
        'HTR75L': 'HiPerMovelets τ=75%',
        'HTR50': 'HiPerMovelets τ=50%', 
        'HTR50L': 'HiPerMovelets τ=50%',

        'Hp': 'HiPerPivots τ=90%', 
        'HpL': 'HiPerPivots τ=90%',
        'HpTR75': 'HiPerPivots τ=75%', 
        'HpTR75L': 'HiPerPivots τ=75%',
        'HpTR50': 'HiPerPivots τ=50%', 
        'HpTR50L': 'HiPerPivots τ=50%',
    }
    
    def __init__(self):
        self.params = [
            Param('')
        ]
