# -*- coding: utf-8
# Reinaldo Chaves (reinaldo@abraji.org.br)
# Script that uses our statistical model to make assessments of the likelihood 
# of hate speech on automatically captured tweets - these assessments are then 
# stored in Airtable
# Model: https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment
#

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import os
import pandas as pd
import requests
import json
import time


# Loads the pretrained XLM-roBERTa-base model that is on the computer
path = "app\\" # your path
model_name = "roberta" # your path
model = f"{path}{model_name}"
#print(model)

tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForSequenceClassification.from_pretrained(model)

clf = pipeline("text-classification", model=model, tokenizer=tokenizer)
#answer = clf("Este es un ejemplo")
#print(type(answer))
#print(answer[0])
#dict = answer[0]
#print(type(dict))
#print(dict.keys()) 
#print(dict['score'])


# Function to add new data to airtable
def add_to_airtable(tweet_id, probability_of_being_an_attack, created_at, source, expanded_url, author_name, author_screen_name, location,text, likely_target_of_attack, ENDPOINT):
    data = {
        "records": [
            {
                "fields": {
                    "text": text,
                    "probability_of_being_an_attack": str(probability_of_being_an_attack),
                    "likely_target_of_attack": str(likely_target_of_attack),
                    "tweet_id": str(tweet_id),
                    "created_at": str(created_at),
                    "author_screen_name": str(author_screen_name),
                    "author_name": str(author_name),
                    "location": str(location),
                    "source": str(source),
                    "expanded_url": str(expanded_url)
                    }
                }
            ]
        }
    
    data = json.dumps(data, indent=4, sort_keys=False, default=str)
    #print(data)
    #time.sleep(1)
       
    try:
        r = requests.request("POST", ENDPOINT, headers=headers, data=data)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    #print(f"Response status code: {r.status_code}")
    #print(r.json()) 

    return r.status_code 



# BRAZIL
# Airtable keys
# https://airtable.com/api

# First, collects the tweets that are already stored in the Airtable table - Portuguese - Brazil
# The tweets directly from API
AIRTABLE_BASE_ID_P = ""
AIRTABLE_TABLE_NAME = ""
AIRTABLE_API_KEY = ""

ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_P}/{AIRTABLE_TABLE_NAME}'

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

params = ()
airtable_records = []
run = True
while run is True:
  response = requests.get(ENDPOINT, params=params, headers=headers)
  airtable_response = response.json()
  airtable_records += (airtable_response['records'])
  if 'offset' in airtable_response:
     run = True
     params = (('offset', airtable_response['offset']),)
  else:
     run = False

airtable_rows = [] 
airtable_index = []
for record in airtable_records:
    airtable_rows.append(record['fields'])
    airtable_index.append(record['id'])
df_current_data_p = pd.DataFrame(airtable_rows, index=airtable_index)
df_current_data_p.info()


# Second, loads the tweets that have already been evaluated by the BERT model
AIRTABLE_BASE_ID_P_already = ""
AIRTABLE_TABLE_NAME_already = ""

ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_P_already}/{AIRTABLE_TABLE_NAME_already}'

params = ()
airtable_records = []
run = True
while run is True:
  response = requests.get(ENDPOINT, params=params, headers=headers)
  airtable_response = response.json()
  airtable_records += (airtable_response['records'])
  if 'offset' in airtable_response:
     run = True
     params = (('offset', airtable_response['offset']),)
  else:
     run = False

airtable_rows = [] 
airtable_index = []
for record in airtable_records:
    airtable_rows.append(record['fields'])
    airtable_index.append(record['id'])
df_current_data_p_rated = pd.DataFrame(airtable_rows, index=airtable_index)
df_current_data_p_rated.info()


# Merge the dataframes and leave only the tweets not yet evaluated, by ID


all_data = pd.merge(df_current_data_p, \
    df_current_data_p_rated, \
    how = 'left',
    left_on=['author_screen_name','text'], \
    right_on=['author_screen_name','text'])

all_data  = all_data[all_data['probability_of_being_an_attack'].isna()]
all_data.info()

