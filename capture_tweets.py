# -*- coding: utf-8
# Reinaldo Chaves (reinaldo@abraji.org.br)
# Script that every day captures tweets from Mexico and Brazil in the Twitter API
# Profiles and keywords widely used in countries are sought to carry out attacks against journalists and environmental activists
#

import os
import tweepy as tw
import pandas as pd
import json
import requests
from datetime import datetime, timedelta

consumer_key = os.environ["TWEEPY_API_KEY"]
consumer_secret = os.environ["TWEEPY_CONSUMER_SECRET"]
access_token = os.environ["TWEEPY_ACCESS_TOKEN"]
access_token_secret = os.environ["TWEEPY_TOKEN_SECRET"]

# use Twitter keys for authentication, via Tweepy
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


#########
# BRAZIL
#########

# search for keywords most likely in Brazil to be used in hate attacks against journalists and heavily attacked environmental profiles
# Each search is limited to 500 characters
new_search = "blogueira OR jornalista burra OR jornalista chata OR jornalista esquerda OR jornalista esquerdista OR jornalista esquerdopata OR jornalista fake OR jornalista feia OR jornalista horrorosa OR jornalista imbecil OR jornalista louca OR jornalista militante OR jornalista puta OR jornalista safada OR jornalista vagabunda -filter:retweets"

# search the last seven days to the current date
now = datetime.now()
dia_hoje = now.strftime("%d")
mes_hoje = now.strftime("%m")
ano_hoje = now.strftime("%Y")
today = ano_hoje + "-" + mes_hoje + "-" + dia_hoje
# 2,000 tweets as a limit
tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="pt",
                   until=today).items(2000)
users_locs = [[tweet.id, tweet.created_at, tweet.source, tweet.geo, tweet.coordinates, tweet.entities, tweet.user, tweet.text] for tweet in tweets]

# transform into initial dataframe and do first cleanups
tweet_text = pd.DataFrame(data=users_locs, 
                    columns=['id', 'created_at', 'source', 'geo', 'coordinates', 'entities', 'user', 'text'])

tweet_text['id'] = tweet_text['id'].apply(str)
tweet_text.rename(columns={'id': 'tweet_id'}, inplace=True)

tweet_text['created_at'] = tweet_text['created_at'].apply(lambda a: pd.to_datetime(a).date())
tweet_text['created_at'].map(lambda x: x.isoformat())

# do the final cleanups and find the information of the authors of the tweets
clean_tweets = []
for num, row in tweet_text.iterrows():
    tweet_id = row['tweet_id']
    created_at = row['created_at']
    source = row['source']
    geo = row['geo']
    coordinates = row['coordinates']
    entities = row['entities']
    user = row['user']
    text = row['text']
    
    try:
        expanded_url = entities['urls'][0]['expanded_url']
    except:
        expanded_url = ""
    author_name = user.name[0:]
    author_screen_name = user.screen_name[0:]
    location = user.location[0:]
    
    dicionario = {"tweet_id": tweet_id, 
                  "created_at": created_at,
                  "source": source,
                  "geo": geo,
                  "coordinates": coordinates,
                  "expanded_url": expanded_url,
                  "author_name": author_name,
                  "author_screen_name": author_screen_name,
                  "location": location,
                  "text": text,
		  "likely_target_of_attack": "journalists"
		  
                 }
    clean_tweets.append(dicionario)
df_clean_tweets1 = pd.DataFrame(clean_tweets)
#df_clean_tweets.info()
#df_clean_tweets.to_excel('test.xlsx',sheet_name='Sheet1',index=False)


# More cases related to environmental activists
new_search = "indígena militante OR ambientalista antipatriota OR ambientalista ladrão OR ambientalista corrupto OR indios mal informados OR índio de butique OR índia de butique OR índio antipatriota OR índia antipatriota OR ambientalista antipatriota  -filter:retweets"

# 2,000 tweets as a limit
tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="pt",
                   until=today).items(2000)
users_locs = [[tweet.id, tweet.created_at, tweet.source, tweet.geo, tweet.coordinates, tweet.entities, tweet.user, tweet.text] for tweet in tweets]

