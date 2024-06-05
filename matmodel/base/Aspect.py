import datetime

class Aspect():
    def __init__(self, value):
        self._value = value

    @property
    def value(self, units=None):
        return self._value

    def __repr__(self):
        return str(self.value)
    
    def match(self, asp1, asp2):
        return asp1.__eq__(asp2)
    
    def __eq__(self, other):
        return self._value == other._value
    
class Boolean(Aspect):
    def __init__(self, value): # TODO Other possible false and true values?
        if value in ['False', 'No', 'FALSE', 'false', 'N', '-', 'NO']:
            value = False
        elif value in ['True', 'Yes', 'TRUE', 'true', 'Y', 'YES', 'S']:
            value = True
        else:
            value = bool(value)
        Aspect.__init__(self, value)
    
class Numeric(Aspect):
    def __init__(self, value):
        value = float(value)
        Aspect.__init__(self, value)
    
class Categoric(Aspect):
    def __init__(self, value):
        Aspect.__init__(self, value)

class Space2D(Aspect):
    def __init__(self, value):
        x, y = value.split(' ')
        Aspect.__init__(self, str((x,y)))
        x, y = float(x), float(y)
        self.x = x
        self.y = y

    @Aspect.value.getter
    def value(self):
        return (self.x, self.y)
    
    def __repr__(self):
        return "({:.3f} {:.3f})".format(self.x, self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Space3D(Space2D):
    def __init__(self, x, y, z):        
        x, y, z = v.split(' ')
        Aspect.__init__(self, str((x,y,z)))
        
        x, y, z = float(x), float(y), float(z)
        self.x = x
        self.y = y
        self.z = z

    @Aspect.value.getter
    def value(self):
        return (self.x, self.y, self.z)
    
    def __repr__(self):
        return "({:.3f} {:.3f} {:.3f})".format(self.x, self.y, self.z)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

class DateTime(Aspect):
    def __init__(self, start, mask="%H:%M"): 
        # Convert to datetime:
        start = self.convert(start)
        Aspect.__init__(self, start)
        
        self.mask = mask
    
    @property
    def start(self):
        return self._value
    
    def day(self): #Just the day (1..30|31*)
        return self._value.day
    
    def month(self): #Just the month (1..12)
        return self._value.month
    
    def year(self): #Just the year
        return self._value.year
    
    def weekday(self): #Just the weekday (0..6)
        return self._value.weekday()
    
    def isweekend(self):
        return self._value.weekday() in [5, 6]
    
    def isweekday(self):
        return not self.isweekend()
    
    def hours(self): #Just the hours of the day
        return self._value.hour
    
    def minutes(self):
        return self._value.hour*60 + self._value.minute
    
    def seconds(self):
        return self.minutes()*60 + self._value.second
    
    def microseconds(self):
        return self.seconds()*1000000 + self._value.microsecond
    
    def get(self, units=None): # TODO for interval?
        if units == None:
            return self._value
        elif units == 'D':
            return self.day()
        elif units == 'M':
            return self.month()
        elif units == 'Y':
            return self.year()
        elif units == 'w':
            return self.weekday()
        elif units == 'h':
            return self.hours()
        elif units == 'm':
            return self.minutes()
        elif units == 's':
            return self.seconds()
        elif units == 'ms':
            return self.microseconds()
        else:
            raise Exception('[ERROR DateTime Aspect]: invalid \'units='+str(units)+'\' conversion.')
    
    def convertMinToDate(self, minutes):
        # reference date (can be any one)
        reference_date = datetime.datetime(2024, 1, 1)

        # Compute difference of time in minutes
        time_diff = datetime.timedelta(minutes=minutes)

        # Add diff to refence date
        result_date = reference_date + time_diff

        return result_date
    
    def convert(self, value, mask = None):
        return datetime.datetime.strptime(value, mask) if mask else self.convertMinToDate(int(value))
    
class Interval(DateTime):
    def __init__(self, start, end, mask="%H:%M"):
        DateTime.__init__(self, start, mask)
        # Convert to datetime
        end = self.convert(end)
        self.end = end
        
    def __repr__(self):
        return '[{} 𛲔𛲔 {}]'.format(self.start, self.end)

class Rank(Aspect):
    def __init__(self, descriptor):
        Aspect.__init__(self, descriptor)
        self.rank_values = [] # ->RankValue
        
    @property
    def descriptor(self):
        return self._value
    
    def add(self, aspect, proportion):
        self.rank_values.append(RankValue(aspect, proportion))
    
class RankValue:
    def __init__(self, value, proportion):
        self.value = value
        self.proportion = proportion

# ------------------------------------------------------------------------------------------------------------
def instantiateAspect(k,v):
    try:
        if k.dtype == 'nominal' or k.dtype == 'categorical':
            return Categoric( str(v) )
        elif k.dtype == 'numeric':
            return Numeric( v )
        elif k.dtype == 'datetime' or k.dtype == 'time':
            return DateTime( v )
        elif k.dtype == 'space2d':
            x, y = v.split(' ')
            return Space2D( v )
        elif k.dtype == 'space3d':
            x, y, z = v.split(' ')
            return Space3D( v )
        elif k.dtype == 'rank':
            return Rank( v )
        elif k.dtype == 'boolean' or k.dtype == 'bool':
            return Boolean( v )
        else:
            return Aspect( v )
    except Exception as e:
        print(e)
        raise Exception("[ERROR Aspect.py]: Failed to load value " + str(v) \
                        + " as type " + k.dtype + ' attr#' + str(k.order))