from matmodel.comparator import Comparator

class DataDescriptor:
    def __init__(self, idDesc=None, labelDesc=None, attributes=[]):
        self.idDesc = idDesc
        self.labelDesc = labelDesc
        
        self.attributes = attributes
        
        self.dependencies = None
        
    def __iter__(self):
        self.actual = 0 
        return self

    def __next__(self):
        if self.actual < len(self.attributes):
            self.actual += 1
            return self.attributes[self.actual-1]
        else:
            raise StopIteration
            
    @property
    def feature_names(self):
        return list(map(lambda attr: attr.text, self.attributes))
        
    @staticmethod
    def instantiate(json_obj):
        jof_id = FeatureDescriptor.instantiate(json_obj['idFeature'])
        jof_lb = FeatureDescriptor.instantiate(json_obj['labelFeature'])
        
        attrs = list(map(lambda a: FeatureDescriptor.instantiate(a), json_obj['attributes']))
        
        dd = DataDescriptor(jof_id, jof_lb, attrs)
        
        dd.dependencies = dict(map(lambda d: (d.dependency_group, \
                                             list(filter(lambda a: a.dependency_group == d.dependency_group, attrs))), attrs))

        if None in dd.dependencies.keys():
            del dd.dependencies[None]
        if len(dd.dependencies.keys()) == 0:
            dd.dependencies = None
        
        return dd

class FeatureDescriptor:
    def __init__(self, order, text, dtype='nominal', comparator=None, weight=None):
        self.order = order
        self.dtype = dtype
        self.text = text
        
        self.weight = weight
        
        self.comparator = comparator
        
        self.dependency_group = None
        
    @property
    def name(self):
        return self.text
    
    @staticmethod
    def instantiate(json_obj):
        fd = FeatureDescriptor(json_obj['order'], json_obj['text'], json_obj['type'])
        
        if 'weight' in json_obj.keys():
            fd.weight = float(json_obj['weight'])
        if 'dependency' in json_obj.keys():
            fd.dependency_group = json_obj['dependency']
        
        if 'comparator' in json_obj.keys():
            fd.comparator = Comparator.instantiate(json_obj)
        return fd
    
    def __repr__(self):
        return str(self.order) + '. ' + self.name + ' ('+self.dtype+')'
# ----------------------------------------------------------------------------------------------------
def readDescriptor(file_path):
    import ast
    file = open(file_path)
    desc = ast.literal_eval(file.read())
    file.close()
    return DataDescriptor.instantiate(desc)

def df2descriptor(df, tid_col='tid', label_col='label'):
    columns = list(df.columns)
    desc = {
        'idFeature': {'order': columns.index(tid_col)+1, 'type': 'numeric', 'text': tid_col}, 
        'labelFeature': {'order': columns.index(label_col)+1, 'type': 'nominal', 'text': label_col},
        'attributes': []
    }
    
    for i in range(len(columns)):
        
        if columns[i] == tid_col or columns[i] == label_col:
            continue
        
        if columns[i] == 'lat_lon' or columns[i] == 'space': # Separate lat and lon becomes Numeric Aspect
            dtype = 'space2d'
            comparator = 'euclidean'
        elif columns[i] == 'xyz' or 'xyz' in columns[i]:
            dtype = 'space3d'
            comparator = 'euclidean'
        elif columns[i] == 'time' or columns[i] == 'datetime' or \
             df.dtypes[columns[i]] == 'datetime64[ns]' or df.dtypes[columns[i]] == '<M8[ns]':
            dtype = 'datetime'
            comparator = 'datetime'
        elif df.dtypes[columns[i]] == int or df.dtypes[columns[i]] == float:
            dtype = 'numeric'
            comparator = 'difference'
        elif df.dtypes[columns[i]] == bool:
            dtype = 'boolean'
            comparator = 'equals'
        else:
            dtype = 'nominal'
            comparator = 'equals'
        
        desc['attributes'].append({
            'order': i+1,
            'type': dtype,
            'text': columns[i],
            'comparator': {'distance': comparator}
        })
    
    return DataDescriptor.instantiate(desc)

def descriptor2json(dataDescriptor):
    desc = {
        'idFeature': {
            'order': dataDescriptor.idDesc.order, 
            'type': dataDescriptor.idDesc.type, 
            'text': dataDescriptor.idDesc.text
        }, 
        'labelFeature': {
            'order': dataDescriptor.labelDesc.order, 
            'type': dataDescriptor.labelDesc.type, 
            'text': dataDescriptor.labelDesc.text
        },
        'attributes': list(map(lambda at: 
            {
                'order': at.order, 
                'type': at.type, 
                'text': at.text,
                'weight': at.weight,
                'comparator': {
                    'distance': at.comparator # TODO inverse convert
                    # TODO other params
                }
            },
                              
        dataDescriptor.attributes))
    }
    
    return desc