from __future__ import print_function
import pandas as pd
import numpy as np
import operator, random
from globals import *
from watson_developer_cloud import ToneAnalyzerV3
import requests, requests

#music dataset
def load_dataset():
    frames = list()
    for i in range(0, 6):
        path = 'data/dataset' + str(i) + '.csv'
        tmp_dataset = pd.read_csv(path,
                            delimiter=',',
                            index_col = False)
        tmp_dataset['genre'] = i
        frames.append(tmp_dataset)

    path = 'data/top_500.csv'
    tmp_dataset = pd.read_csv(path,
                        delimiter=',',
                        index_col = False)
    tmp_dataset['genre'] = 6
    frames.append(tmp_dataset)

    return pd.concat(frames)
DATASET = load_dataset()

#formirate link for mp3
def get_track_url(mp3_name = 'krphheaup850.mp3'):
    return 'http://f.muzis.ru/' + mp3_name

def find_nearest(value, array):
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def find_best_match(dataset, text_emotion):
    columns = list()

    #sort emotion by value
    for elem in sorted(text_emotion.items(), key=operator.itemgetter(1), reverse=True):
        columns.append(elem[0])

    tmp = dataset

    #find of nearest for every value from large to low
    for key in columns:
        unique_values = tmp[key].unique()
        nearest = find_nearest(text_emotion[key], unique_values)
        tmp = tmp[tmp[key] == nearest]
    return tmp

def get_match(text, value):
    #get emotions from IBM WATSON
    tone_anal = ToneAnalyzerV3(
                    username='2c744365-e72f-49f6-a452-d9beda1d5422',
                    password='PXCyLNY3uLfr',
                    version='2016-05-19')

    tone_result = tone_anal.tone(text=text)['document_tone']['tone_categories'][0]['tones']

    #formirate emo dictionary
    emotions = dict()
    for tone in tone_result:
        emotions.update({tone['tone_id'] : round(tone['score'], 1)})


    tracks = find_best_match(DATASET[DATASET['genre'] == value], emotions)
    #tracks = tracks.sample()[['file_mp3', 'performer', 'title']]
    mp3 = random.choice(tracks['file_mp3'].tolist())
    return get_track_url(mp3) #, performer, track_name

def get_random(value):
    '''
    if value != 7:
        df = DATASET[DATASET['genre'] == value].sample()[['file_mp3', 'performer', 'title']]
    else:
        df = DATASET.sample()[['file_mp3', 'performer', 'title']]
    '''
    df = DATASET[DATASET['genre'] == value]
    mp3 = random.choice(df['file_mp3'].tolist())# DATASET.sample()[['file_mp3', 'performer', 'title']]
    return get_track_url(mp3)