all_data = all_data[["coordinates", "tweet_id_x", "expanded_url_x", "source_x", "created_at_x", "author_screen_name", "author_name_x", "location_x", "likely_target_of_attack_x", "text", "geo"]]

all_data.rename(columns = {'coordinates_x':'coordinates'},inplace = True)
all_data.rename(columns = {'tweet_id_x':'tweet_id'},inplace = True)
all_data.rename(columns = {'expanded_url_x':'expanded_url'},inplace = True)
all_data.rename(columns = {'source_x':'source'},inplace = True)
all_data.rename(columns = {'created_at_x':'created_at'},inplace = True)
all_data.rename(columns = {'author_name_x':'author_name'},inplace = True)
all_data.rename(columns = {'location_x':'location'},inplace = True)
all_data.rename(columns = {'likely_target_of_attack_x':'likely_target_of_attack'},inplace = True)
all_data.rename(columns = {'geo_x':'geo'},inplace = True)
all_data.info()


# Test if there are tweets
size = len(all_data.index)
if size != 0:

    model_notes = []
    for index, row in all_data.iterrows():
        tweet_id = row["tweet_id"]
        source = row["source"]
        created_at = row["created_at"]
        author_screen_name = row["author_screen_name"]
        author_name = row["author_name"]
        location = row["location"]
        likely_target_of_attack = row["likely_target_of_attack"]
        text = str(row["text"])
        expanded_url = row["expanded_url"]

        answer = clf(text)
        values = answer[0]
        note = values['score']

        dicionario = {"text": text, 
        "probability_of_being_an_attack": str(note),
        "likely_target_of_attack": likely_target_of_attack,
        "tweet_id": tweet_id,
        "created_at": created_at,
        "author_screen_name": author_screen_name,
        "author_name": author_name,
        "location": location,
        "source": source,
        "expanded_url": expanded_url
        }
        model_notes.append(dicionario)

    df_model_notes_br = pd.DataFrame(model_notes)
    df_model_notes_br.info()

    #df_model_notes_br.to_excel('test_notes_brazil.xlsx',sheet_name='Sheet1',index=False)


    # Add the new model ratings
    AIRTABLE_BASE_ID_P_RATES = ""
    AIRTABLE_TABLE_NAME_RATES = ""
    ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_P_RATES}/{AIRTABLE_TABLE_NAME_RATES}'

    for num, row in df_model_notes_br.iterrows():
        tweet_id = row['tweet_id']
        created_at = row['created_at']
        source = row['source']
        location = row['location']
        expanded_url = row['expanded_url']
        author_name = row['author_name']
        author_screen_name = row['author_screen_name']
        text = row['text']
        likely_target_of_attack = row['likely_target_of_attack']
        probability_of_being_an_attack = row['probability_of_being_an_attack']

        add_to_airtable(tweet_id, probability_of_being_an_attack, created_at, source, expanded_url, author_name, author_screen_name, location,text,likely_target_of_attack, ENDPOINT)

        

 


# MEXICO
# Airtable keys
# https://airtable.com/api


# First, collects the tweets that are already stored in the Airtable table - Spanish - Mexico
# The tweets directly from API
AIRTABLE_BASE_ID_M = ""
AIRTABLE_TABLE_NAME_M = ""

ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_M}/{AIRTABLE_TABLE_NAME_M}'

params = ()
airtable_records = []
run = True
while run is True:
  response = requests.get(ENDPOINT, params=params, headers=headers)
  airtable_response = response.json()
  airtable_records += (airtable_response['records'])
  if 'offset' in airtable_response:
     run = True
     params = (('offset', airtable_response['offset']),)
  else:
     run = False

airtable_rows = [] 
airtable_index = []
for record in airtable_records:
    airtable_rows.append(record['fields'])
    airtable_index.append(record['id'])
df_current_data_m = pd.DataFrame(airtable_rows, index=airtable_index)
df_current_data_m.info()


# Second, loads the tweets that have already been evaluated by the BERT model
AIRTABLE_BASE_ID_M_already = ""
AIRTABLE_TABLE_NAME_already_M = ""

ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_M_already}/{AIRTABLE_TABLE_NAME_already_M}'