# transform into initial dataframe and do first cleanups
tweet_text_e = pd.DataFrame(data=users_locs, 
                    columns=['id', 'created_at', 'source', 'geo', 'coordinates', 'entities', 'user', 'text'])

tweet_text_e['id'] = tweet_text_e['id'].apply(str)
tweet_text_e.rename(columns={'id': 'tweet_id'}, inplace=True)

tweet_text_e['created_at'] = tweet_text_e['created_at'].apply(lambda a: pd.to_datetime(a).date())
tweet_text_e['created_at'].map(lambda x: x.isoformat())

# do the final cleanups and find the information of the authors of the tweets
clean_tweets = []
for num, row in tweet_text_e.iterrows():
    tweet_id = row['tweet_id']
    created_at = row['created_at']
    source = row['source']
    geo = row['geo']
    coordinates = row['coordinates']
    entities = row['entities']
    user = row['user']
    text = row['text']
    
    try:
        expanded_url = entities['urls'][0]['expanded_url']
    except:
        expanded_url = ""
    author_name = user.name[0:]
    author_screen_name = user.screen_name[0:]
    location = user.location[0:]
    
    dicionario = {"tweet_id": tweet_id, 
                  "created_at": created_at,
                  "source": source,
                  "geo": geo,
                  "coordinates": coordinates,
                  "expanded_url": expanded_url,
                  "author_name": author_name,
                  "author_screen_name": author_screen_name,
                  "location": location,
                  "text": text,
		  "likely_target_of_attack": 'environmental activists'
                 }
    clean_tweets.append(dicionario)
df_clean_tweets2 = pd.DataFrame(clean_tweets)
#df_clean_tweets_e.info()


frames = [df_clean_tweets1, df_clean_tweets2]
df_clean_tweets_portuguese = pd.concat(frames)

df_clean_tweets_portuguese = df_clean_tweets_portuguese.drop_duplicates(
  subset = ['author_name', 'text'],
  keep = 'last').reset_index(drop = True)

df_clean_tweets_portuguese.info()

# Airtable keys
# https://airtable.com/api

AIRTABLE_BASE_ID_P = os.environ["AIRTABLE_BASE_ID_P"]
AIRTABLE_TABLE_NAME = os.environ["AIRTABLE_TABLE_NAME"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]


ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_P}/{AIRTABLE_TABLE_NAME}'

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

# Collects the tweets that are already stored in the Airtable table
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
df_current_data = pd.DataFrame(airtable_rows, index=airtable_index)


# Unites current Tweepy scrape and stored data
# Eliminate duplicate Tweet IDs and ['author_name', 'text']
all_data = pd.merge(df_clean_tweets_portuguese, \
    df_current_data, \
    how = 'left',
    left_on=['author_name','text'], \
    right_on=['author_name','text'])

all_data.info()
all_data = all_data[["coordinates_x", "tweet_id_x", "expanded_url_x", "source_x", "created_at_x", "author_screen_name_x", "author_name", "location_x", "likely_target_of_attack_x", "text", "geo_x"]]

all_data.rename(columns = {'coordinates_x':'coordinates'},inplace = True)
all_data.rename(columns = {'tweet_id_x':'tweet_id'},inplace = True)
all_data.rename(columns = {'expanded_url_x':'expanded_url'},inplace = True)
all_data.rename(columns = {'source_x':'source'},inplace = True)
all_data.rename(columns = {'created_at_x':'created_at'},inplace = True)
all_data.rename(columns = {'author_screen_name_x':'author_screen_name'},inplace = True)
all_data.rename(columns = {'location_x':'location'},inplace = True)
all_data.rename(columns = {'likely_target_of_attack_x':'likely_target_of_attack'},inplace = True)
all_data.rename(columns = {'geo_x':'geo'},inplace = True)

all_data['tweet_id'] = all_data['tweet_id'].str.strip()
#all_data.shape

df_tweets_final = all_data.drop_duplicates(
  subset = ['author_name', 'text'],
  keep = 'last').reset_index(drop = True)

df_tweets_final.info()

