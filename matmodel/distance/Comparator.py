class Comparator:
    '''<Abstract> Calculates the distance.

    Properties:
    max_value=None  - Maximum possible value for distance, default: Comparator.MAX_VALUE = float('inf').
    '''
    
    MAX_VALUE = float('inf')
    
    def __init__(self):
        self.max_value = Comparator.MAX_VALUE
    
    def distance(self, asp1, asp2):
        '''Calculates the distance.

        Arguments:
        asp1 (Aspect<?>) - value 1 to compare
        asp2 (Aspect<?>) - value 2 to compare
        
        Return:
        distance - distance equality value (0 for equal values, 1 for different).
        '''
        return 0 if asp1.__eq__(asp2) else 1
    def match(self, asp1, asp2):
        return True
    def normalize(self, distance):
        if self.max_value == -1:
            return distance
        if distance >= self.max_value:
            return self.max_value
        return distance / self.max_value
    def enhance(self, distance):
        distance = (distance * distance)
        return distance if distance < self.max_value else self.max_value
    
    @staticmethod
    def instantiate(json_obj):
        return None # TODO
    
class EqualsDistance(Comparator):
    def __init__(self):
        self.max_value = 1
        
    def distance(self, asp1, asp2):
        '''Calculates the distance for eqality ignoring case.

        Arguments:
        asp1 (Aspect<nominal>) - value 1 to compare
        asp2 (Aspect<nominal>) - value 2 to compare
        
        Return:
        distance - distance equality value (0 for equal values, 1 for different).
        '''
        return 0 if asp1._value.upper() == asp2._value.upper() else 1

class CaselessDistance(Comparator):
    def __init__(self):
        self.max_value = 1
    
class NumericDistance(Comparator):
    def __init__(self):
        pass

    def distance(self, asp1, asp2):
        '''Calculates the numeric distance.

        Arguments:
        asp1 (Aspect<numeric>) - value 1 to compare
        asp2 (Aspect<numeric>) - value 2 to compare
        
        Return:
        distance - distance difference value (asp1 - asp2).
        '''
        return asp1._value - asp2._value
    
class AbsoluteDistance(NumericDistance):
    def __init__(self):
        pass

    def distance(self, asp1, asp2):
        '''Calculates the absolute distance.

        Arguments:
        asp1 (Aspect<numeric>) - value 1 to compare
        asp2 (Aspect<numeric>) - value 2 to compare
        
        Return:
        distance - distance difference value, abs(asp1 - asp2).
        '''
        return abs(asp1._value - asp2._value)
      
class DateDistance(Comparator): 
    '''Calculates the date distance in one of the following units:
    D - days
    M - months
    Y - years
    w - weeks
    h - hours
    m - minutes
    s - seconds (default), which includes microseconds fraction
    
    'weekday'   - difference in weekdays
    '=weekday'  - equal weekday (0 for equal values, 1 for different)
    'isweekday' - equal if both are weekdays or both are weekends (0 for equal values, 1 for different)

    Properties:
    units='ms'      - Unit measure to get distance.
    max_value=None  - Maximum possible value for distance, default: Comparator.MAX_VALUE = float('inf')
    '''
    def __init__(self, units=None, max_value=None):
        self.units = units
        if max_value:
            self.max_value = max_value
    
    def distance(self, asp1, asp2):
        dt1 = max(asp1._value - asp2._value)
        dt2 = min(asp1._value - asp2._value)
#        delta = abs(asp1._value - asp2._value)
        if self.units == None or self.units == 's':
            return (dt1 - dt2).total_seconds()
        if units == 'D':
            return (dt1 - dt2).days
        elif units == 'M': # This is a workaround datetime.timedelta:
            from dateutil.relativedelta import relativedelta
            delta = relativedelta(dt1, dt2)
            return delta.years*12 + delta.months
        elif units == 'Y':
            return dt1.year - dt2.year
        elif units == 'w':
            return (dt1 - dt2).days // 7
        elif units == 'h':
            return (dt1 - dt2).total_seconds() // 3600
        elif units == 'm':
            return (dt1 - dt2).total_seconds() // 60
        elif units == 'weekday':
            return dt1.weekday() - dt2.weekday()
        elif units == '=weekday':
            return dt1.weekday() == dt2.weekday()
        elif units == 'isweekday':
            return 0 if dt1.isweekday() == dt2.isweekday() else 1
        else:               
            return (dt1 - dt2).total_seconds()