params = ()
airtable_records = []
run = True
while run is True:
  response = requests.get(ENDPOINT, params=params, headers=headers)
  airtable_response = response.json()
  airtable_records += (airtable_response['records'])
  if 'offset' in airtable_response:
     run = True
     params = (('offset', airtable_response['offset']),)
  else:
     run = False

airtable_rows = [] 
airtable_index = []
for record in airtable_records:
    airtable_rows.append(record['fields'])
    airtable_index.append(record['id'])
df_current_data_m_rated = pd.DataFrame(airtable_rows, index=airtable_index)
df_current_data_m_rated.info()


# Filter BERT model ratings greater than or equal to 0.8
#df_current_data_e = df_current_data_m_rated.copy()
#df_current_data_e['probability_of_being_an_attack'] = df_current_data_e['probability_of_being_an_attack'].astype(float)
#df_current_data_e = df_current_data_e[df_current_data_e['probability_of_being_an_attack'] >= 0.8]
#df_current_data_e.info()


all_data = pd.merge(df_current_data_m, \
    df_current_data_m_rated, \
    how = 'left',
    left_on=['author_screen_name','text'], \
    right_on=['author_screen_name','text'])

all_data  = all_data[all_data['probability_of_being_an_attack'].isna()]
all_data.info()

all_data = all_data[["coordinates", "tweet_id_x", "expanded_url_x", "source_x", "created_at_x", "author_screen_name", "author_name_x", "location_x", "likely_target_of_attack_x", "text", "geo"]]

all_data.rename(columns = {'coordinates_x':'coordinates'},inplace = True)
all_data.rename(columns = {'tweet_id_x':'tweet_id'},inplace = True)
all_data.rename(columns = {'expanded_url_x':'expanded_url'},inplace = True)
all_data.rename(columns = {'source_x':'source'},inplace = True)
all_data.rename(columns = {'created_at_x':'created_at'},inplace = True)
all_data.rename(columns = {'author_name_x':'author_name'},inplace = True)
all_data.rename(columns = {'location_x':'location'},inplace = True)
all_data.rename(columns = {'likely_target_of_attack_x':'likely_target_of_attack'},inplace = True)
all_data.rename(columns = {'geo_x':'geo'},inplace = True)
all_data.info()


# Test if there are tweets
size = len(all_data.index)
if size != 0:

    model_notes = []
    for index, row in all_data.iterrows():
        tweet_id = row["tweet_id"]
        source = row["source"]
        created_at = row["created_at"]
        author_screen_name = row["author_screen_name"]
        author_name = row["author_name"]
        location = row["location"]
        likely_target_of_attack = row["likely_target_of_attack"]
        text = str(row["text"])
        expanded_url = row["expanded_url"]

        answer = clf(text)
        values = answer[0]
        note = values['score']

        dicionario = {"text": text, 
        "probability_of_being_an_attack": str(note),
        "likely_target_of_attack": likely_target_of_attack,
        "tweet_id": tweet_id,
        "created_at": created_at,
        "author_screen_name": author_screen_name,
        "author_name": author_name,
        "location": location,
        "source": source,
        "expanded_url": expanded_url
        }
        model_notes.append(dicionario)

    df_model_notes_mx = pd.DataFrame(model_notes)
    df_model_notes_mx.info()

    #df_model_notes_br.to_excel('test_notes_brazil.xlsx',sheet_name='Sheet1',index=False)


    # Add the new model ratings
    ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_M_already}/{AIRTABLE_TABLE_NAME_already_M}'

    for num, row in df_model_notes_mx.iterrows():
        tweet_id = row['tweet_id']
        created_at = row['created_at']
        source = row['source']
        location = row['location']
        expanded_url = row['expanded_url']
        author_name = row['author_name']
        author_screen_name = row['author_screen_name']
        text = row['text']
        likely_target_of_attack = row['likely_target_of_attack']
        probability_of_being_an_attack = row['probability_of_being_an_attack']

        add_to_airtable(tweet_id, probability_of_being_an_attack, created_at, source, expanded_url, author_name, author_screen_name, location,text,likely_target_of_attack, ENDPOINT)

        