# function to add new data to airtable
def add_to_airtable(tweet_id, created_at, source, geo, coordinates, expanded_url, author_name, author_screen_name, location,text, likely_target_of_attack):
	data = {
		"records": [
			{
				"fields": {
					"tweet_id": str(tweet_id),
					"created_at": str(created_at),
					"source": str(source),
					"geo": str(geo),
					"coordinates": str(coordinates),
					"expanded_url": str(expanded_url),
					"author_name": str(author_name),
					"author_screen_name": str(author_screen_name),
					"location": str(location),
					"text": text,
					"likely_target_of_attack": str(likely_target_of_attack)            
					}
				}
			]
		}
	
	data = json.dumps(data, indent=4, sort_keys=False, default=str)
	
	#print(data)
	
	try:
		r = requests.request("POST", ENDPOINT, headers=headers, data=data)
	except requests.exceptions.HTTPError as err:
		raise SystemExit(err)
		
	#print(f"Response status code: {r.status_code}")
	
	#if r.status_code != 200:
	#	print(f"Response status code: {r.status_code}")
	
	return r.status_code 


# test for new data
size = len(df_tweets_final.index)
if size != 0:
	for num, row in df_tweets_final.iterrows():
		tweet_id = row['tweet_id']
		if tweet_id is None or tweet_id == "":
			tweet_id = "nan"
		
		created_at = row['created_at']
		if created_at is None or created_at == "":
			created_at = "nan"
		
		source = row['source']
		if source is None or source == "":
			source = "nan"
				
		geo = row['geo']
		if geo is None or geo == "":
			geo = "nan"
		
		coordinates = row['coordinates']
		if coordinates is None or coordinates == "":
			coordinates = "nan"
			
		expanded_url = row['expanded_url']
		if expanded_url is None or expanded_url == "":
			expanded_url = "nan"
				
		author_name = row['author_name']
		if author_name is None or author_name == "":
			author_name = "nan"
			
		author_screen_name = row['author_screen_name']
		if author_screen_name is None or author_screen_name == "":
			author_screen_name = "nan"	
		
		location = row['location']
		if location is None or location == "":
			location = "nan"	
			
		text = row['text']
		if text is None or text == "":
			text = "nan"	
			
		likely_target_of_attack = row['likely_target_of_attack']
		if likely_target_of_attack is None or likely_target_of_attack == "":
			likely_target_of_attack = "nan"	
		
		add_to_airtable(tweet_id, created_at, source, geo, coordinates, expanded_url, author_name, author_screen_name, location,text,likely_target_of_attack)

    	




# MEXICO


# 1 - search for keywords most likely in Mexico 
# Each search is limited to 500 characters
new_search = "to:AristeguiOnline OR to:aristeguicnn OR to:DeniseDresserG OR to:lumendoz OR to:Fridaguerrera OR to:rynram OR to:CarlosLoret OR to:epigmenioibarra OR periodista tonta OR periodista tonto OR periodista pendeja OR periodista pendejo OR periodista tarada OR periodista tarado OR periodista estúpida OR periodista estupida OR periodista estúpido OR periodista estupido -filter:retweets"


tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="es",
                   until=today).items(2000)
users_locs = [[tweet.id, tweet.created_at, tweet.source, tweet.geo, tweet.coordinates, tweet.entities, tweet.user, tweet.text] for tweet in tweets]

# transform into initial dataframe and do first cleanups
tweet_text_es_1 = pd.DataFrame(data=users_locs, 
                    columns=['id', 'created_at', 'source', 'geo', 'coordinates', 'entities', 'user', 'text'])

size = len(tweet_text_es_1.index)
if size != 0:
    tweet_text_es_1['id'] = tweet_text_es_1['id'].apply(str)
    tweet_text_es_1.rename(columns={'id': 'tweet_id'}, inplace=True)

    tweet_text_es_1['created_at'] = tweet_text_es_1['created_at'].apply(lambda a: pd.to_datetime(a).date())
    tweet_text_es_1['created_at'].map(lambda x: x.isoformat())

    # do the final cleanups and find the information of the authors of the tweets
    clean_tweets = []
    for num, row in tweet_text_es_1.iterrows():
        tweet_id = row['tweet_id']
        created_at = row['created_at']
        source = row['source']
        geo = row['geo']
        coordinates = row['coordinates']
        entities = row['entities']
        user = row['user']
        text = row['text']
    
        try:
            expanded_url = entities['urls'][0]['expanded_url']
        except:
            expanded_url = ""
        author_name = user.name[0:]
        author_screen_name = user.screen_name[0:]
        location = user.location[0:]
    
        dicionario = {"tweet_id": tweet_id, 
                  "created_at": created_at,
                  "source": source,
                  "geo": geo,
                  "coordinates": coordinates,
                  "expanded_url": expanded_url,
                  "author_name": author_name,
                  "author_screen_name": author_screen_name,
                  "location": location,
                  "text": text,
		  "likely_target_of_attack": "journalists"
                 }
        clean_tweets.append(dicionario)
    df_clean_tweets_es_1 = pd.DataFrame(clean_tweets)    
