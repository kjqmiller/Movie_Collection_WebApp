# Movie_Collectoin_WebApp - Simple web app to catalogue a movie collection
## Introduction
This project allows the user to search for a film or series via the IMDb API and then add any titles they select to their collection. The selected films are then saved to a collection in MongoDB Atlas where they then can be viewed and/or deleted. The back end is ran using Flask with the pages using vanilla HTML and CSS.

## Why?
I started this project because I wanted to:
  * Get some experience building a web application
  * Start learning about Flask and backend development
  * Learn more about using API's
  * Gain experience with a document database (MongoDB Atlas)

## Technologies
  * Python 3.9
  * Flask
  * MongoDB Atlas
  * IMDb API

This application lets the user use the IMDb API to search for movies and TV series. The results of the search are returned and the posters, along with the title and release year are displayed. The user can select as many titles as they wish from the results, and selected titles are then saved. If a title is already in the collection, or there is a problem with the data, then those titles are not added to the database. The user can navigate to the *Collection* page where all titles that are in the database are retrieved and displayed. The titles can also be clicked on and a new tab will open with that title's IMDb page.
