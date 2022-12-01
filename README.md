# Attack Detector

This project is part of the [2022 JournalismAI Fellowship Programme](https://www.lse.ac.uk/media-and-communications/polis/JournalismAI/Fellowship-Programme). The Fellowship brought together 46 journalists and technologists from across the world to collaboratively explore innovative solutions to improve journalism via the use of AI technologies. You can explore all the Fellowship projects [at this link](https://www.lse.ac.uk/media-and-communications/polis/JournalismAI/Fellowship-Programme).

The project was developed as a collaboration between *[Abraji](https://www.abraji.org.br/)* and *[Data Crítica](https://datacritica.org/)*. The fellows who contributed to the project are: *[Reinaldo Chaves](https://twitter.com/paidatocandeira) (Project Coordinator-Abraji), [Schirlei Alves](https://twitter.com/schirlei_alves) (Data Journalist-Abraji), [Fernanda Aguirre](https://twitter.com/feragru) (Data Analyst & Researcher-Data Crítica) and [Gibran Mena](https://twitter.com/gibsteria) (Co-founder & Director-Data Crítica)*.

[JournalismAI](https://www.lse.ac.uk/media-and-communications/polis/JournalismAI) is a project of [Polis](https://www.lse.ac.uk/media-and-communications/polis) – the journalism think-tank at the London School of Economics and Political Science – and it’s sponsored by the [Google News Initiative](https://newsinitiative.withgoogle.com/). If you want to know more about the Fellowship and the other JournalismAI activities, [sign up for the newsletter](https://mailchi.mp/lse.ac.uk/journalismai) or get in touch with the team via hello@journalismai.info

---

## Contents

- [Introduction](#introduction)
- [Methodology](#methodology)
- [Data](#data)
- [Labelling](#labelling)
- [Pre-trained models](#pre-trained-models)
- [Topic modeling](#topic-modeling)
- [Future work](#future-work)
- [Contact us](#contact-us)

---

## Introduction

The motivation for this project is the rampant situation of violence against journalists in our countries. Between January and April 2022, Abraji identified 151 episodes of physical and verbal aggressions against journalists in Brazil (62.9% originated on the internet).

In Mexico, from 2000 to date, the journalist protection organization [Artículo 19](https://articulo19.org/) has documented 156 murders of journalists. 47 happened during the administration of former President Enrique Peña Nieto and 36 under current President Andrés Manuel López Obrador. 

In the 2021 [World Press Freedom Index](https://rsf.org/en/2021-world-press-freedom-index-journalism-vaccine-against-disinformation-blocked-more-130-countries), Reporters Without Borders places Brazil and Mexico on the list of countries where journalism is very risky – 111th and 143rd respectively – out of 180 countries. They share the “bad” classification with India (142nd) and Russia (at 150th), among others.

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

We requested the [Twitter academic account](https://developer.twitter.com/en/products/twitter-api/academic-research) that allows a larger extraction, of up to 10M per month, and we learned the commands to use and to build queries in two projects that use the Twitter API: Twarc and Tweepy

---
## Automation

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