else:
    df_clean_tweets_es_1 = tweet_text_es_2.copy()
#df_clean_tweets_es_1.info()
#df_clean_tweets.to_excel('test.xlsx',sheet_name='Sheet1',index=False)




# 2  
new_search = "periodista bruja OR periodista arpia OR periodista arpía OR periodista burra OR periodista burro OR periodista amargada OR OR periodista amargado OR periodista vieja OR periodista loca OR periodista esta loca OR periodista chiflada OR periodista ridícula OR periodista ridículo OR periodista una perra OR periodista inmunda OR periodista inmundo OR periodista vieja inmunda OR periodista vieja de mierda OR periodista asquerosa OR periodista asqueroso -filter:retweets"


tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="es",
                   until=today).items(2000)
users_locs = [[tweet.id, tweet.created_at, tweet.source, tweet.geo, tweet.coordinates, tweet.entities, tweet.user, tweet.text] for tweet in tweets]

# transform into initial dataframe and do first cleanups
tweet_text_es_2 = pd.DataFrame(data=users_locs, 
                    columns=['id', 'created_at', 'source', 'geo', 'coordinates', 'entities', 'user', 'text'])

size = len(tweet_text_es_2.index)
if size != 0:
    tweet_text_es_2['id'] = tweet_text_es_2['id'].apply(str)
    tweet_text_es_2.rename(columns={'id': 'tweet_id'}, inplace=True)

    tweet_text_es_2['created_at'] = tweet_text_es_2['created_at'].apply(lambda a: pd.to_datetime(a).date())
    tweet_text_es_2['created_at'].map(lambda x: x.isoformat())

    # do the final cleanups and find the information of the authors of the tweets
    clean_tweets = []
    for num, row in tweet_text_es_2.iterrows():
        tweet_id = row['tweet_id']
        created_at = row['created_at']
        source = row['source']
        geo = row['geo']
        coordinates = row['coordinates']
        entities = row['entities']
        user = row['user']
        text = row['text']
    
        try:
            expanded_url = entities['urls'][0]['expanded_url']
        except:
            expanded_url = ""
        author_name = user.name[0:]
        author_screen_name = user.screen_name[0:]
        location = user.location[0:]
    
        dicionario = {"tweet_id": tweet_id, 
                  "created_at": created_at,
                  "source": source,
                  "geo": geo,
                  "coordinates": coordinates,
                  "expanded_url": expanded_url,
                  "author_name": author_name,
                  "author_screen_name": author_screen_name,
                  "location": location,
                  "text": text,
		  "likely_target_of_attack": "journalists"
                 }
        clean_tweets.append(dicionario)

    df_clean_tweets_es_2 = pd.DataFrame(clean_tweets)    
else:
    df_clean_tweets_es_2 = tweet_text_es_2.copy()



# 3 
new_search = "periodista ve a lavar platos OR periodista mamadora OR periodista zorra OR periodista rubia tarada OR periodista cabrona OR periodista embaucadora OR periodista ladrona OR periodista ladron OR periodista ladrón OR periodista hija de perra OR periodista hija de puta OR periodista hijo de perra OR periodista hijo de puta OR periodista lambiscona OR periodista naca OR periodista lamebotas OR periodista arrastrada OR periodista luchona -filter:retweets"


tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="es",
                   until=today).items(2000)
users_locs = [[tweet.id, tweet.created_at, tweet.source, tweet.geo, tweet.coordinates, tweet.entities, tweet.user, tweet.text] for tweet in tweets]

