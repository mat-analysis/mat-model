# -*- coding: utf-8 -*-
"""
MAT-Tools: Python Framework for Multiple Aspect Trajectory Data Mining

The present application offers a tool, to support the user in the modeling of multiple aspect trajectory data. It integrates into a unique framework for multiple aspects trajectories and in general for multidimensional sequence data mining methods.
Copyright (C) 2022, MIT license (this portion of code is subject to licensing from source project distribution)

Created on Apr, 2024
Copyright (C) 2024, License GPL Version 3 or superior (see LICENSE file)


Authors:
    - Tarlis Portela
    - Vanessa Lago Machado
"""
import datetime

class Aspect():
    """
    Represents a generic attribute or 'aspect' of a point, such as a spatial, temporal, or categorical aspect.
    
    Attributes:
    -----------
    _value: 
        The actual value of the aspect.
    
    Methods:
    -----------
    value(units=None): 
        Property to get the value of the aspect.
    __repr__(): 
        Returns a string representation of the aspect.
    match(asp1, asp2): 
        Checks if two aspects are equal.
    __eq__(other): 
        Checks if this aspect is equal to another aspect based on its value.
    """
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
    """
    Represents a boolean aspect. The value can be a boolean or strings that can be interpreted as boolean.
    """
    def __init__(self, value): # TODO Other possible false and true values?
        if value in ['False', 'No', 'FALSE', 'false', 'N', '-', 'NO']:
            value = False
        elif value in ['True', 'Yes', 'TRUE', 'true', 'Y', 'YES', 'S']:
            value = True
        else:
            value = bool(value)
        Aspect.__init__(self, value)
    
class Numeric(Aspect):
    """
    Represents a numeric aspect, where the value is instantiated as a float.
    """
    def __init__(self, value):
        value = float(value)
        Aspect.__init__(self, value)
    
class Categoric(Aspect):
    """
    Represents a categorical aspect. The value is treated as a string variable.
    """
    def __init__(self, value):
        Aspect.__init__(self, value)

class Space2D(Aspect):
    """
    Represents a 2D spatial aspect, storing x and y coordinates.
    
    Attributes:
    -----------
    x (float): 
        The x-coordinate (latitude).
    y (float): 
        The y-coordinate (longitude).
    """
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
    """
    Represents a 3D spatial aspect, extending the 2D space with an additional z-coordinate.
    
    Attributes:
    -----------
    x (float): 
        The x-coordinate.
    y (float): 
        The y-coordinate.
    z (float): 
        The z-coordinate.
    """
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
    """
    Represents a temporal aspect, storing date and time information.
    
    Uni
    
    Attributes:
    -----------
    start or value (datetime): 
        The start time of the interval.
    mask (str): 
        The format in which the date and time is provided.
    
    Methods:
    --------
    day(): 
        Returns the day of the month.
    month(): 
        Returns the month.
    year():  
        Returns the year.
    weekday():  
        Returns the day of the week (0 for Monday, 6 for Sunday).
    isweekend(): C 
        hecks if the date falls on a weekend.
    isweekday():  
        Checks if the date falls on a weekday.
    hours():  
        Returns the hour of the day.
    minutes():  
        Returns the total minutes since the start of the day.
    seconds():  
        Returns the total seconds since the start of the day.
    microseconds():  
        Returns the total microseconds since the start of the day.
    get(units=None):  
        Returns the value in a specified unit (e.g., D, M, Y, etc.).
    convertMinToDate(minutes):  
        Converts minutes to a datetime object.
    convert(value, mask=None):  
        Converts a string value to a datetime object.
        
    Notes:
    ------
    units: The available unit codes are:
        - D: days
        - M: months
        - Y: years
        - w: weekday
        - h: hours
        - m: minutes
        - s: seconds
        - ms: microseconds
    """
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
    """
    Represents a temporal interval between two DateTime points.
    
    Attributes:
    -----------
    start or value (datetime): 
        The start time of the interval.
    end (datetime): 
        The end time of the interval.
    """
    def __init__(self, start, end, mask="%H:%M"):
        DateTime.__init__(self, start, mask)
        # Convert to datetime
        end = self.convert(end)
        self.end = end
        
    def __repr__(self):
        return '[{} 𛲔𛲔 {}]'.format(self.start, self.end)

class Rank(Aspect):
    """
    Represents a ranked aspect, containing ranked values.
    
    Attributes:
    -----------
    rank_values (list):
        A list of RankValue objects, each containing an aspect and its proportion.
    
    Methods:
    --------
    add(aspect, proportion): 
        Adds a ranked value to the rank with its proportion.
    """
    def __init__(self, descriptor):
        Aspect.__init__(self, descriptor)
        self.rank_values = [] # ->RankValue
        
    @property
    def descriptor(self):
        return self._value
    
    def add(self, aspect, proportion):
        self.rank_values.append(RankValue(aspect, proportion))
    
class RankValue:
    """
    Represents a value in a Rank, with its corresponding proportion.
    
    Attributes:
    -----------
    value (Aspect): 
        The aspect associated with this rank value.
    proportion (float): 
        The proportion associated with this rank value.
    """
    def __init__(self, value, proportion):
        self.value = value
        self.proportion = proportion

# ------------------------------------------------------------------------------------------------------------
def instantiateAspect(k,v):
    """
    Instantiates an Aspect object based on the data type specified in the DataDescriptor.
    
    Args:
    -----
    k: 
        DataDescriptor object that contains metadata about the attribute.
    v: 
        The raw value to be converted into an Aspect.
    
    Returns:
    --------
        An instantiated Aspect object (e.g., Boolean, Numeric, Space2D, DateTime, etc.).
    
    Raises:
    -------
    Exception: 
        If the instantiation fails for any reason.
    """
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