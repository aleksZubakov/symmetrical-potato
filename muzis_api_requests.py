from __future__ import print_function
import pandas as pd
import numpy as np
import operator, time

from watson_developer_cloud import ToneAnalyzerV3
import requests, requests

#formirate link for mp3
CSV_PATH = 'newdataset.csv'
def get_track_url(mp3_name = 'krphheaup850.mp3'):
    return 'http://f.muzis.ru/' + mp3_name

def load_dataset():
    result = pd.read_csv(CSV_PATH,
                delimiter=',',
                index_col = False
                )
    return result

def get_sorted_keys(dictionary):
    result = list()
    for key, value in sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True):
        result.append(key)

    return result

def find_nearest(value, array):
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def find_best_match(dataset, text_emotion):
    columns = get_sorted_keys(text_emotion)
    tmp = dataset.sort(columns)

    for key in columns:
        unique_values = tmp[key].unique()
        nearest = find_nearest(text_emotion[key], unique_values)
        tmp = tmp[tmp[key] == nearest]
    return tmp['file_mp3']

tone_analyzer = ToneAnalyzerV3(
   username='fc6ef0da-16d5-442f-974a-a106a3c8897f',
   password='8tdG1H7dkFm0',
   version='2016-05-19')


dataset = load_dataset()

emotions = {'anger' : 0.7,
           'disgust' : 0.3,
           'fear' : 0.5,
           'joy' : 0.1,
           'sadness' : 0.0}
start_time = time.time()
print(find_best_match(dataset, emotions))
print(time.time() - start_time)

