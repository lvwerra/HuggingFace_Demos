import json
import itertools
import pandas as pd

def load_json(f_path):
    with open(f_path) as f:
        data = json.load(f)
    
    return data

def load_jsonl(fn):
    result = []
    with open(fn, 'r') as f:
        for line in f:
            data = json.loads(line)
            result.append(data)
    return result 

def to_jsonl(fn,data,mode='w'):
    with open(fn, mode) as outfile:
        if isinstance(data,list):
            for entry in data:
                json.dump(entry, outfile)
                outfile.write('\n')
        else:
            json.dump(data, outfile)
            outfile.write('\n')


def flatten_list(list_of_lists):
    '''
    list_of_lists : TYPE
        any iregular list.

    Returns
    -------
    a flat list

    '''
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten_list(list_of_lists[0]) + flatten_list(list_of_lists[1:])
    return list_of_lists[:1] + flatten_list(list_of_lists[1:])            

def hyper_param_permutation(hyper_params):
    ## prepare params for gride search ##
    assert isinstance(hyper_params,dict)
    param_names = list(hyper_params.keys())
    all_param_list = [hyper_params[k] for k in param_names]
    permu = list(itertools.product(*all_param_list))
    res = [dict(zip(param_names,i)) for i in permu]
    return res

def load_hp_res(hp_res_dir,to_csv_dir=None,sort_col=None):
    ## load hp tuning results 
    res = load_jsonl(hp_res_dir)
    df = pd.json_normalize(res,sep='_')
    
    if isinstance(sort_col, list):
        df.sort_values(by=sort_col,
                       ascending=False,
                       inplace=True)
    if isinstance(to_csv_dir,str):
        df.to_csv(to_csv_dir)
    
    return df,res

def get_best_hp_param(hp_res_dir:str,sort_col:list):
    ## get best param based on sorting criteria 
    df,hp_dict = load_hp_res(hp_res_dir,sort_col)
    best_param = hp_dict[df.index[0]]
    
    return best_param

if __name__ == "__main__":
    
    
    inp_param = {'batch':[1,2,3],
                 'lr':[0.1,0.2,0.3]}
    
    res = hyper_param_permutation(inp_param)
    print(res)