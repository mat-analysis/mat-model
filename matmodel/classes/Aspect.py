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

class Space2D(Aspect):
    def __init__(self, x, y):
        Aspect.__init__(self, str((x,y)))
        self.x = x
        self.y = y

    @Aspect.value.getter
    def value(self):
        return (self.x, self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Space3D(Space2D):
    def __init__(self, x, y, z):
        Space2D.__init__(x, y)
        Aspect.__init__(self, str((x,y,z)))
        self.z = z

    @Aspect.value.getter
    def value(self):
        return (self.x, self.y, self.z)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

class DateTimeAspect(Aspect):
    def __init__(self, value):
        Aspect.__init__(self, value)
    
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
    
    @Aspect.value.getter
    def value(self, units=None):
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
            raise Exception('[ERROR DateTimeAspect]: invalid \'units='+str(units)+'\' conversion.')
    
#    def __eq__(self, other):
#        return self._value == other._value

# ------------------------------------------------------------------------------------------------------------
def instantiateAspect(k,v):
    try:
        if k['type'] == 'nominal':
            return Aspect( str(v) )
        elif k['type'] == 'numeric':
            return Aspect( float(v) )
        elif k['type'] == 'space2d':
            x, y = v.split(' ')
            return Space2D(float(x), float(y))
        elif k['type'] == 'space3d':
            x, y, z = v.split(' ')
            return Space3D(float(x), float(y), float(z))
        elif k['type'] == 'boolean':
            return Aspect( bool(v) )
        elif k['type'] == 'datetime':
            from datetime import datetime
            #Format like: "YYYY-MM-DD HH:MM:SS.ffffff"
            return DateTimeAspect( datetime.fromisoformat(v) )
        else:
            return Aspect( v )
    except:
        raise Exception("[ERROR Aspect.py]: Filed to load value " + str(v) \
                        + " as type " + str(k['type']) + ' attr#' + str(k['order']))