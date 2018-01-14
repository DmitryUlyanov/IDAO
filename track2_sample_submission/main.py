import pandas as pd

train = pd.read_csv('train.csv.zip')



submission = pd.DataFrame(train.user_id.unique()[:5000], columns = ['user_id'])

submission['id3_1'] = 0
submission['id3_2'] = 1
submission['id3_3'] = 2
submission['id3_4'] = 3
submission['id3_5'] = 4
                       
submission.to_csv('submission.csv', index=False)