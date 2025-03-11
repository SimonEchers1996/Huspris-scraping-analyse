# Huspris-scraping-analyse
## In the scraping folder
In this folder you will find.
1. for_scraping.py - In this file is the tools to do the scraping. It means getting all the links on the page for boligsiden
2. scrape.py - The main module that runs the scraping. Currently it is scraping house prices in the Odense municipality form 2019 till 2025 march.

## In the analysis folder
In this folder you will find.
1. ScrapedPrices.csv - The initial scraped prices from boligsiden.dk
2. analysis.ipynb - A jupyter notebook describing how I treat the data, filter out outliers and at last two models(random forest and XGBoost) that predict the prices.

What is missing for the analysis is,
1. Evalution of the results and a conclusion. We need to look at the distribution of the errors and at what prices the errors occur. Currently the mean absolute error of the house prices is nearly 700 thousand, which sounds like a lot, but it could be due to a few properties being incorrectly guessed. On the bright side, the model generalizes really well. The models are not trained on the 2024 and 2025 properties, but the error is identical to those from 2019-2023. The work around was normalizing the prices in that range to a 2024/2025 equivalent.
2. A more in-depth filtering out of outliers(there is a lot in the raw data).
