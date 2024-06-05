class Comparator:
    '''<Abstract> Calculates the distance.

    Properties:
    max_value=None  - Maximum possible value for distance, default: Comparator.MAX_VALUE = float('inf').
    '''
    
    MAX_VALUE = float('inf')
    
    def __init__(self, max_value=None):
        self.max_value = max_value
        self.min_value = 0
    
    def match(self, asp1, asp2, match_threshold=0):
        """
        Determine whether two aspects match in equality
        Override this method to change behavior, can use match_threshold to match based on a specified threshold.

        Parameters:
        -----------
        asp1 : Aspect
            The first aspect to be compared.
        asp2 : Aspect
            The second aspect to be compared.
        match_threshold : float, optional
            A threshold for matching criteria (default 0). 
            Currently, it is used to match based on 0 distance.

        Returns:
        --------
        bool
            True if the two aspects match, False otherwise.
        """
        return True if self.distance(asp1, asp2) <= match_threshold else False
    
    def distance(self, asp1, asp2):
        '''Calculates the distance.

        Arguments:
        asp1 (Aspect<?>) - value 1 to compare
        asp2 (Aspect<?>) - value 2 to compare
        
        Return:
        distance - distance equality value (0 for equal values, 1 for different).
        '''
        return 0 if asp1.__eq__(asp2) else 1
    
    def normalize(self, distance):
        if not self.max_value:
            return distance
        
        return (distance - self.min_value) / (self.max_value - self.min_value)
    
    def enhance(self, distance):
        distance = (distance * distance)
        if self.max_value and distance > self.max_value:
            return self.max_value
        else:
            return distance
    
    @staticmethod
    def instantiate(json_obj):
        # TODO: new distances and specific cases:
        max_value = json_obj['comparator']['maxValue'] if 'maxValue' in json_obj['comparator'].keys() else None
        if max_value == -1:
            max_value = None
        
        c = None
        if json_obj['comparator']['distance'] == 'difference' and  json_obj['type'] == 'time':
            units = json_obj['comparator']['units'] if 'units' in json_obj['comparator'].keys() else 'm'
            c = TimeDistance(max_value, units)
        
        elif json_obj['comparator']['distance'] == 'diffnotneg' or json_obj['comparator']['distance'] == 'difference':
            c = AbsoluteDistance(max_value)
        
        else:
            cname = eval( str(json_obj['comparator']['distance']).capitalize()+'Distance' )
            c = cname(max_value)
            
        # Other Params:
        min_value = json_obj['comparator']['minValue'] if 'minValue' in json_obj['comparator'].keys() else None
        if min_value == -1:
            c.min_value = min_value
            
        for k, v in json_obj['comparator'].items():
            if k not in ['distance', 'maxValue', 'minValue']:
                setattr(c, k, v)
        return c

class EqualsDistance(Comparator):
    def __init__(self, max_value=None):
        Comparator.__init__(self, max_value)
        
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
    def __init__(self, max_value=None):
        Comparator.__init__(self, max_value)
    
class NumericDistance(Comparator):
    def __init__(self, max_value=None):
        Comparator.__init__(self, max_value)

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
    def __init__(self, max_value=None):
        Comparator.__init__(self, max_value)

    def distance(self, asp1, asp2):
        '''Calculates the absolute distance.

        Arguments:
        asp1 (Aspect<numeric>) - value 1 to compare
        asp2 (Aspect<numeric>) - value 2 to compare
        
        Return:
        distance - distance difference value, abs(asp1 - asp2).
        '''
        return abs(asp1._value - asp2._value)

class TimeDistance(Comparator):    
    '''Calculates the closest time distance.
    Only works for time in hours, minutes, seconds, and microseconds. Ex.: difference between 22h and 2h is 3h.

    Properties:
    units='ms'      - Unit measure to get distance: h (hours), m (minutes), s (seconds), ms (microseconds)
    max_value=None  - Maximum possible value for distance (Ex.: hours = 24)
    '''
    
    def __init__(self, max_value=None, units='m'): 
        # Works for time in hours, minutes or seconds. Ex.: difference between 22h and 2h is 3h.
        self.units = units
        if units == 'h':
            max_value = 23
        elif units == 'm':
            max_value = 24*60-1
        elif units == 's':
            max_value = 24*60*60-1
        elif units == 'ms':
            max_value = 24*60*60*1000-1
        
        Comparator.__init__(self, max_value)
        
    
    def distance(self, asp1, asp2):
        '''Calculates the closest time distance.
        
        Arguments:
        asp1 (Aspect<numeric>, DateTime Aspect) - value 1 to compare
        asp2 (Aspect<numeric>, DateTime Aspect) - value 2 to compare
        
        Return:
        distance - distance difference in the informed units.
        '''
        
        v1 = asp1.get(self.units)
        v2 = asp2.get(self.units)
        
        v1, v2 = max(v1, v2), min(v1, v2)
        
        return min( ((self.max_value - v1) + v2 +1), (v1 - v2) )
    
    def abs_distance(self, asp1, asp2):
        '''Calculates the simple time distance.
        
        Arguments:
        asp1 (Aspect<numeric>, DateTime Aspect) - value 1 to compare
        asp2 (Aspect<numeric>, DateTime Aspect) - value 2 to compare
        
        Return:
        distance - distance difference in the informed units.
        '''
        
        v1 = asp1.get(self.units)
        v2 = asp2.get(self.units)
        
        return abs(v1 - v2)

