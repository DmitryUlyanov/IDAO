import numpy as np

def scorer(y_true, y_pred, num_users=1079572):
    '''
        `y_true` and `y_pred` are dictionaries of type {user: items_list}
        
        `num_users` is the number of users in training set. 
        The scorer expects predictions for exactly `ceil(num_users*0.05)` users
        
        For private and public leaderboard evaluation:
            - for the track one scorer `num_users` is equal to 1079572
            - for the track two `num_users=100000`
    '''
    
    num_users_5p = np.ceil(0.05 * num_users)
    
    # Check everything is correct
    assert type(y_true) == type(y_pred) == dict, 'Need `y_pred` and `y_true` to be dictionaries.'
    assert len(y_pred) == num_users_5p, 'Found predictions for %d users, instead of %d.' % (len(y_pred), num_users_5p)
    assert np.all([len(x) == 5 for x in y_pred.values()]), 'Please, submit exactly 5 items per user.'
    
    # Compute score
    score = 0
    for user, items_pred in y_pred.items():
        items_true = y_true.get(user, [])
        score += len(set(items_true) & set(items_pred)) > 0

    return score / float(len(y_pred)) * 10000.0


# Tests
if __name__ == '__main__': 
   
    # 1
    
    y_true = {1: [0], 2: [1,2], 3: []}
    try: 
        scorer(y_true, [24, 51], 3)
    except Exception as e:
        assert str(e)=='Need `y_pred` and `y_true` to be dictionaries.', '#1 WRONG'
    else:
        assert False, '#1 WRONG'

    # 2

    y_true = {1: [0], 2: [1,2], 3: []}
    y_test = {1: range(5), 2: range(5)}
    try:
        scorer(y_true, y_test, 3)
    except Exception as e:
        assert str(e)=='Found predictions for 2 users, instead of 1.', '#2 WRONG'
    else:
        assert False, '#2 WRONG'

    # 3

    y_true = {1: [0], 2: [1,2], 3: []}
    y_test = {1: range(4)}
    try:
        scorer(y_true, y_test, 3)
    except Exception as e:
        assert str(e)=='Please, submit exactly 5 items per user.', '#3 WRONG'
    else:
        assert False, '#3 WRONG'
    
    # 4 

    y_true = {1: [0], 2: [1,2], 3: [], 4: [-3,33], 5: [0], 6: [1,2], 7: [], 8: [-3,33],9: [0], 10: [1,2], 311: [], 244: [-3,33]}
    y_test = {3: range(5)}

    assert scorer(y_true, y_test, num_users=20) == 0

    # 5 
    
    y_true = {1: [0], 2: [1,2], 3: [], 4: [-3,33], 5: [0], 6: [1,2], 7: [], 8: [-3,33],9: [0], 10: [1,2], 311: [], 244: [-3,33]}
    y_test = {1: range(5), 3: range(5), 6: range(5)}

    assert scorer(y_true, y_test, num_users=60) == 2./3. * 10000

    print('Passed')