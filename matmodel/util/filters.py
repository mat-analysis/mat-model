def names2indexes(sel_attributes, attributes_desc):
    return list(map(lambda y: attributes_desc.index(y), filter(lambda x: x['text'] in sel_attributes, attributes_desc)))

def attributes2names(attributes_desc):
    return list(map(lambda y: y['text'], attributes_desc))