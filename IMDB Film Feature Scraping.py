import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

weekly_boxoffice = pd.read_csv('Extract/weekly_boxoffice.csv')
movie_pool = weekly_boxoffice[['movie_odid', 'display_name']].drop_duplicates()
movie_identifiers = pd.read_csv('Extract/movie_identifiers.csv')
movie_imdb_id = movie_identifiers[movie_identifiers['domain']=='IMDB']
movie_imdb_id.rename(columns = {'id':'tconst'}, inplace = True) 
movie_id = pd.merge(movie_pool, movie_imdb_id, how='inner', on=['movie_odid', 'display_name'])
movie_id = movie_id[['tconst']]

# import and merge the imdb public data
title_basics = pd.read_csv('title.basics.tsv',sep='\t')
title_basics = title_basics [title_basics ['titleType'] == 'movie'] # only keep movies
title_ratings = pd.read_csv('title.ratings.tsv',sep='\t') # merge with rating data
title_merge = pd.merge(title_basics, title_ratings, on='tconst') 
title_merge = title_merge[title_merge['startYear']!= '\\N']

movie_space = pd.merge(movie_id, title_merge, how = 'inner', on = 'tconst')
movie_space['startYear'] = movie_space['startYear'].astype(int)
movie_space = movie_space[movie_space['startYear'] >= 1997]



sample_space = movie_space
#[movie_space['startYear'] == 1997]
#sample_space = movie_space[movie_space['startYear'] == 1998]
#sample_space = movie_space[movie_space['startYear'] == 1999]
#sample_space = movie_space[movie_space['startYear'] == 2000]
#sample_space = movie_space[movie_space['startYear'] == 2001]
#sample_space = movie_space[movie_space['startYear'] == 2002]
#sample_space = movie_space[movie_space['startYear'] == 2003]
#sample_space = movie_space[movie_space['startYear'] == 2004]
#sample_space = movie_space[movie_space['startYear'] == 2005]
#sample_space = movie_space[movie_space['startYear'] == 2006]
#sample_space = movie_space[movie_space['startYear'] == 2007]
#sample_space = movie_space[movie_space['startYear'] == 2008]
#sample_space = movie_space[movie_space['startYear'] == 2009]
#sample_space = movie_space[movie_space['startYear'] == 2010]
#sample_space = movie_space[movie_space['startYear'] == 2011]
#sample_space = movie_space[movie_space['startYear'] == 2012]
#sample_space = movie_space[movie_space['startYear'] == 2013]
#sample_space = movie_space[movie_space['startYear'] == 2014]
#sample_space = movie_space[movie_space['startYear'] == 2015]
#sample_space = movie_space[movie_space['startYear'] == 2016]
#sample_space = movie_space[movie_space['startYear'] == 2017]
#sample_space = movie_space[movie_space['startYear'] == 2018]
#sample_space = movie_space[movie_space['startYear'] == 2019]
len(sample_space)


# In[402]:


imdbID_space = sample_space['tconst']
length = len(sample_space)

imdbID = []
runtimeMin = []
mpaa = []
genre = []
releaseDates = []
ratings = []
numVotes = []
plots = []
directors = []
writers = []
stars = []
metascore = []
numReviews = []
numCritics = []
awards = []
country = []
language = []
budget = []
openingWeekend = []
gross = []
color = []
#distributors = []
#productionCom = []

