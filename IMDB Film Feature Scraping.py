import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# put down your file/data path
sample_space = pd.read_csv('')

# movies are represented by id codes in IMDB database, for example, the movie Joker's id is "tt7286456"
# before scraping, we need to have a movie id space to loop over later
# a good way is to load the data from IMDB public datasets, the "tconst" variable is the alphanumeric unique identifier of the title
# sample_space should be a dataframe with a column called "tconst"

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


i = 0
for x in imdbID_space[0:length]:
    
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
    
    
    i = i+1


zippedList = zip(imdbID, mpaa, runtimeMin, genre, releaseDates, ratings, numVotes, plots, directors, 
                 writers, stars, metascore, numReviews, numCritics, awards, country, language, 
                 budget, openingWeekend, gross, color)

imdbfeatures = pd.DataFrame(zippedList, columns = ['imdbID', 'mpaa', 'runtimeMin', 'genre', 'releaseDates', 
                                                   'ratings', 'numVotes', 'plots', 'directors', 'writers', 
                                                   'stars', 'metascore', 'numReviews', 'numCritics', 'awards', 
                                                   'country', 'language', 'budget', 'openingWeekend', 'gross', 
                                                   'color'])
imdbfeatures.to_csv('output/imdbFeatures.csv', index = False)
