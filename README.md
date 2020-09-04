## IMDB Scraping

This web scraper is tailored for imdb.com. The main goal is to collect user-generated online text reviews as well as relevant movie features for future research purposes. Here I list all the variables that will be gathered.

Note: IMDB does offer public datasets: https://www.imdb.com/interfaces/. 

### IMDB Text Reviews Scraping.py

1. imdbID: the IMDB ID of the movie title
2. totalNumReviews: total number of reviews of the movie title
3. userID: the IMDB ID of the user who posted the review
4. spoilerWarning: equals to 1 if the review is marked with "Warning: Spoilers"
5. reviewTitles: the title of the review
6. reviewUseful: the number of users who find the review helpful out of the number of users who vote. Ex: 198 out of 303 found this helpful
7. reviewDates: the date of the review got posted
8. userReviews: the text content of the review
9. userRates: the rating given along with the review, a numerical value between 0 and 10

The final results in dataframe format may look like the following. Notice that further cleaning and organizing are needed to get the neat data.

![Screen Shot 2020-09-03 at 8 59 03 PM](https://user-images.githubusercontent.com/33683715/92200315-6b0ad600-ee2e-11ea-9b0b-b3b7766d3216.png)

### IMDB Film Feature Scraping.py

imdbID, runtimeMin, mpaa, genre, releaseDates, ratings, numVotes, plots, directors, writers, stars, metascore, numReviews, numCritics, country, language, budget, openingWeekend, color