i = 0
for x in imdbID_space[9940:length]:
    
    print(i, ".", x)
    
    # create the imdbID
    
    url = 'https://www.imdb.com/title/' + x
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    imdbID.append(x)
    
    ### runtime minutes
    
    if len(soup.find_all('time')) == 0:
        runtimeMin.append(None)
    elif len(soup.find_all('time')) == 2:
        runtimeMin.append(soup.find_all('time')[1].text)
    else:
        runtimeMin.append(soup.find_all('time')[0].text.replace(" ", "").replace("\n", ""))
    
    ### mpaa ratings, genres, release dates
    if len(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")) == 4:
        mpaa.append(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")[0])
        genre.append(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")[2])
        releaseDates.append(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")[3])
        
    elif (len(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")) == 2) & (len(soup.find_all('time')) == 0):
        mpaa.append("Not Rated")
        genre.append(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")[0])
        releaseDates.append(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")[1])
    elif (len(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")) == 2) & (len(soup.find_all('time')) != 0):
        mpaa.append("Not Rated")
        genre.append(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")[1])
        releaseDates.append(None)
    else: 
        mpaa.append("Not Rated")
        genre.append(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")[1])
        releaseDates.append(soup.find('div', attrs={'class':'subtext'}).text.replace(" ", "").replace("\n", "").split("|")[2])


    ### ratings
    ratings.append(soup.find('span', attrs={'itemprop': "ratingValue"}).text)
    
    ### number of votes
    numVotes.append(soup.find('span', attrs={'itemprop': "ratingCount"}).text.replace(",", ""))
    
    ### plots
    plots.append(" ".join(soup.find('div', attrs={'class': "summary_text"}).text.replace("\n", "").split()))
    
    ### directors, writers, stars
    if len(soup.find_all('div', attrs={'class': "credit_summary_item"})) == 0:
        directors.append(None)
        writers.append(None)
        stars.append(None)
    elif len(soup.find_all('div', attrs={'class': "credit_summary_item"})) == 3:
        directors.append([item.text for item in soup.find_all('div', attrs={'class': "credit_summary_item"})[0].find_all('a')])
        writers.append([item.text for item in soup.find_all('div', attrs={'class': "credit_summary_item"})[1].find_all('a')])
        stars.append([item.text for item in soup.find_all('div', attrs={'class': "credit_summary_item"})[2].find_all('a')][:-1])
    elif len(soup.find_all('div', attrs={'class': "credit_summary_item"})) == 1:
        directors.append([item.text for item in soup.find_all('div', attrs={'class': "credit_summary_item"})[0].find_all('a')])
        writers.append(None)
        stars.append(None)
    else:
        directors.append([item.text for item in soup.find_all('div', attrs={'class': "credit_summary_item"})[0].find_all('a')])
        writers.append(None)
        stars.append([item.text for item in soup.find_all('div', attrs={'class': "credit_summary_item"})[1].find_all('a')][:-1])
    
    ### meta scores
    if soup.find('div', attrs={'class': "titleReviewBarItem"}) is None:
        metascore.append(None)
    else:
        metascore.append(soup.find('div', attrs={'class': "titleReviewBarItem"}).find('span').text)
    
    ### number of reviews, number of critics
    if soup.find('div', attrs={'class': 'titleReviewBarItem titleReviewbarItemBorder'}) is None:
        numReviews.append(0)
        numCritics.append(0)
    elif len(soup.find('div', attrs={'class': 'titleReviewBarItem titleReviewbarItemBorder'}).find_all('a')) == 1:
        numReviews.append(soup.find('div', attrs={'class': 'titleReviewBarItem titleReviewbarItemBorder'}).find_all('a')[0].text.replace(" user", "").replace(",", ""))
        numCritics.append(0)
    else:
        numReviews.append(soup.find('div', attrs={'class': 'titleReviewBarItem titleReviewbarItemBorder'}).find_all('a')[0].text.replace(" user", "").replace(",", ""))
        numCritics.append(soup.find('div', attrs={'class': 'titleReviewBarItem titleReviewbarItemBorder'}).find_all('a')[1].text.replace(" critic", "").replace(",", ""))
    
    ### awards
    awards.append([item.text.replace("\n", "").replace("  ", "") for item in soup.find_all('span', attrs={'class': 'awards-blurb'})])
    
    ### countries
    if soup.find('h4', attrs={'class': 'inline'}, string = 'Country:') is None:
        country.append(None)
    else:
        country.append(soup.find('h4', attrs={'class': 'inline'}, string = 'Country:').next_sibling.next_sibling.text)
    
    ### languages
    if soup.find('h4', attrs={'class': 'inline'}, string = 'Language:') is None:
        language.append(None)
    else:
        language.append(soup.find('h4', attrs={'class': 'inline'}, string = 'Language:').next_sibling.next_sibling.text)
    
    ### budgets
    if soup.find('h4', attrs={'class': 'inline'}, string = 'Budget:') is None:
        budget.append(None)
    else:
        budget.append(soup.find('h4', attrs={'class': 'inline'}, string = 'Budget:').next_sibling.replace(" ", "").replace("\n", "").replace(",", ""))
    
    ### opening weekend boxoffice revenue USA
    if soup.find('h4', attrs={'class': 'inline'}, string = 'Opening Weekend USA:') is None:
        openingWeekend.append(None)
    else:
        openingWeekend.append(soup.find('h4', attrs={'class': 'inline'}, string = 'Opening Weekend USA:').next_sibling.replace(" ", "").replace("\n", "").replace(",", ""))
    
    ### gross boxoffice revenue USA
    if soup.find('h4', attrs={'class': 'inline'}, string = 'Gross USA:') is None:
        gross.append(None)
    else:
        gross.append(soup.find('h4', attrs={'class': 'inline'}, string = 'Gross USA:').next_sibling.replace(" ", "").replace("\n", "").replace(",", ""))
    
    ### color
    if soup.find('h4', attrs={'class': 'inline'}, string = 'Color:') is None:
        color.append('Color')
    else:
        color.append(soup.find('h4', attrs={'class': 'inline'}, string = 'Color:').next_sibling.next_sibling.text)
    
    
    #url = 'https://www.imdb.com/title/' + x + '/companycredits'
    #page = requests.get(url)
    #soup = BeautifulSoup(page.text, 'html.parser')
    
    #distributors.append(soup.find('h4', attrs={'class': 'dataHeaderWithBorder', 'id':'distributors'}).next_sibling.next_sibling.find('a').text)
    #productionCom.append(soup.find('h4', attrs={'class': 'dataHeaderWithBorder', 'id':'production'}).next_sibling.next_sibling.find('a').text)


    
    i = i+1


# In[403]:


zippedList = zip(imdbID, mpaa, runtimeMin, genre, releaseDates, ratings, numVotes, plots, directors, 
                 writers, stars, metascore, numReviews, numCritics, awards, country, language, 
                 budget, openingWeekend, gross, color)

imdbfeatures = pd.DataFrame(zippedList, columns = ['imdbID', 'mpaa', 'runtimeMin', 'genre', 'releaseDates', 
                                                   'ratings', 'numVotes', 'plots', 'directors', 'writers', 
                                                   'stars', 'metascore', 'numReviews', 'numCritics', 'awards', 
                                                   'country', 'language', 'budget', 'openingWeekend', 'gross', 
                                                   'color'])
imdbfeatures.to_csv('Features/imdbFeatures_7.csv', index = False)


# ## Clean the data

# In[6]:


imdbFeatures_1 = pd.read_csv('Features/imdbFeatures_1.csv')
imdbFeatures_2 = pd.read_csv('Features/imdbFeatures_2.csv')
imdbFeatures_3 = pd.read_csv('Features/imdbFeatures_3.csv')
imdbFeatures_4 = pd.read_csv('Features/imdbFeatures_4.csv')
imdbFeatures_5 = pd.read_csv('Features/imdbFeatures_5.csv')
imdbFeatures_6 = pd.read_csv('Features/imdbFeatures_6.csv')
imdbFeatures_7 = pd.read_csv('Features/imdbFeatures_7.csv')
imdbFeatures_pre = pd.concat([imdbFeatures_1, imdbFeatures_2, imdbFeatures_3, 
                              imdbFeatures_4, imdbFeatures_5, imdbFeatures_6, imdbFeatures_7,])


imdbFeatures_pre = imdbFeatures_pre[['imdbID', 'mpaa', 'runtimeMin', 'genre', 'ratings',
                                     'numVotes', 'plots', 'directors', 'writers', 'stars',
                                     'country', 'language', 'color']].reset_index()
# mpaa
imdbFeatures_pre['mpaa'].loc[imdbFeatures_pre['mpaa']== 'Not Rated'] = 'Unrated'
imdbFeatures_pre['mpaa'].loc[imdbFeatures_pre['mpaa']== 'NotRated'] = 'Unrated'
imdbFeatures_pre = imdbFeatures_pre[(imdbFeatures_pre['mpaa'] != 'TV-14') &
                                    (imdbFeatures_pre['mpaa'] != 'TV-MA') &
                                    (imdbFeatures_pre['mpaa'] != 'TV-PG') &
                                    (imdbFeatures_pre['mpaa'] != 'TV-Y7') &
                                    (imdbFeatures_pre['mpaa'] != 'TV-G')]
imdbFeatures_pre['runtimeMin'] = imdbFeatures_pre['runtimeMin'].replace('min', '', regex = True)

# genre
imdbFeatures_pre['genre1'] = imdbFeatures_pre['genre'].str.split(',', expand = True)[0]
imdbFeatures_pre['genre2'] = imdbFeatures_pre['genre'].str.split(',', expand = True)[1]
imdbFeatures_pre['genre3'] = imdbFeatures_pre['genre'].str.split(',', expand = True)[2]

# directors
imdbFeatures_pre['directors'] = imdbFeatures_pre['directors'].str.split(',', expand = True)[0]
imdbFeatures_pre['directors'] = imdbFeatures_pre['directors'].replace("'", '', regex = True).replace("\"", '', regex = True).replace("\[", '', regex = True).replace("\]", '', regex = True)
imdbFeatures_pre['directors'] = imdbFeatures_pre['directors'].str.strip()

# writers
imdbFeatures_pre['writers'] = imdbFeatures_pre['writers'].str.split(',', expand = True)[0]
imdbFeatures_pre['writers'] = imdbFeatures_pre['writers'].replace("'", '', regex = True).replace("\"", '', regex = True).replace("\[", '', regex = True).replace("\]", '', regex = True)
imdbFeatures_pre['writers'] = imdbFeatures_pre['writers'].str.strip()


# Star
imdbFeatures_pre['star1'] = imdbFeatures_pre['stars'].str.split(',', expand = True)[0]
imdbFeatures_pre['star1'] = imdbFeatures_pre['star1'].replace("'", '', regex = True).replace("\"", '', regex = True).replace("\[", '', regex = True).replace("\]", '', regex = True)
imdbFeatures_pre['star1'] = imdbFeatures_pre['star1'].str.strip()
imdbFeatures_pre['star2'] = imdbFeatures_pre['stars'].str.split(',', expand = True)[1]
imdbFeatures_pre['star2'] = imdbFeatures_pre['star2'].replace("'", '', regex = True).replace("\"", '', regex = True).replace("\[", '', regex = True).replace("\]", '', regex = True)
imdbFeatures_pre['star2'] = imdbFeatures_pre['star2'].str.strip()
imdbFeatures_pre['star3'] = imdbFeatures_pre['stars'].str.split(',', expand = True)[2]
imdbFeatures_pre['star3'] = imdbFeatures_pre['star3'].replace("'", '', regex = True).replace("\"", '', regex = True).replace("\[", '', regex = True).replace("\]", '', regex = True)
imdbFeatures_pre['star3'] = imdbFeatures_pre['star3'].str.strip()
#country
imdbFeatures_pre['country'] = imdbFeatures_pre['country'].str.strip()
imdbFeatures_pre['country'].loc[imdbFeatures_pre['country']=='USA'] = 1
imdbFeatures_pre['country'].loc[imdbFeatures_pre['country']!= 1] = 0
#language
imdbFeatures_pre['language'] = imdbFeatures_pre['language'].str.strip()
imdbFeatures_pre['language'].loc[imdbFeatures_pre['language']=='English'] = 1
imdbFeatures_pre['language'].loc[imdbFeatures_pre['language']!= 1] = 0

#color
imdbFeatures_pre['color'].loc[imdbFeatures_pre['color']=='Color'] = 1
imdbFeatures_pre['color'].loc[imdbFeatures_pre['color']!= 1] = 0

imdbFeatures = imdbFeatures_pre.drop(['genre', 'stars', 'runtimeMin', 'index'], axis = 1)
imdbFeatures.to_csv('Features/imdbFeatures_reg.csv', index = False)





