## IMDB Scraping

This web scraper is tailored for imdb.com. The main goal is to collect user-generated online text reviews as well as relevant movie features for future research purposes. Here I list all the variables that will be gathered.

Note: IMDB does offer public datasets: https://www.imdb.com/interfaces/. 

### IMDB Text Reviews Scraping.py

1. imdbID: the IMDB ID of the movie title
2. totalNumReviews: total number of reviews of the movie title
3. userID: the IMDB ID of the user who posted the review
4. spoilerWarning: equals to 1 if the review is marked with "Warning: Spoilers"
5. reviewTitles: the title of the review
6. usefulNum: the number of users who find the review helpful
7. usefulTotal: the number of users who vote
8. reviewDates: the date of the review got posted
9. userReviews: the text content of the review
10. userRates: the rating given along with the review, a numerical value between 0 and 10
                                                  
The final results in dataframe format may look like the following:

<img width="1354" alt="Screen Shot 2020-09-04 at 11 32 19 AM" src="https://user-images.githubusercontent.com/33683715/92274609-6da71300-eea2-11ea-91fe-aceae8520a78.png">

### IMDB Film Features Scraping.py

imdbID, runtimeMin, mpaa, genre, releaseDates, ratings, numVotes, plots, directors, writers, stars, metascore, numReviews, numCritics, country, language, budget, openingWeekend, color
