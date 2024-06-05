import pandas as pd
import json
from tqdm.auto import tqdm

from matdata.preprocess import organizeFrame

from matmodel.base import Trajectory, Movelet
from matmodel.evaluation import Quality
from matmodel.descriptor import readDescriptor, df2descriptor

# ------------------------------------------------------------------------------------------------------------
# TRAJECTORY 
# ------------------------------------------------------------------------------------------------------------
def df2trajectory(df, data_desc=None, tid_col='tid', label_col='label'):
    """
    Convert a DataFrame to a list of Trajectory objects.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be converted.
    data_desc : str, optional
        The data descriptor file, a file path for the data descriptor JSON. If None, a descriptor
        is generated from the DataFrame (default None).
    tid_col : str, optional
        The name of the column representing trajectory IDs (default 'tid').
    label_col : str, optional
        The name of the column representing class labels (default 'label').

    Returns:
    --------
    list of Trajectory
        The list of converted Trajectory objects.
    DataDescriptor
        The data descriptor object used for reading the dataset trajectories.
    """
    
    df = normalize(df)
    
    # Translate atributes:
    if data_desc:
        data_desc = readDescriptor(data_desc)
    else:
        data_desc = df2descriptor(df, tid_col, label_col)
    
    features = data_desc.feature_names
    
    ls_trajs = []
    def processT(df, tid):
        df_aux = df[df[tid_col] == tid]
        label = df_aux[label_col].unique()[0]
        
        points = list( df_aux[features].itertuples(index=False, name=None) )
        return Trajectory(tid, label, points, data_desc)
    
    tids = list(df[tid_col].unique())
    #tids = tids[from_traj: to_traj if len(tids) > to_traj else len(tids)] # TODO
    ls_trajs = list(map(lambda tid: processT(df, tid), tqdm(tids, desc='Converting Trajectories')))
        
    return ls_trajs, data_desc

# ------------------------------------------------------------------------------------------------------------
# MOVELETS 
# ------------------------------------------------------------------------------------------------------------
def json2movelet(file, name='movelets', count=0):
    
    data = json.load(file)
    
    if name not in data.keys():
        name='shapelets'
    
    l = len(data[name])
    
    count = 0
    def parseM(x):
        nonlocal count
        
        tid = data[name][x]['trajectory']
        label = data[name][x]['label']
        
        points = pd.DataFrame(data[name][x]['points_with_only_the_used_features'])
        points['tid'] = tid
        points['label'] = label
        data_desc = df2descriptor(normalize(points))

        T = Trajectory(tid, label, None, None) #[], data_desc)
        start = int(data[name][x]['start'])
        end   = int(data[name][x]['end'])
        quality = Quality(float(data[name][x]['quality']['quality']), # * 100.0), 
                          size=float(data[name][x]['quality']['size']), 
                          start=float(data[name][x]['quality']['start']), 
                          dimensions=float(data[name][x]['quality']['dimensions']))
        m = Movelet(T, start, points, data[name][x]['pointFeatures'], quality, count, data_desc.attributes)
        
        # Converting points
        points = list( points[data_desc.feature_names].itertuples(index=False, name=None) )
        m.readSequence(points, data_desc)
        
        count += 1
        return m
    
    ls_movelets = list(map(lambda x: parseM(x), tqdm(range(0, l), desc='Reading Movelets')))

    ls_movelets.sort(key=lambda x: x.quality.value, reverse=True)
    return ls_movelets

def normalize(df):
    df, columns_order_zip, _ = organizeFrame(df, make_spatials=True)
    return df[columns_order_zip]