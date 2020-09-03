#!/usr/bin/env python
# coding: utf-8

# # IMDB Text Reviews Scraping

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[4]:


data = '/Users/lia/Google Drive/UW PhD/Lia Research/PROJECTS/Data/'


# In[13]:


weekly_boxoffice = pd.read_csv(data + 'Opus Extract/weekly_boxoffice.csv')
movie_pool = weekly_boxoffice[['movie_odid', 'display_name']].drop_duplicates()
movie_identifiers = pd.read_csv(data +'Opus Extract/movie_identifiers.csv')
movie_imdb_id = movie_identifiers[movie_identifiers['domain']=='IMDB']
movie_imdb_id.rename(columns = {'id':'tconst'}, inplace = True) 
movie_id = pd.merge(movie_pool, movie_imdb_id, how='inner', on=['movie_odid', 'display_name'])
movie_id = movie_id[['tconst']]

# import and merge the imdb public data
title_basics = pd.read_csv(data + 'IMDB/title.basics.tsv',sep='\t')
title_basics = title_basics [title_basics ['titleType'] == 'movie'] # only keep movies
title_ratings = pd.read_csv(data + 'IMDB/title.ratings.tsv',sep='\t') # merge with rating data
title_merge = pd.merge(title_basics, title_ratings, on='tconst') 
title_merge = title_merge[title_merge['startYear']!= '\\N']

movie_space = pd.merge(movie_id, title_merge, how = 'inner', on = 'tconst')
movie_space['startYear'] = movie_space['startYear'].astype(int)
movie_space = movie_space[movie_space['startYear'] >= 1997]


# In[38]:


movie_space


# In[14]:


movie_space[movie_space['tconst'] == 'tt9844368']


# In[58]:


#sample_space = movie_space[movie_space['startYear'] == 1997]
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
sample_space = movie_space[movie_space['startYear'] == 2019]
#sample_space = movie_space[movie_space['tconst'] == 'tt9844368']
len(sample_space)


# In[59]:


imdbID_space = sample_space['tconst']
length = len(sample_space)
imdbID = []
totalNumReviews = []
spoilerWarning = []
reviewTitles = []
reviewUseful = []
reviewDates = []
userReviews = []
userRates = []
userID = []

i = 0
for x in imdbID_space[0:length]:
    
    print(i, ".", x)
    
    # create the imdbID
    
    url = 'https://www.imdb.com/title/' + x + '/reviews'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Scrape the first page
    # find the total number of the reviews  
    total = "".join(soup.find('div', attrs={'class':'header'}).find('span').text.split()[0].split(","))
    info_base = soup.find_all('div', attrs={'class':'lister-item'})
    selector = 'span svg + span' 
    
    for info in info_base:
        
        imdbID.append(x)
        totalNumReviews.append(total)
        userRates.append(info.select(selector))
        reviewTitles.append(info.find('a', attrs={'class':'title'}).text)
        reviewDates.append(info.find('span', attrs={'class':'review-date'}).text)
        reviewUseful.append(info.find('div', attrs={'class':'actions text-muted'}).text)
        userID.append(info.find('span', attrs={'class':'display-name-link'}).find('a').get('href'))
        userReviews.append(info.find('div', attrs={'class':'text show-more__control'}).text)
        
        if info.find('span', attrs={'class':'spoiler-warning'}) is None:
            
            spoilerWarning.append('None')
        else:          
            spoilerWarning.append(info.find('span', attrs={'class':'spoiler-warning'}).text)
            
        
    # since each page only display 25 items, we need to loop more times
    looptimes = int(np.floor(int(total)/25))
    print('Need to loop', looptimes, 'times')
    
    for j in range(looptimes-1):

        datakey = soup.find('div', attrs={'class':'load-more-data'}).get('data-key')
        url_loadmore = 'https://www.imdb.com/title/' + x + '/reviews/_ajax?paginationKey=' + datakey
        page_loadmore = requests.get(url_loadmore)
        soup_loadmore = BeautifulSoup(page_loadmore.text, 'html.parser')
        
        info_base_loadmore = soup.find_all('div', attrs={'class':'lister-item'})
        selector = 'span svg + span' 
        
        for info_loadmore in info_base_loadmore:
            imdbID.append(x)
            totalNumReviews.append(total)
            userRates.append(info_loadmore.select(selector))
            reviewTitles.append(info_loadmore.find('a', attrs={'class':'title'}).text)
            reviewDates.append(info_loadmore.find('span', attrs={'class':'review-date'}).text)
            reviewUseful.append(info_loadmore.find('div', attrs={'class':'actions text-muted'}).text)
            userID.append(info_loadmore.find('span', attrs={'class':'display-name-link'}).find('a').get('href'))
            userReviews.append(info_loadmore.find('div', attrs={'class':'text show-more__control'}).text)    
            
            if info.find('span', attrs={'class':'spoiler-warning'}) is None:
                spoilerWarning.append('None')
            else:          
                spoilerWarning.append(info_loadmore.find('span', attrs={'class':'spoiler-warning'}))
            
        
        soup = soup_loadmore
        
        print(j)
    
    i = i+1


# In[60]:


zippedList = zip(imdbID, totalNumReviews, userID, spoilerWarning, reviewTitles, reviewUseful, reviewDates,
                 userReviews, userRates)

imdbReviews = pd.DataFrame(zippedList, columns = ['imdbID', 'totalNumReviews', 'userID', 'spoilerWarning', 
                                                  'reviewTitles', 'reviewUseful', 'reviewDates', 
                                                  'userReviews', 'userRates'])
imdbReviews.to_csv('Output/imdbReviews_2019.csv')


# In[ ]:




