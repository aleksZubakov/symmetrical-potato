from __future__ import print_function
import pandas as pd
import numpy as np
import operator, random
from globals import *
from watson_developer_cloud import ToneAnalyzerV3
import requests, requests

#music dataset
CSV_PATH = 'newdataset.csv'
DATASET = pd.read_csv(CSV_PATH,
                delimiter=',',
                index_col = False)

#formirate link for mp3
def get_track_url(mp3_name = 'krphheaup850.mp3'):
    return 'http://f.muzis.ru/' + mp3_name

def get_sorted_keys(dictionary):
    result = list()
    for elem in sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True):
        result.append(elem[0])

    return result

def find_nearest(value, array):
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def find_best_match(dataset, text_emotion):
    columns = get_sorted_keys(text_emotion)
    tmp = dataset

    for key in columns:
        unique_values = tmp[key].unique()
        nearest = find_nearest(text_emotion[key], unique_values)
        tmp = tmp[tmp[key] == nearest]
    return tmp['file_mp3']

def get_match(text):
    tone_anal = ToneAnalyzerV3(
                    username='fc6ef0da-16d5-442f-974a-a106a3c8897f',
                    password='8tdG1H7dkFm0',
                    version='2016-05-19')

    tone_result = tone_anal.tone(text=text)['document_tone']['tone_categories'][0]['tones']
    emotions = dict()
    for tone in tone_result:
        emotions.update({tone['tone_id'] : round(tone['score'], 1)})
    track_names = find_best_match(DATASET, emotions)
    track_name = random.choice(track_names.tolist())
    return get_track_url(track_name)

def get_random():
    return get_track_url(random.choice(
                            DATASET['file_mp3'].tolist()))

