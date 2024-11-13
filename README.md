# BaT-Auction-Analysis

The goal of this project is to be able to predict the hammer price for a car on BringaTrailer (linked below) using variables such as mileage, color, location, transmission, etc. User would be able to pick an eligible car model of their choice and run it through the model. 

**Data Source:** https://bringatrailer.com/

## Tools/Methods used

**Language**: Python
**Libraries/Frameworks**: Pandas, Selenium Webdriver

The code uses Selenium to loop through the auction listing history for a user given model and puts the results and details into a pandas dataframe to be run through an xgboost model

## Optimizations
--