class TimeDistance(Comparator):    
    '''Calculates the closest time distance.
    Only works for time in hours, minutes, seconds, and microseconds. Ex.: difference between 22h and 2h is 3h.

    Properties:
    units='ms'      - Unit measure to get distance: h (hours), m (minutes), s (seconds), ms (microseconds)
    max_value=None  - Maximum possible value for distance (Ex.: hours = 24)
    '''
    def __init__(self, units='ms', max_value=None): 
        # Works for time in hours, minutes or seconds. Ex.: difference between 22h and 2h is 3h.
        self.units = units
        if max_value:
            self.max_value = max_value
        elif units == 'h':
            self.max_value = 23
        elif units == 'm':
            self.max_value = 24*60-1
        elif units == 's':
            self.max_value = 24*60*60-1
        elif units == 'ms':
            self.max_value = 24*60*60*1000-1
    
    def distance(self, asp1, asp2):
        '''Calculates the closest time distance.
        
        Arguments:
        asp1 (Aspect<numeric>, DateTimeAspect) - value 1 to compare
        asp2 (Aspect<numeric>, DateTimeAspect) - value 2 to compare
        
        Return:
        distance - distance difference in the informed units.
        '''
        v1 = asp1.value(self.units)
        v2 = asp2.value(self.units)
        v1 = max(v1, v2)
        v2 = min(v1, v2)
        return min( ((self.max_value - v1) + v2 +1), (v1 - v2) )
    
class EuclideanDistance(Comparator):
    def __init__(self):
        pass

    def distance(self, asp1, asp2):
        '''Calculates the Euclidean distance (works for points of 2D, 3D, and more).
        
        Arguments:
        asp1 (Space2D, Space3D) - value 1 to compare
        asp2 (Space2D, Space3D) - value 2 to compare
        
        Return:
        distance - distance value.
        '''
        import math
        return math.sqrt( sum(map(lambda v1, v2: abs(v1 - v2)**2, asp1.value, asp2.value)) )
        
#        from movelets.classes.Aspect import Space2D, Space3D
#        assert isinstance(asp1, Space2D) and isinstance(asp2, Space2D), 'Expected Space2D or Space3D for EuclideanDistance calculation.'
#        
#        import math
#        diffX = abs(asp1.x - asp2.x)
#        diffY = abs(asp1.y - asp2.y)
#        
#        if isinstance(asp1, Space3D):
#            diffZ = abs(asp1.z - asp2.z)
#            return math.sqrt( diffX * diffX + diffY * diffY + diffZ * diffZ )
#        else:
#            return math.sqrt( diffX * diffX + diffY * diffY )
    
class ManhattanDistance(Comparator):
    def __init__(self):
        pass

    def distance(self, asp1, asp2):
        '''Calculates the Manhattan distance (works for points of 2D, 3D, and more).
        
        Arguments:
        asp1 (Space2D, Space3D) - value 1 to compare
        asp2 (Space2D, Space3D) - value 2 to compare
        
        Return:
        distance - distance value.
        '''
        return sum(map(lambda v1, v2: abs(v1 - v2), asp1.value, asp2.value))
    
class LcsDistance(Comparator):
    def __init__(self):
        pass
    
    def lcs(self, X, Y):
        m = len(X)
        n = len(Y)

        L = list(map(lambda i: [None]*(n + 1), range(m + 1)))

        def sublcs(i, j):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

            return L[i][j]

        list(map(lambda i: list(map(lambda j: sublcs(i, j), range(n + 1))), range(m + 1)))            

        return L[m][n]

    def distance(self, asp1, asp2):
        '''Calculates the Longest Common Subsequence difference.
        
        Arguments:
        asp1 (Aspect<nominal>) - value 1 to compare
        asp2 (Aspect<nominal>) - value 2 to compare
        
        Return:
        distance - LCS distance value.
        '''
        return self.lcs(asp1._value, asp2._value)
    
class EditlcsDistance(LcsDistance):
    def __init__(self):
        pass

    def distance(self, asp1, asp2):
        '''Calculates the Longest Common Subsequence difference.
        
        Arguments:
        asp1 (Aspect<nominal>) - value 1 to compare
        asp2 (Aspect<nominal>) - value 2 to compare
        
        Return:
        distance - LCS distance value.
        '''
        lcs = self.lcs(asp1._value, asp2._value)
        return ((len(asp1._value) - lcs) + (len(asp2._value) - lcs))