## IMDB Scraping

This web scraper is tailored for imdb.com. The main goal is to collect user-generated online text reviews as well as relevant movie features for some research purpose. Here I list all the variables that will be gathered:

### IMDB Text Reviews Scraping.py

1. imdbID: the IMDB ID of the movie
2. totalNumReviews: total numner of reviews of the movie
3. spoilerWarning: equals to 1 if the review is marked with "Warning: Spoilers"
4. reviewTitles: the title of the review
5. reviewUseful: the number of users who find the review helpful out of the number of users who vote, ex: 198 out of 303 found this helpful
6. reviewDates: the date of the review posted
7. userReviews: the text content of the review
8. userRates: the rating given along with the review
9. userID: the IMDB ID of the user who posted the reveiw


### IMDB Film Feature Scraping.py

imdbID, runtimeMin, mpaa, genre, releaseDates, ratings, numVotes, plots, directors, writers, stars, metascore, numReviews, numCritics, country, language, budget, openingWeekend, color
