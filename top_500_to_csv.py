import requests
import json
import pandas as pd

txtfile = open("top 500.txt")

txtlines = txtfile.readlines()
url = 'http://muzis.ru/api/search.api'

from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
   username='fc6ef0da-16d5-442f-974a-a106a3c8897f',
   password='8tdG1H7dkFm0',
   version='2016-05-19')

columns = ['anger',
           'disgust',
           'fear',
           'joy',
           'sadness',
           'file_mp3']
music_dataset = pd.DataFrame(columns=columns)

for i in  range(0 ,len(txtlines)):
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
            answer['file_mp3']]
            music_dataset.loc[len(music_dataset)] = a_list
        print(music_dataset)




txtfile.close()