class DatetimeDistance(Comparator): 
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
    
    def __init__(self, max_value=None, units=None):
        Comparator.__init__(self, max_value)
        self.units = units
    
    def distance(self, asp1, asp2):
        dt1 = max(asp1._value, asp2._value)
        dt2 = min(asp1._value, asp2._value)
#        delta = abs(asp1._value - asp2._value)
        if self.units == None or self.units == 's':
            return (dt1 - dt2).total_seconds()
        if self.units == 'D':
            return (dt1 - dt2).days
        elif self.units == 'M': # This is a workaround datetime.timedelta:
            from dateutil.relativedelta import relativedelta
            delta = relativedelta(dt1, dt2)
            return delta.years*12 + delta.months
        elif self.units == 'Y':
            return dt1.year - dt2.year
        elif self.units == 'w':
            return (dt1 - dt2).days // 7
        elif self.units == 'h':
            return (dt1 - dt2).total_seconds() // 3600
        elif self.units == 'm':
            return (dt1 - dt2).total_seconds() // 60
        elif self.units == 'weekday':
            return dt1.weekday() - dt2.weekday()
        elif self.units == '=weekday':
            return dt1.weekday() == dt2.weekday()
        elif self.units == 'isweekday':
            return 0 if dt1.isweekday() == dt2.isweekday() else 1
        else:               
            return (dt1 - dt2).total_seconds()
    
class InintervalDistance(DatetimeDistance): # TimeDistance.distance calculate difference in minutes (if units == 'm')        
    def __init__(self, max_value=None, units='m'):
        DatetimeDistance.__init__(self, max_value, units)  
        
    def distance(self, asp1, asp2):
        from matmodel.base import Interval
        
        # in case one aspect is an Interval return 0 if match, else return 1
        if isinstance(asp1, Interval) or isinstance(asp2, Interval):
            return 0 if self.match(asp1, asp2) else 1
        else:
            return super().distance(asp1, asp2) # Gets the time difference
    
    def match(self, asp1, asp2, match_threshold=0): #Check if the dates or intervals match (can use with 'DateTime' or 'Interval' instances, or mixed)
        from matmodel.base import DateTime, Interval
        
        if not (isinstance(asp1, DateTime) and isinstance(asp2, DateTime)):
            raise TypeError("Aspects must be 'DateTime' or 'Interval' instances.")

        # For 2 intervals:
        if isinstance(asp1, Interval) and isinstance(asp2, Interval):
            return self.converge(asp1, asp2)
        
        # For 1 date and 1 interval:
        # If asp1 or asp2 represents a point in time (just DateTime.start),
        elif isinstance(asp1, Interval) or isinstance(asp2, Interval):
            return self.match_date_interval(asp1, asp2)

        # If both asp1 and asp2 represents a point in time, we use the distance to see a match:
        # (match_th is a threshold for matching, default 0)
        else:
            return self.match_dates(asp1, asp2, match_threshold)
    
    def match_dates(self, asp1, asp2, match_threshold=0):
        return False if int(self.distance(asp1, asp2)) > match_threshold else True
        
    def match_date_interval(self, asp1, asp2):
        from matmodel.base import Interval
        
        if isinstance(asp2, Interval): #  asp1 is the DateTime, asp2 is the Interval
            D = asp1
            I = asp2
        else:
            D = asp2
            I = asp1
            
        return True if D.start >= I.start and D.start <= I.end else False
    
    def converge(self, asp1, asp2):
        if not (isinstance(asp1, Interval) and isinstance(asp2, Interval)):
            raise TypeError("Aspects must be 'Interval' instances.")

        if max(asp1.start, asp2.start) <= min(asp1.end, asp2.end):
            return True
        else:
            return False
    
class EuclideanDistance(Comparator):
    def __init__(self, max_value=None):
        Comparator.__init__(self, max_value)

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
    def __init__(self, max_value=None):
        Comparator.__init__(self, max_value)

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
    def __init__(self, max_value=None):
        Comparator.__init__(self, max_value)
    
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
    
    def lcs_distance(self, X, Y):
        return max(len(X),len(Y)) - self.lcs(X, Y) 

    def distance(self, asp1, asp2):
        '''Calculates the Longest Common Subsequence difference.
        
        Arguments:
        asp1 (Aspect<nominal>) - value 1 to compare
        asp2 (Aspect<nominal>) - value 2 to compare
        
        Return:
        distance - LCS distance value.
        '''
        return self.lcs_distance(asp1._value, asp2._value)
    
class EditlcsDistance(LcsDistance):
    def __init__(self, max_value=None):
        Comparator.__init__(self, max_value)

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