#Twitter Extraction and Analysis
Twitter Extraction and Analysis Tools based on Tweepy

Made for UniMe internship and thesis (code: T.E.A.)

**Important** : before running any tool, get your Twitter API keys and write them in the authorization file (for example: `auth_creds.ini`).

_Works with Linux (any distro), Windows (7/8.1/10), macOS (from OS X Yosemite to higher)_

**System Requirements**
- Python 3 (works **only** on Python 3, no backports for now)
- Tweepy module
- Texblob module
- NLTK corpora (use: `python -m textblob.download_corpora`)
- Geocoder module
- Matplotlib module
- Pandas module
- Fuzzywuzzy module (used for text comparison)
- Numpy module

##Quickstart

###Tweets extraction and "sentiment" analysis
- Script name: `twitter_tea.py`
- Purpose: download all the recent tweets (from Twitter main page) that contains a specific hashtag, then find all the other hashtags related and classifies them for "sentiment" (polarity for Textblob/NLTK). 
- Output: three files with the most used hashtag used in "positive", "negative" and "neutral" tweets, divided per sentiment; a file containing all the downloaded tweets with user, datetime and full text.
- Arguments: 
	- `-a`: user auth. file (containing Twitter Dev. keys)
	- `-o`: output filename (full downloaded tweets CSV file)
	- `-n`: number of tweets to download
	- `-t`: query hashtag (between `""` or `''`)

###Hashtag/Sentiment plotter
- Script name: `trend_plotter.py`
- Purpose: plot three graphs regarding the most used "positive/negative/neutral" hashtags, using specified plot parameters, related to query hashtag.
- Output: three PNG images saved into the same script dir.
- Arguments:
	- `-i`: base input file (full downloaded tweets CSV filename)
	- `-n`: number of tweets to parse.
	- `-t`: query hashtag
	- `-l`: limit the hashtag frequency in Y bar (for plotting)
	- `-g`: open graph in window (y/n)

###Country plotter
- Script name: `country_plotter.py`
- Purpose: plot a graph regarding the countries from witch users send tweets related to query hashtag.
- Output: a PNG image saved into the same script dir; a "db" file used for caching geo locations.
- Arguments:
	- `-i`: base input file (full downloaded tweets CSV filename)
	- `-n`: number of tweets to parse.  
	- `-h`: query hashtag
	- `-l`: limit the hashtag frequency in the pie-chart (for plotting)
	- `-g`: open graph in window (y/n)

**Important**: the script is based on caching geolocations using a Koomot online database; it store already-processed country names in a "db" file used as simply database. 
Basically the script improves its performance every time it's launched: the more is running, the more country names are stored into geo-cache file.

###Timeline extraction
- Script name: `get_timeline.py`
- Purpose: get the timeline of a specified username (no more than 3400 tweets can be dowloaded) and the "sentiment" (polarity) for each saved tweet.
- Output: a CSV file containing the full timeline and sentiment data per tweet.
- Arguments:
	- `-a`: user auth. file (containing Twitter Dev keys)
	- `-u`: username to analyze
	- `-o`: output filename

###Filter timeline by keywords
- Script name: `filter_timeline.py`
- Purpose: filter tweets in a CSV timeline, using specified "query" keywords
- Output: a new CSV file containing only the tweets with query kewywords, sentiment data included.
- Arguments:
	- `-i`: input CSV timeline
	- `-k`: keywords (between `""` or `''`, each word separed by comma, like: `word1,word2,...`)

###Timeline "sentiment" analysis
- Script name: `process_timeline.py`
- Purpose: build a dataset with tweet dates, average sentiment and error per each date; save it to a CSV file.
- Output: a CSV file with dates, avg sentiment and error
- Arguments:
	- `-i`: input filtered timeline (already processed by `filter_timeline.py`)
	- `-o`: output filename

**Note**: `error = (sentiment_max_day - sentiment_min_day) / 2`

###Timeline Plotter
- Script name: `polarity_plotter.py`
- Purpose: plot a scatter graph regarding polarities and errors, in a specified timeframe
- Output: a PNG image saved in the same script dir.
- Arguments:
	- `-i`: input analyzed&filtered CSV file (already processed by `process_timeline.py`)
	- `-u`: username of analyzed account
	- `-k`: query keywords
	- `-g`: open graph in window (y/n)
	- `-s`: starting date (for limits view to specific timeframe)
	- `-e`: ending date (for limits view to specific timeframe)

##Followers extraction
- Script name: `get_followers.py`
- Purpose: get the follower of a specified account
- Output: a CSV file written with followers usernames
- Arguments:
	- `-a`: user auth. file (containing Twitter Dev. keys)
	- `-u`: account username to analyze
	- `-o`: output filename

**Note**: Each session can download only 3200 usernames every 15 minutes; rate limits can't be surpassed.
