# -*- coding: utf-8
# Reinaldo Chaves (reinaldo@abraji.org.br)
# Script for the website https://attackdetector.herokuapp.com/
# It's an app deployable on Heroku, using config vars
#

import dash 
from dash.dependencies import Input, Output
from dash import dash_table
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import requests
import plotly.express as px
import plotly.graph_objects as go
from dash import html
import os

app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)

## BRAZIL
# Airtable keys
# https://airtable.com/api

AIRTABLE_BASE_ID_P = os.environ["AIRTABLE_BASE_ID_port_rated"]
AIRTABLE_TABLE_NAME = os.environ["AIRTABLE_TABLE_NAME_rated"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]

ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_P}/{AIRTABLE_TABLE_NAME}'

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

# Collects the tweets that are already stored in the Airtable table - Portuguese - Brazil
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


df_current_data_p['id'] = df_current_data_p['author_name']
df_current_data_p.set_index('id', inplace=True, drop=False)
#print(df_current_data_p.columns)

# Filter BERT model ratings >= to 0.8
df_current_data_p['probability_of_being_an_attack'] = df_current_data_p['probability_of_being_an_attack'].astype(float)
df_current_data_p = df_current_data_p[df_current_data_p['probability_of_being_an_attack'] >= 0.8]

size_p = len(df_current_data_p.index)


conta_tipos_p = df_current_data_p.groupby(['author_name'])['tweet_id'].count().sort_values(ascending=False).reset_index()
conta_tipos_p.columns = ['top_authors_of_tweets', 'total_of_posts_found']

conta_tipos_p = conta_tipos_p.head(10)

figura1 = go.Figure([go.Bar(x = conta_tipos_p['top_authors_of_tweets'], y = conta_tipos_p['total_of_posts_found'], marker_color = 'yellow')])

figura1.update_layout(title = 'See top 10 tweeters in Brazil - or more mentioned',
                  xaxis_title = 'Top authors of tweets',
                  yaxis_title = 'Total of posts found'
                  )





# MEXICO
# Airtable keys s
# https://airtable.com/api


AIRTABLE_BASE_ID_E = os.environ["AIRTABLE_BASE_ID_spa_rated"]

ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID_E}/{AIRTABLE_TABLE_NAME}'


# Collects the tweets that are already stored in the Airtable table - Portuguese - Mexico
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
df_current_data_e = pd.DataFrame(airtable_rows, index=airtable_index)

df_current_data_e.info()


df_current_data_e['id'] = df_current_data_e['author_name']
df_current_data_e.set_index('id', inplace=True, drop=False)
#print(df_current_data_e.columns)

# Filter BERT model ratings greater than or equal to 0.8
df_current_data_e['probability_of_being_an_attack'] = df_current_data_e['probability_of_being_an_attack'].astype(float)
df_current_data_e = df_current_data_e[df_current_data_e['probability_of_being_an_attack'] >= 0.8]

size_e = len(df_current_data_e.index)


conta_tipos_e = df_current_data_e.groupby(['author_name'])['tweet_id'].count().sort_values(ascending=False).reset_index()
conta_tipos_e.columns = ['top_authors_of_tweets', 'total_of_posts_found']

conta_tipos_e = conta_tipos_e.head(10)

figura2 = go.Figure([go.Bar(x = conta_tipos_e['top_authors_of_tweets'], y = conta_tipos_p['total_of_posts_found'], marker_color = 'green')])

figura2.update_layout(title = 'See top 10 tweeters in Mexico - or more mentioned',
                  xaxis_title = 'Top authors of tweets',
                  yaxis_title = 'Total of posts found'
                  )




app.title = 'Project Attack Detector'
server = app.server

PLOTLY_LOGO1 = "https://www.portaldosjornalistas.com.br/wp-content/uploads/2019/09/Abraji.png"
PLOTLY_LOGO2 = "https://venenoenmiagua.datacritica.org/static/logo-data_critica_black.9e1abca7.svg"


#df_table_e = df_current_data_e[['text', 'created_at', 'author_screen_name']]
#df_table_p = df_current_data_p[['text', 'created_at', 'author_screen_name']]

