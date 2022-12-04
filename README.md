# Attack Detector

This project is part of the [2022 JournalismAI Fellowship Programme](https://www.lse.ac.uk/media-and-communications/polis/JournalismAI/Fellowship-Programme). The Fellowship brought together 46 journalists and technologists from across the world to collaboratively explore innovative solutions to improve journalism via the use of AI technologies. You can explore all the Fellowship projects [at this link](https://www.lse.ac.uk/media-and-communications/polis/JournalismAI/Fellowship-Programme).

The project was developed as a collaboration between *[Abraji](https://www.abraji.org.br/)* and *[Data Crítica](https://datacritica.org/)*. The fellows who contributed to the project are: *[Reinaldo Chaves](https://twitter.com/paidatocandeira) (Project Coordinator-Abraji), [Schirlei Alves](https://twitter.com/schirlei_alves) (Data Journalist-Abraji), [Fernanda Aguirre](https://twitter.com/feragru) (Data Analyst & Researcher-Data Crítica) and [Gibran Mena](https://twitter.com/gibsteria) (Co-founder & Director-Data Crítica)*.

[JournalismAI](https://www.lse.ac.uk/media-and-communications/polis/JournalismAI) is a project of [Polis](https://www.lse.ac.uk/media-and-communications/polis) – the journalism think-tank at the London School of Economics and Political Science – and it’s sponsored by the [Google News Initiative](https://newsinitiative.withgoogle.com/). If you want to know more about the Fellowship and the other JournalismAI activities, [sign up for the newsletter](https://mailchi.mp/lse.ac.uk/journalismai) or get in touch with the team via hello@journalismai.info

---

## Contents

- [Introduction](#introduction)
- [Methodology](#methodology)
- [Data](#data)
- [Automation](#automation)
- [Labelling](#labelling)
- [Pre-trained models](#pre-trained-models)
- [Topic modeling](#topic-modeling)
- [Future work](#future-work)
- [Contact us](#contact-us)

---

## Introduction

The motivation for this project is the rampant situation of violence against journalists in our countries. Between January and April 2022, Abraji identified 151 episodes of physical and verbal aggressions against journalists in Brazil (62.9% originated on the internet). This year, 2022, Brazil had an extremely polarized election in October and, since October 30, when the election result was given, until November, 64 episodes involving physical aggression, death threats, expulsion of teams from public places were recorded.

In Mexico, from 2000 to date, the journalist protection organization [Artículo 19](https://articulo19.org/) has documented 156 murders of journalists. 47 happened during the administration of former President Enrique Peña Nieto and 36 under current President Andrés Manuel López Obrador. 

In the 2021 [World Press Freedom Index](https://rsf.org/en/2021-world-press-freedom-index-journalism-vaccine-against-disinformation-blocked-more-130-countries), Reporters Without Borders places Brazil and Mexico on the list of countries where journalism is very risky – 111th and 143rd respectively – out of 180 countries. They share the “bad” classification with India (142nd) and Russia (at 150th), among others.

Another example, in 2021, the Voces del Sur (VdS) Network recorded 4,930 alerts of violations of freedom of expression, freedom of the press, and the right of access to information in 14 countries in Latin America. This [report](https://vocesdelsurunidas.org/wp-content/uploads/2022/11/SHADOW-REPORT-2021.pdf) in English details the situation in Mexico, Brazil and other Latin American countries.

And this type of harassment and online attacks against journalists happens in the same way against environmental activists - another focus of our project. These people suffer intimidation, defamation and persecution for defending areas under environmental degradation in Brazil and Mexico.

Digital violence is known to have serious consequences for the psychological health of journalists and land defender activists. The defender Samir Flores Soberanes was murdered in Mexico after being vilified by the Mexican government for his opposition to the Morelos Integral Project. The defender Bruno Pereira was also recently murdered along with journalist Dom Phillips in an investigation in the Yavari Valley in Brazil.

It is essential to analyse online attacks to understand how they work, who initiates them, who shares these messages, and what forms the attacks take. For example, it is important to understand whether they are misogynistic, racist, or a combination of various forms of hate speech.

*Who whe are*

Abraji (Brazilian Association of Investigative Journalism) is an NGO that has projects to improve investigative journalism in Brazil, and that involve data science, freedom of expression, transparency and advocacy

Data Crítica It is a collective of journalists and developers that uses data analysis and visualization, programming languages, and network science to investigate critical issues: the environment, and racial, economic, and gender-based power imbalances.


---

## Methodology
Our project is about hate speech against journalists and environmental activists in Brazil and Mexico. The context of digital and coordinated hate attacks has a worldwide political importance today, influencing elections, public discussions and affecting the reputation of thousands of people. Let's show a little of the situation in Mexico and Brazil that shaped our project

Data Critica and Abraji have works on digital aggression against journalists and environmental activists, as this restricts freedom of expression and affects the work of these professionals

So using AI methods seemed like a way to improve our work and then, making this work public could help other professionals and the debate about digital attacks in our countries

This type of digital intimidation has also been used in many countries to weaken democracies and increase the power of populist leaders. So we imagine that our work can also be used and improved in other nations.

In the creation of our project we realized some problems and opportunities that this brought to solve

Problem:
+ Our project is about hate speech against journalists and environmental activists in Brazil and Mexico. And there is a risk context under which journalists and environmental activists carry out their work 
+ And Online attacks are a form of coercion and silencing that can bypass the digital world 
+ For example, the presidents of Mexico and Brazil use disqualifying the work of journalists as a tactic
+ Mexico and Brazil, according to human rights and journalism organizations, have thousands of cases of digital harassment in recent years, which end up stimulating other problems, such as judicial harassment, physical aggression and other violence against these people

And about the opportunities: 
+ Using machine learning and NLP to find these digital assaults could make it faster to detect coordinated attacks against journalists and environmental activists
+ These tools can help to more easily detect entities, subjects and keywords of these attacks, as well as their authors
+ This work could help the tasks of investigative journalists and researchers who study hate speech and its impact on freedom of expression and democracy
+ And also collaborate with advocacy actions and protection projects against digital attacks

Our project had some changes along the way. Certain points were given more priority and others we realized that we would not have time to implement this year. And we also thought that a website with an automated database and its respective visualizations would be the best way to show the statistical machine learning model that we have improved in these months

So, in summary, these were the main steps that we took:

<b>Step 1</b>

Was very important for us to better understand the problem of hate speech data, to map main victims, perpetrators of attacks, most used keywords, and how to work with this data using data science. We also spoke with researchers from Google and AWS, two companies that have created analytical and commercial tools just for hate speech in several languages, due to the relevance of this problem in the world. And we also had a lot of contact with the programmers at RockingData, an Argentinian start-up specializing in data science and artificial intelligence, who helped us a lot with our model.

<b>Step 2</b>

We learned more about extracting data on social networks - see below

<b>Step 3</b>

We face the possibilities for automation and project infrastructure - see bellow

<b>Step 4</b>

And in step 4, we tested about 10 thousand tweets in Portuguese and Spanish with different models in BERT for sentiment analysis - with training and validation database. BERT is an open source machine learning framework for natural language processing (NLP). BERT is designed to help computers understand the meaning of ambiguous language in text by using surrounding text to establish context. See bellow more details


---

## Data
About the data we use in the project. We decided to include only the hate speech disseminated by Twitter posts, because it is a social network with an [API](https://developer.twitter.com/en/docs/twitter-api), it is very widely used for this purpose in Mexico and Brazil, and we would not have time to implement other social media in time. 

We requested the [Twitter academic account](https://developer.twitter.com/en/products/twitter-api/academic-research) that allows a larger extraction, of up to 10M per month, and we learned the commands to use and to build queries in two projects that use the Twitter API: [Twarc](https://twarc-project.readthedocs.io/en/latest/twarc2_en_us/) and [Tweepy](https://docs.tweepy.org/en/stable/)

Example query in Twarc - collecting data via terminal:
- Research and interviews to get the most offensive Portuguese keywords in Brazil against journalists: 
blogueira OR jornalista burra OR  jornalista chata OR jornalista esquerda OR jornalista esquerdista OR jornalista esquerdopata OR jornalista fake OR jornalista feia OR jornalista horrorosa OR jornalista imbecil OR jornalista louca OR jornalista militante OR jornalista puta OR jornalista safada OR jornalista vagabunda OR jornazista

- Construction of a querie in twarc2 (in the academic API) to enter these profiles and search for these keywords, in pt, without retweet, in the year 2022, with a limit of 10,000 tweets, including archived tweets, and creating the results.jsonl

*twarc2 search "(from:Rconstantino OR from:brom_elisa OR from:mfriasoficial OR from:taoquei1 OR from:BolsonaroSP OR from:CarlosBolsonaro blogueira OR jornalista burra OR  jornalista chata OR jornalista esquerda OR jornalista esquerdista OR jornalista esquerdopata OR jornalista fake OR jornalista feia OR jornalista horrorosa OR jornalista imbecil OR jornalista louca OR jornalista militante OR jornalista puta OR jornalista safada OR jornalista vagabunda OR jornazista) lang:pt -is:retweet"  --start-time 2022-01-01 --end-time 2022-08-14 --limit 10000 --archive results.jsonl*

Example to Spanish tweets about environmental activists:

*twarc2 search "(to:BuenMadrazo OR to:CEMDA OR to:tiburon_pepe OR to:PabloMontanoB OR to:sikuaa OR ambientalista tonta OR ambientalista pendeja OR ambientalista tarada OR ambientalista estúpida OR ambientalista estupida OR activista tonta OR activista pendeja OR activista tarada OR activista estúpida OR activista estupida  OR indio tonto OR indio pendejo OR indio tarado OR indio estúpido OR indio estupido OR india estúpida OR india estupida) lang:es -is:retweet"  --start-time 2022-09-01 --end-time 2022-10-30 --limit 2000 --archive results.jsonl*

After, transform into a CSV

twarc2 csv results.jsonl tweets_with_attacks_journalists.csv

This data collected with the help of Twarc helped implement and improve the sentiment analysis model we use (see below). Afterwards, Twitter data started to be collected daily, using Tweepy, and each post is evaluated in the BERT model.

The script that collects tweets daily is in this repository: [capture_tweets.py](https://github.com/JournalismAI/attackdetector/blob/main/capture_tweets.py)

---
## Automation
We learned alternatives to make the process of collecting and cleaning data automatic, and subsequent storage in a database that delivers the result to a website that is updated daily, with data and graphics. 

We looked for alternatives that were easier to code in Python and that were free or less expensive. For this we chose, at this point in the project, [Heroku](https://www.heroku.com/) (a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud with deployments). 

Second, to host the workflows of the site and automation we leave the scripts stored in [Github](https://github.com/). After, to create sites with [Plotly/Dash](https://plotly.com/dash/) (a framework for building data apps in Python), and finally upload and download databases in tables on [Airtable](https://www.airtable.com/). In addition to using [Colab Pro](https://colab.research.google.com/signup) to test and evaluate statistical sentiment analysis models

The [project's website](https://attackdetector.herokuapp.com/) is now live, and daily captures tweets with keywords in Portuguese and Spanish related to journalists and environmental activists. Through the [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler) feature, the [capture_tweets.py](https://github.com/JournalismAI/attackdetector/blob/main/capture_tweets.py) script does this automatically and sends the unduplicated results to two tables in Airtable.

Then, the not-yet-automated part of the project, we compare this new data every day with the data with which the statistical model of the project already made probability evaluations - it's a model of more than 1GB in size. These results and new evaluations then go to two new tables in Airtable, which are responsible for making the project's website visualizations.

---
## Labelling

---

## Pre-trained models

---

## Topic modeling

To classify the different types of hate speech, we applied the [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/) algorithm to identify clusters.

### Clusters for hate speech data in Spanish 
![Clusters for Spanish](assets/clusters-es.png)

### Clusters for hate speech data in Portuguese 
![Clusters for Portuguese](assets/clusters-pt.png)

So far we have identified that the clusters are grouped according to the types of insults used, i.e., attacks based on fatphobia, transphobia, offenses to physical appearance, offenses questioning the intellect, just to mention a few.

---

## Future work

---

## Contact us

If you want to collaborate or just to know more about the project, please reach out to us:

- reinaldo@abraji.org.br
- faguirre@datacritica.org
