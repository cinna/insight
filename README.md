
Insight Data Engineering - Coding Challenge
===========================================================

The solution to the [coding challenge](https://github.com/InsightDataScience/coding-challenge) for the Insight Data Engineering Program implemented in Python 3.5.

## Challenge Summary

This challenge is to implement two features:

1. Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.
2. Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.

Here, we have to define a few concepts (though there will be examples below to clarify):

- A tweet's text is considered "clean" once all of the escape characters (e.g. \n, \", \/ ) and unicode have been removed.
- A Twitter hashtag graph is a graph connecting all the hashtags that have been mentioned together in a single tweet.

## Details of Implementation

We'd like you to implement your own version of these two features.  However, we don't want this challenge to focus on the relatively uninteresting "dev ops" of connecting to the Twitter API, which can be complicated for some users.  Normally, tweets can be obtained through Twitter's API in JSON format, but you may assume that this has already been done and written to a file named `tweets.txt` inside a directory named `tweet_input`.  For simplicity, this file `tweets.txt` will only contain the actual JSON messages (in reality, the API also can emit messages about the connection and the API rate limits).  Additionally, `tweets.txt` will have the content of each tweet on a newline:

tweets.txt:

	{JSON of first tweet}  
	{JSON of second tweet}  
	{JSON of third tweet}  
	.
	.
	.
	{JSON of last tweet}  

## First Feature

The point of the first feature is to extract and clean the relevant data for the Twitter JSON messages with the format of 

	<contents of "text" field> (timestamp: <contents of "created_at" field>)

## Second Feature
The second feature will continually update the Twitter hashtag graph and hence, the average degree of the graph. The graph should just be built using tweets that arrived in the last 60 seconds as compared to the timestamp of the latest tweet. As new tweets come in, edges formed with tweets older than 60 seconds from the timstamp of the latest tweet should be evicted. For each incoming tweet, only extract the following fields in the JSON response
* "hastags" - hashtags found in the tweet
* "created_at" - timestamp of the tweet


## Tweets Cleaned

The solution is based on using a generator to read and buffer data to ensure that the process can handle the largest data files. A custom tokenization is used to retrieve the text and timestamp from tweets. The decoder is designed to satisfy the requirements in the official repository. We keep counts of all extracted tweets with unicode characters. The extracted cleaned tweets are written to the output file.

## Average degree of the hashtag graph

The solution is based on using two data structures: a "dictionary" to keep track of all edges on the current graph and a "queue" to store all tweets within last 60 seconds window. The number of contributing tweets are kept in the dictionary. The contributing tweets keep the graph up to date. Once all tweets liked to an edge are expired from the time window, then the node and edges are removed from graph.  This gives the simple complexity to perform the search operations in _O(1)_ time and to add/remove nodes from the queue in _O(1)_ time. The two operations are all we need to maintain an updated version of the graph. n


## Run programs

Both _Cleaned Tweets_ and _Average Degree_ programs are launched by running _run.sh_ Bash script:

	./run.sh

The results will be available in the files _tweet_output/ft1.txt_ and _tweet_output/ft2.txt_.

To manually run the programs:

	python insight_challenge/src/tweets_cleaned.py <file_1> <file_n>
	python insight_challenge/src/average_degree.py <file_1> <file_n>


## Tests

Tests are available in the _tests_ directory. 

	cd tests
	ft1.txt, ft2.txt 


## Dependencies

- Python3

### Library Dependencies
- Standard python libraries
 datetime,  codecs,  functools, re, sys, time, deque, collections, itertools, codecs