navbar = dbc.Navbar(
        [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = PLOTLY_LOGO1, height = "70px"), ),
                        dbc.Col(html.Img(src = PLOTLY_LOGO2, height = "70px"), ),
                        
                        dbc.Col(
             dbc.NavbarBrand("Hate tweets against journalists - Brazil and Mexico - beta version", style = {'color':'black', 'fontSize':'25px','fontFamily':'Times New Roman'}
                            ),
             ),

                    ],
                    align="center",
                    className="g-10",
                ),
            
            dbc.Row(
            [
        dbc.Col(
        dbc.Button(id = 'button', children = "Get to know JournalismAI", color = "primary",  href = 'https://www.lse.ac.uk/media-and-communications/polis/JournalismAI'), 
            )        
    ],
            
     className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)
            
         ],
)

html.Br()
html.Br()


# -------------------------------------------------------------------------------------------------

size_p = str(size_p)
size_e = str(size_e)

card_content1 = [
    dbc.CardHeader("Brazil"),
    
    dbc.CardBody(
        [
            html.H5(size_p, className = "card-title"),
            
            html.P("This is the current number of hateful tweets our machine learning model has found so far - ratings >= to 0.8",
                   className = "card-text")
            
            
            ]
               
        )  
    ]

card_content2 = [
    dbc.CardHeader("Mexico"),
    
    dbc.CardBody(
        [
            html.H5(size_e, className = "card-title"),
            
            html.P("This is the current number of hateful tweets our machine learning model has found so far - ratings >= to 0.8",
                   className = "card-text")
            
            
            ]
               
        )  
    ]
# --------------------------------------------------------------------------------------


