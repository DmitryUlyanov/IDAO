import os
import numpy as np
import pandas as pd
import sys
import json 

def score_series(y_true, y_pred):
    """
        Expects y_true and y_pred to be 1d arrays of the same lenght
    """
    return np.mean(np.abs(y_true - y_pred))/np.mean(np.abs(y_true))

def scorer(df_true, df_pred):
   
    scores = []
    for ID in df_true.ATM_ID.unique():
        
        df_true_part = df_true.query('ATM_ID == @ID')
        df_pred_part = df_pred.query('ATM_ID == @ID')
        
        
        if df_true_part.shape[0] != df_pred_part.shape[0]:
            print("$Wrong number of predictions for ATM_ID = %d$" % ID)
            sys.exit(4)

        if not np.all(df_true_part.DATE == df_pred_part.DATE):
            print("$Could not parse dates for ATM_ID = %d. Wrong format\encoding? Duplicated/wrong dates?$" % ID)
            sys.exit(4)
       
        score = score_series(df_true_part.CLIENT_OUT, df_pred_part.CLIENT_OUT)
        scores.append(score)
    
    return np.mean(scores)

def check_submission(df_pred):
    if len(df_pred.columns) != 3:
            print('$Wrong number of columns$')
            sys.exit(4)
    
    for c in ['ATM_ID', 'DATE', 'CLIENT_OUT']:
        if c not in df_pred.columns:
            print('$Column %s is missing in your submission.$' % c)
            sys.exit(4)

    if df_pred.shape[0] != 1650:
        print('$The submission should have exactly 1650 rows.$')
        sys.exit(4)

if __name__ == '__main__':
    true_values_path = sys.argv[3] 
    submitted_path =  sys.argv[2]

    
    # Load csv file
    if submitted_path.endswith('tar.gz'):
        print("$Use .zip of .gz format please. Pandas does not load .tar.gz correctly.$")
        sys.exit(4)
    try:
        df_pred = pd.read_csv(submitted_path)
        check_submission(df_pred)
        df_pred = df_pred.sort_values(['ATM_ID', 'DATE']).reset_index(drop=True)

    except Exception as e:
        print("$Error while reading .csv file: " + str(e) + "$")
        sys.exit(4)

    # Load target
    df_true = pd.read_csv(true_values_path).sort_values(['ATM_ID', 'DATE']).reset_index(drop=True)
    score = scorer(df_true, df_pred) * 10000

    print(score)
    sys.exit(0)