# Sample starter script for cleaning up tweets

import pandas as pd
import re

tweets = pd.read_csv('tweets_in_general_user_mfriasoficial.csv', encoding ='utf-8', dtype = 'str', sep = ',')
tweets.info()

# copy from lowercase text column
tweets['text_copy'] = tweets['text'].str.lower()
tweets[['text', 'text_copy']].sample(5)

# remove emojis
def remove_emoji(rowline):
    resultado = str(rowline["text_copy"]).strip()
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', resultado)

tweets["text_copy"] = tweets.apply(remove_emoji, axis=1)

# eliminate repeated text_copy
tweets = tweets.drop_duplicates(subset=["text_copy"], keep=False)
tweets.shape

# remove html tags
def remove_tags(string):
    result = re.sub('<.*?>','',string)
    return result

tweets['text_copy']=tweets['text_copy'].apply(lambda cw : remove_tags(cw))

# Separate tweets only longer than 10 characters
# tweets = tweets.loc[tweets['text_copy'].str.len() > 10]

# Separate only tweets with at least three words
count = tweets['text_copy'].str.split().str.len()
tweets = tweets[(count>=3)]
tweets.shape

tweets_to_save = tweets[['id',
'author_id',
'created_at', 
'text', 
'text_copy',
'entities.mentions',
'entities.urls',
'context_annotations', 
'public_metrics.like_count', 
'public_metrics.quote_count', 
'public_metrics.reply_count', 
'public_metrics.retweet_count', 
'possibly_sensitive']]
tweets_to_save.to_excel('tweets_in_general_user_mfriasoficial_clean.xlsx',sheet_name='Sheet1',index=False)