# transform into initial dataframe and do first cleanups
tweet_text_es_3 = pd.DataFrame(data=users_locs, 
                    columns=['id', 'created_at', 'source', 'geo', 'coordinates', 'entities', 'user', 'text'])

size = len(tweet_text_es_3.index)
if size != 0:
    tweet_text_es_3['id'] = tweet_text_es_3['id'].apply(str)
    tweet_text_es_3.rename(columns={'id': 'tweet_id'}, inplace=True)

    tweet_text_es_3['created_at'] = tweet_text_es_3['created_at'].apply(lambda a: pd.to_datetime(a).date())
    tweet_text_es_3['created_at'].map(lambda x: x.isoformat())

    # do the final cleanups and find the information of the authors of the tweets
    clean_tweets = []
    for num, row in tweet_text_es_3.iterrows():
        tweet_id = row['tweet_id']
        created_at = row['created_at']
        source = row['source']
        geo = row['geo']
        coordinates = row['coordinates']
        entities = row['entities']
        user = row['user']
        text = row['text']
    
        try:
            expanded_url = entities['urls'][0]['expanded_url']
        except:
            expanded_url = ""
        author_name = user.name[0:]
        author_screen_name = user.screen_name[0:]
        location = user.location[0:]
    
        dicionario = {"tweet_id": tweet_id, 
                  "created_at": created_at,
                  "source": source,
                  "geo": geo,
                  "coordinates": coordinates,
                  "expanded_url": expanded_url,
                  "author_name": author_name,
                  "author_screen_name": author_screen_name,
                  "location": location,
                  "text": text,
		  "likely_target_of_attack": "journalists"
                 }
        clean_tweets.append(dicionario)

    df_clean_tweets_es_3 = pd.DataFrame(clean_tweets)    
else:
    df_clean_tweets_es_3 = tweet_text_es_3.copy()




# 4
new_search = "periodista pinche gata OR periodista cerda OR periodista marrana OR periodista simia OR periodista vieja fea OR periodista vieja gorda OR periodista gorda OR periodista machorra OR periodista marimacha OR periodista tortillera OR periodista travesti OR periodista desviada OR periodista negra asquerosa OR periodista negra de mierda OR periodista pinche negra OR periodista india OR periodista prieta OR periodista negro de mierda -filter:retweets"


tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="es",
                   until=today).items(2000)
users_locs = [[tweet.id, tweet.created_at, tweet.source, tweet.geo, tweet.coordinates, tweet.entities, tweet.user, tweet.text] for tweet in tweets]

# transform into initial dataframe and do first cleanups
tweet_text_es_4 = pd.DataFrame(data=users_locs, 
                    columns=['id', 'created_at', 'source', 'geo', 'coordinates', 'entities', 'user', 'text'])

size = len(tweet_text_es_4.index)
if size != 0:
    tweet_text_es_4['id'] = tweet_text_es_4['id'].apply(str)
    tweet_text_es_4.rename(columns={'id': 'tweet_id'}, inplace=True)

    tweet_text_es_4['created_at'] = tweet_text_es_4['created_at'].apply(lambda a: pd.to_datetime(a).date())
    tweet_text_es_4['created_at'].map(lambda x: x.isoformat())

    # do the final cleanups and find the information of the authors of the tweets
    clean_tweets = []
    for num, row in tweet_text_es_4.iterrows():
        tweet_id = row['tweet_id']
        created_at = row['created_at']
        source = row['source']
        geo = row['geo']
        coordinates = row['coordinates']
        entities = row['entities']
        user = row['user']
        text = row['text']
    
        try:
            expanded_url = entities['urls'][0]['expanded_url']
        except:
            expanded_url = ""
        author_name = user.name[0:]
        author_screen_name = user.screen_name[0:]
        location = user.location[0:]
    
        dicionario = {"tweet_id": tweet_id, 
                  "created_at": created_at,
                  "source": source,
                  "geo": geo,
                  "coordinates": coordinates,
                  "expanded_url": expanded_url,
                  "author_name": author_name,
                  "author_screen_name": author_screen_name,
                  "location": location,
                  "text": text,
		  "likely_target_of_attack": "journalists"
                 }
        clean_tweets.append(dicionario)

    df_clean_tweets_es_4 = pd.DataFrame(clean_tweets)    
else:
    df_clean_tweets_es_4 = tweet_text_es_4.copy()




# 5
new_search = "periodista comunista asquerosa OR periodista feminazi OR periodista abortera OR  periodista comunista asqueroso OR periodista drogadicta OR periodista vagabunda OR periodista cocainomana OR periodista mariguanera OR periodista marihuanera OR periodista drogadicto OR periodista vagabundo OR periodista cocainomano OR periodista mariguanero OR periodista marihuanero -filter:retweets"


tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="es",
                   until=today).items(2000)
users_locs = [[tweet.id, tweet.created_at, tweet.source, tweet.geo, tweet.coordinates, tweet.entities, tweet.user, tweet.text] for tweet in tweets]

# transform into initial dataframe and do first cleanups
tweet_text_es_5 = pd.DataFrame(data=users_locs, 
                    columns=['id', 'created_at', 'source', 'geo', 'coordinates', 'entities', 'user', 'text'])

size = len(tweet_text_es_5.index)
if size != 0:
    tweet_text_es_5['id'] = tweet_text_es_5['id'].apply(str)
    tweet_text_es_5.rename(columns={'id': 'tweet_id'}, inplace=True)

    tweet_text_es_5['created_at'] = tweet_text_es_5['created_at'].apply(lambda a: pd.to_datetime(a).date())
    tweet_text_es_5['created_at'].map(lambda x: x.isoformat())

    # do the final cleanups and find the information of the authors of the tweets
    clean_tweets = []
    for num, row in tweet_text_es_5.iterrows():
        tweet_id = row['tweet_id']
        created_at = row['created_at']
        source = row['source']
        geo = row['geo']
        coordinates = row['coordinates']
        entities = row['entities']
        user = row['user']
        text = row['text']
    
        try:
            expanded_url = entities['urls'][0]['expanded_url']
        except:
            expanded_url = ""
        author_name = user.name[0:]
        author_screen_name = user.screen_name[0:]
        location = user.location[0:]
    
        dicionario = {"tweet_id": tweet_id, 
                  "created_at": created_at,
                  "source": source,
                  "geo": geo,
                  "coordinates": coordinates,
                  "expanded_url": expanded_url,
                  "author_name": author_name,
                  "author_screen_name": author_screen_name,
                  "location": location,
                  "text": text,
		  "likely_target_of_attack": "journalists"
                 }
        clean_tweets.append(dicionario)

    df_clean_tweets_es_5 = pd.DataFrame(clean_tweets)    
else:
    df_clean_tweets_es_5 = tweet_text_es_5.copy()




# 6
new_search = "to:BuenMadrazo OR to:CEMDA OR to:tiburon_pepe OR to:PabloMontanoB OR to:sikuaa OR ambientalista tonta OR ambientalista pendeja OR ambientalista tarada OR ambientalista estúpida OR ambientalista estupida OR activista tonta OR activista pendeja OR activista tarada OR activista estúpida OR activista estupida  OR indio tonto OR indio pendejo OR indio tarado OR indio estúpido OR indio estupido OR india estúpida OR india estupida -filter:retweets"


tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="es",
                   until=today).items(2000)
users_locs = [[tweet.id, tweet.created_at, tweet.source, tweet.geo, tweet.coordinates, tweet.entities, tweet.user, tweet.text] for tweet in tweets]

# transform into initial dataframe and do first cleanups
tweet_text_es_6 = pd.DataFrame(data=users_locs, 
                    columns=['id', 'created_at', 'source', 'geo', 'coordinates', 'entities', 'user', 'text'])