body_app = dbc.Container([
                 
        html.Br(),
    
        dbc.Row([
        html.Div(id = 'link_div',
                 children = [html.A(id = 'text1', children = 'Our project is about hate speech against journalists and environmental activists in Brazil and Mexico. The context of digital and coordinated hate attacks has a worldwide political importance today, influencing elections, public discussions and affecting the reputation of thousands of people. See more about our project, including the scripts, in this repository on ', style = {'fontSize':15}),
                             html.A(id = 'text2', children = 'Github', href = 'https://github.com/JournalismAI/attackdetector', style = {'fontSize':15})
                             
                            ],
                 style = {'textAlign':'center'})
            ]),
    
    
        html.Br(),

        dbc.Row([
        dbc.Col(dbc.Card(card_content1, color = "info", inverse = True)),
        dbc.Col(dbc.Card(card_content2, color = 'info', inverse = True))        
            ]),

        html.Br(),
        
        dbc.Row( html.Marquee("Information is updated daily at 12:00 AM UTC"), style = {'color':'green'}),

        html.Br(),
        html.Br(),

        
        dbc.Row([html.Div(html.H4('See the Twitter users (or more mentioned) with the most hateful posts in Brazil against journalists or environmental activists (data collected since October 2022)'),
                      style = {'textAlign':'center','fontWeight':'bold','family':'georgia','width':'100%'})]),

        html.Br(),
        html.Br(),
        
        dbc.Row([dbc.Col(dcc.Graph(id = 'graph-haters_b', figure = figura1), style = {'height':'450px'},xs = 12, sm = 12, md = 6, lg = 6, xl = 6),
                 dbc.Col(dcc.Graph(id = 'graph-haters_m', figure = figura2), style = {'height':'450px'},xs = 12, sm = 12, md = 6, lg = 6, xl = 6)
             ]),
  
        html.Br(),
        html.Br(),

        html.H5(id = 'H51', children = 'View and search tweets from Mexico (use "Hide Fields" to select your preferred columns) - all ratings', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        html.Iframe(src="https://airtable.com/embed/shr3Oa34SwJ45MF5E?backgroundColor=purple&viewControls=on",
                style={"height": "533px", "width": "100%"}),
     
        html.Br(),
        html.Br(),

        html.H5(id = 'H52', children = 'View and search tweets from Brazil (use "Hide Fields" to select your preferred columns) - all ratings', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        html.Iframe(src="https://airtable.com/embed/shrufoWmGOCM8vlM2?backgroundColor=purple&viewControls=on",
                style={"height": "533px", "width": "100%"}),
          


        html.Br(),
        html.Br(),
    
        html.H6(id = 'H53', children = 'More about the project', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
        html.Br(),
        dbc.Row([
        html.Div(id = 'link_div2',
                 children = [html.A(id = 'text3', children = 'This project is part of the ', style = {'fontSize':15}),
                             html.A(id = 'text4', children = '2022 JournalismAI Fellowship Programme', href = 'https://www.lse.ac.uk/media-and-communications/polis/JournalismAI/Fellowship-Programme', style = {'fontSize':15}),
                             html.A(id = 'text5', children = '. The Fellowship brought together 46 journalists and technologists from across the world to collaboratively explore innovative solutions to improve journalism via the use of AI technologies. You can explore all the Fellowship projects ', style = {'fontSize':15}),
                             html.A(id = 'text6', children = 'at this link.', href = 'https://www.lse.ac.uk/media-and-communications/polis/JournalismAI/Fellowship-Programme', style = {'fontSize':15})
                             
                            ],
                 style = {'textAlign':'center'})
            ]),
    
        html.Br(),

        dbc.Row([
        html.Div(id = 'link_div3',
                 children = [html.A(id = 'text7', children = 'The project was developed as a collaboration between ', style = {'fontSize':15}),
                             html.A(id = 'text8', children = 'Abraji', href = 'https://www.abraji.org.br/', style = {'fontSize':15}),
                             html.A(id = 'text9', children = ' and ', style = {'fontSize':15}),
                             html.A(id = 'text10', children = 'Data Crítica', href = 'https://datacritica.org/', style = {'fontSize':15}),
                             html.A(id = 'text11', children = '. The fellows who contributed to the project are: Reinaldo Chaves (Project Coordinator-Abraji), Schirlei Alves (Data Journalist-Abraji), Fernanda Aguirre (Data Analyst & Researcher-Data Crítica) and Gibran Mena (Co-founder & Director-Data Crítica).', style = {'fontSize':15})
                             
                            ],
                 style = {'textAlign':'center'})
            ]),
    
        html.Br(),
    
        dbc.Row([
        html.Div(id = 'link_div4',
                 children = [html.A(id = 'text12', children = 'JournalismAI is a project of Polis – the journalism think-tank at the London School of Economics and Political Science – and it’s sponsored by the Google News Initiative. If you want to know more about the Fellowship and the other JournalismAI activities, ', style = {'fontSize':15}),
                             html.A(id = 'text13', children = 'sign up for the newsletter', href = 'https://mailchi.mp/lse.ac.uk/journalismai', style = {'fontSize':15}),
                             html.A(id = 'text14', children = ' or get in touch with the team via ', style = {'fontSize':15}),
                             html.A(id = 'text15', children = 'hello@journalismai.info', href = 'mailto:hello@journalismai.info', style = {'fontSize':15})
                             
                            ],
                 style = {'textAlign':'center'})
            ]),
    
        html.Br(),
    
        dbc.Row([
        html.Div(id = 'link_div5',
                 children = [html.A(id = 'text16', children = 'Contact us - If you want to collaborate or just to know more about the project, please reach out to us: ', style = {'fontSize':15}),
                             html.A(id = 'text17', children = 'reinaldo@abraji.org.br', href = 'mailto:reinaldo@abraji.org.br', style = {'fontSize':15}),
                             html.A(id = 'text18', children = ' or ', style = {'fontSize':15}),
                             html.A(id = 'text19', children = 'faguirre@datacritica.org', href = 'mailto:faguirre@datacritica.org', style = {'fontSize':15})
                             
                            ],
                 style = {'textAlign':'center'})
            ]),
    
         html.Br(),

         ],fluid = True)



app.layout = html.Div(id = 'parent', children = [navbar, body_app])




if __name__ == "__main__":
    app.run_server()
