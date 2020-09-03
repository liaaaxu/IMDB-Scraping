import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# put down your file/data path
sample_space = ''

# movies are represented by id codes in IMDB database, for example, the movie Joker's id is "tt7286456"
# before scraping, we need to have a movie id space to loop over later


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


zippedList = zip(imdbID, totalNumReviews, userID, spoilerWarning, reviewTitles, reviewUseful, reviewDates,
                 userReviews, userRates)

imdbReviews = pd.DataFrame(zippedList, columns = ['imdbID', 'totalNumReviews', 'userID', 'spoilerWarning', 
                                                  'reviewTitles', 'reviewUseful', 'reviewDates', 
                                                  'userReviews', 'userRates'])
imdbReviews.to_csv('Output/imdbReviews.csv')