size = len(tweet_text_es_6.index)
if size != 0:
    tweet_text_es_6['id'] = tweet_text_es_6['id'].apply(str)
    tweet_text_es_6.rename(columns={'id': 'tweet_id'}, inplace=True)

    tweet_text_es_6['created_at'] = tweet_text_es_6['created_at'].apply(lambda a: pd.to_datetime(a).date())
    tweet_text_es_6['created_at'].map(lambda x: x.isoformat())

    # do the final cleanups and find the information of the authors of the tweets
    clean_tweets = []
    for num, row in tweet_text_es_6.iterrows():
        tweet_id = row['tweet_id']
        created_at = row['created_at']
        source = row['source']
        geo = row['geo']
        coordinates = row['coordinates']
        entities = row['entities']
        user = row['user']
        text = row['text']
    
        try:
            expanded_url = entities['urls'][0]['expanded_url']
        except:
            expanded_url = ""
        author_name = user.name[0:]
        author_screen_name = user.screen_name[0:]
        location = user.location[0:]
    
        dicionario = {"tweet_id": tweet_id, 
                  "created_at": created_at,
                  "source": source,
                  "geo": geo,
                  "coordinates": coordinates,
                  "expanded_url": expanded_url,
                  "author_name": author_name,
                  "author_screen_name": author_screen_name,
                  "location": location,
                  "text": text,
		  "likely_target_of_attack": "environmental activists"
                 }
        clean_tweets.append(dicionario)

    df_clean_tweets_es_6 = pd.DataFrame(clean_tweets)    
else:
    df_clean_tweets_es_6 = tweet_text_es_6.copy()

#df_clean_tweets_es_6.info()


frames = [df_clean_tweets_es_1, df_clean_tweets_es_2, df_clean_tweets_es_3, df_clean_tweets_es_4, df_clean_tweets_es_5, df_clean_tweets_es_6]
df_clean_tweets_spanish = pd.concat(frames)

df_clean_tweets_spanish = df_clean_tweets_spanish.drop_duplicates(
  subset = ['author_name', 'text'],
  keep = 'last').reset_index(drop = True)

#df_clean_tweets_spanish.info()



# Airtable keys
# https://airtable.com/api

AIRTABLE_BASE_ID_E = os.environ["AIRTABLE_BASE_ID_E"]
AIRTABLE_TABLE_NAME = os.environ["AIRTABLE_TABLE_NAME"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]


ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_E}/{AIRTABLE_TABLE_NAME}'


# Collects the tweets that are already stored in the Airtable table
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
df_current_data = pd.DataFrame(airtable_rows, index=airtable_index)

# Unites current Tweepy scrape and stored data
# Eliminate duplicate Tweet IDs and ['author_name', 'text']
all_data = pd.merge(df_clean_tweets_spanish, \
    df_current_data, \
    how = 'left',
    left_on=['author_name','text'], \
    right_on=['author_name','text'])

all_data = all_data[["coordinates_x", "tweet_id_x", "expanded_url_x", "source_x", "created_at_x", "author_screen_name_x", "author_name", "location_x", "likely_target_of_attack_x", "text", "geo_x"]]

all_data.rename(columns = {'coordinates_x':'coordinates'},inplace = True)
all_data.rename(columns = {'tweet_id_x':'tweet_id'},inplace = True)
all_data.rename(columns = {'expanded_url_x':'expanded_url'},inplace = True)
all_data.rename(columns = {'source_x':'source'},inplace = True)
all_data.rename(columns = {'created_at_x':'created_at'},inplace = True)
all_data.rename(columns = {'author_screen_name_x':'author_screen_name'},inplace = True)
all_data.rename(columns = {'location_x':'location'},inplace = True)
all_data.rename(columns = {'likely_target_of_attack_x':'likely_target_of_attack'},inplace = True)
all_data.rename(columns = {'geo_x':'geo'},inplace = True)

all_data['tweet_id'] = all_data['tweet_id'].str.strip()
#all_data.shape

df_tweets_final_es = all_data.drop_duplicates(
  subset = ['author_name', 'text'],
  keep = 'last').reset_index(drop = True)

df_tweets_final_es.info()



# test for new data
size = len(df_tweets_final_es.index)
if size != 0:
	for num, row in df_tweets_final_es.iterrows():
		tweet_id = row['tweet_id']
		created_at = row['created_at']
		source = row['source']
		geo = row['geo']
		coordinates = row['coordinates']
		expanded_url = row['expanded_url']
		author_name = row['author_name']
		author_screen_name = row['author_screen_name']
		location = row['location']
		text = row['text']
		likely_target_of_attack = row['likely_target_of_attack']
		
		add_to_airtable(tweet_id, created_at, source, geo, coordinates, expanded_url, author_name, author_screen_name, location,text, likely_target_of_attack)
