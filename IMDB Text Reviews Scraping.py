import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

######################################## PART 1: SCRAPING ########################################

# put down your file/data path
sample_space = pd.read_csv('')

# movies are represented by id codes in IMDB database, for example, the movie Joker's id is "tt7286456"
# before scraping, we need to have a movie id space to loop over later
# a good way is to load the data from IMDB public datasets, the "tconst" variable is the alphanumeric unique identifier of the title
# sample_space should be a dataframe with a column called "tconst"

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


######################################## PART 2: CLEANING ########################################

imdbReviews = pd.read_csv('Output/imdbReviews.csv')

imdbID = imdbReviews['imdbID']

totalNumReviews = imdbReviews['totalNumReviews']

userID = imdbReviews['userID']
userID = userID.str.split('/', expand = True)[2]

spoilerWarning = imdbReviews['spoilerWarning']
spoilerWarning[spoilerWarning == "Warning: Spoilers"] = 1
spoilerWarning[spoilerWarning == "None"] = 0
spoilerWarning[spoilerWarning == '<span class="spoiler-warning">Warning: Spoilers</span>'] = 1

reviewTitles = imdbReviews['reviewTitles']
reviewTitles = reviewTitles.str.split('\n', expand = True)[0]

reviewUseful = imdbReviews['reviewUseful']
temp = reviewUseful.str.split('\n', expand = True)[1]
usefulNum = temp.str.split('out of', expand = True)[0].replace(',', '', regex=True).astype(int)
usefulTotal = temp.str.split('out of', expand = True)[1].str.split('found this helpful.', expand = True)[0].replace(',', '', regex=True).astype(int)

reviewDates = imdbReviews['reviewDates']
temp = reviewDates.replace({' January ': '/1/', ' February ': '/2/', ' March ': '/3/', ' April ': '/4/',
                            ' May ': '/5/', ' June ': '/6/', ' July ': '/7/', ' August ': '/8/', 
                            ' September ': '/9/', ' October ': '/10/', ' November ': '/11/', 
                            ' December ': '/12/'}, regex=True).astype(str)
reviewDates = pd.to_datetime(temp, infer_datetime_format=True)

userReviews = imdbReviews['userReviews']

userRates = imdbReviews['userRates']
userRates = userRates.replace({'\[<span>':'', '</span>]':'', '\[]': 0}, regex=True).astype(int)

zippedList = zip(imdbID, totalNumReviews, userID, spoilerWarning, reviewTitles, usefulNum, usefulTotal, reviewDates,
                 userReviews, userRates)

imdbReviews_cleaned = pd.DataFrame(zippedList, columns = ['imdbID', 'totalNumReviews', 'userID', 'spoilerWarning', 
                                                          'reviewTitles', 'usefulNum', 'usefulTotal', 'reviewDates', 
                                                          'userReviews', 'userRates']).reset_index()

imdbReviews_cleaned.to_csv('Output/imdbReviews_cleaned.csv')
