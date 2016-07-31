import requests
import json
import pandas as pd

txtfile = open("top 500.txt")

txtlines = txtfile.readlines()
url = 'http://muzis.ru/api/search.api'

from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
                    username='2c744365-e72f-49f6-a452-d9beda1d5422',
                    password='PXCyLNY3uLfr',
                    version='2016-05-19')

columns = ['anger',
           'disgust',
           'fear',
           'joy',
           'sadness',
           'file_mp3',
           'performer',
           'title']
music_dataset = pd.DataFrame(columns=columns)

for i in  range(300 ,len(txtlines)):
    line = txtlines[i].split("\t")
    req_line = line[1]+' '+line[2]
    data = {
        'q_track': req_line,
        'size': 1
    }

    str_answer = requests.post(url, data)
    json_answer = json.loads(str_answer.text)

    for answer in json_answer['songs']:
        if answer['lyrics'] != '':
            tmp = tone_analyzer.tone(text=answer['lyrics'])

            a_list = [
            round(tmp['document_tone']['tone_categories'][0]['tones'][0]['score'], 1),  # anger
            round(tmp['document_tone']['tone_categories'][0]['tones'][1]['score'], 1),  # disgust
            round(tmp['document_tone']['tone_categories'][0]['tones'][2]['score'], 1), # fear
            round(tmp['document_tone']['tone_categories'][0]['tones'][3]['score'], 1), # joy
            round(tmp['document_tone']['tone_categories'][0]['tones'][4]['score'], 1), # sadness
            answer['file_mp3'],
            answer['performer'],
            answer['track_name']]
            music_dataset.loc[len(music_dataset)] = a_list
    print(i)

def changeencode(data, cols):
    for col in cols:
        data[col] = data[col].str.decode('iso-8859-1').str.encode('utf-8')
    return data
music_dataset = changeencode(music_dataset, ['performer', 'title'])
music_dataset.to_csv('lastdataset.csv')


txtfile.close()
