# Twitter_Extraction_Analysis
Twitter Extraction and Analysis Tools based on Tweepy

Made for UniMe internship (code: T.E.A.)

The project is composed of three tools:

- <b>twitter_tea.py</b> connects to Twitter (using user's API Keys) and get a certain number of tweets based on given search parameters, saving them on file. (run `./twitter_tea.py -h` to check arguments)

- <b>trend_processing.py</b> read downloaded tweets and classifies them for "sentiment" (positive/negative/neutral) regarding the current search, then plot three histograms based on classified data, one for each "sentiment". (run `./trend_processing.py -h` to check arguments)

- <b>country_processing.py</b> read downloaded tweets and classifies them for "country" (parsing the tweet origin position on the Earth), then plot a pie chart based on ordered data. (run `./country_processing.py -h` to check arguments)
