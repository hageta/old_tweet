#coding: UTF-8
import pandas as pd
import os

class CsvOperator:

    @staticmethod
    def export_csv(array_dict, path, title = ''):
        if path is None:
             path = os.path.dirname(os.path.abspath(__name__))
        os.chdir(path)
        title = title+'_' if (title != '') else ''
        def extract_period(data_frame):
            print(data_frame.head(1))
            start = list(data_frame.head(1)['created_at'])[0]
            end = list(data_frame.tail(1)['created_at'])[0]
            return start + '_' + end

        data_frame = pd.DataFrame.from_dict(array_dict)
        period = extract_period(data_frame)
        data_frame.to_csv( str(title) + period + '.csv')
