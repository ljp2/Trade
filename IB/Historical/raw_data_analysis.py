import os
import pandas as pd

data_directory  = 'C:/Trade/Data'
look_ahead = 5

orig_columns = ['time', 'open', 'high', 'low', 'close', 'volume']

for filename in os.listdir(data_directory):
    if filename.endswith('.csv'):
        data = pd.read_csv(os.path.join(data_directory, filename), sep='\t')
        data.columns = orig_columns

        N = len(data)
        N_last_check = N - look_ahead - 1

    highest_high = []
    lowest_low = []
    high_before_low = []

    for i in range(N):
        if i >= N_last_check:
            highest_high.append(None)
            lowest_low.append(None)
            high_before_low.append(None)
        else:
            high_values = data['high'].iloc[i+1:i+look_ahead+1]
            low_values = data['low'].iloc[i+1:i+look_ahead+1]
            highest_index = high_values.idxmax()
            lowest_index = low_values.idxmin()

            highest_value = data['high'].iloc[highest_index]
            lowest_value = data['low'].iloc[lowest_index]
    
            highest_high.append(highest_value)
            lowest_low.append(lowest_value)
            high_before_low.append(highest_index < lowest_index)

    data['highest_high'] = highest_high
    data['lowest_low'] = lowest_low
    data['high_before_low'] = high_before_low


    print(data.head(8))
    print(data.tail(8))
    data.to_csv('test.csv', sep='\t', index=False)

    break
