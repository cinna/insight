# example of program that calculates the average degree of hashtags
# example of program that calculates the number of tweets cleaned
import datetime
import codecs
from functools import partial
import re
import sys
import time
import json
import itertools
import tweets


#Custom bisect insort_right implementation
def insort_right(a, x, lo=0, hi=None):
    #"""Insert item x in list a, and keep it sorted assuming a is sorted.
    #If x is already in a, insert it to the left of the leftmost x.
    #Optional args lo (default 0) and hi (default len(a)) bound the
    #slice of a to be searched.
    #"""
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (hi+lo)//2
        if x.time < a[mid].time : hi = mid
        else: lo = mid+1
    a.insert(lo, x)

#Custom bisect_left implementation
def bisect_left(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid].time < x: lo = mid+1
        else: hi = mid
    return lo


# Custom JSON to extract intended tweets contents
def CustomDecoder(input_text):
	parse_error = False
	tweet_hashtags = list()
	tweet_time = ""
	jsonData = json.loads(input_text)
	#take all hashtags, remove duplicates
	if "entities" in jsonData:
		tweetEntities = jsonData["entities"]
		if "hashtags" in tweetEntities:
			hashtag_list = tweetEntities["hashtags"]
			if hashtag_list:		
				tweet_hashtags = [item['text'] for item in hashtag_list]
				tweet_hashtags = list(set(tweet_hashtags))
	#convert timestamp into datetime format
	if "created_at" in jsonData:
		time_stamp = jsonData["created_at"]
		tweet_time = time.mktime(time.strptime(time_stamp, '%a %b %d %H:%M:%S %z %Y'))	
	else:
		parse_error = True
		raise ValueError('Parse error: two tweets in one line')	
	return tweet_hashtags, tweet_time, parse_error

def HashtagParser(text):
	# to avoid duplicates we define list of hashtags as a set
	hashtags=set()
	escapes='[' + re.escape(''.join([',','.',';','&','(',')','^',':',"'","\""])) + ']'
	for term in sorted(text.split()):
		if (term[0]=='#'):
			clean_term	= re.sub(escapes,'', term) 
			hashtags.add(clean_term)			
	return list(hashtags)
	
def TimestampParser(timestamp):
	try:
		time_ = time.strptime(timestamp, '%a %b %d %H:%M:%S %z %Y')			
		return(time.mktime(time_))
	except ValueError as e:
	    print(e)

# Redundancy in case First Decoder failed! (Yes, it happened in my test cases)
def CustomDecoder2(buffer=''):
	#	retrieving timestamps 			
	index_start = buffer.find("{\"created_at\":\"")
	parse_error=False
	index_end = buffer.find("\",",index_start)
	if ((index_start<0) or (index_end <=0)):		
		parse_error = True
	time_stamp=buffer[index_start+15:index_end]	
	#	retrieving tweets
	index_start = buffer.find(",\"text\":\"")
	index_end = buffer.find("\",",index_start)
	if ((index_start<0) or (index_end <=0)):
		parse_error = True	
	text=buffer[index_start+9:index_end]	    	
	tweet_hashtags = list()
	tweet_time = 0;
	if (not parse_error):	
		tweet_hashtags = HashtagParser(text) 
		tweet_time =  TimestampParser(time_stamp)
	return tweet_hashtags, tweet_time, parse_error #[text,time_stamp], index_end, parse_error

# Read the input data file and extract the tweets
# buffersize can be optimized for the best performance
def JsonParse(fileobj, buffersize=1024*1):
    buffer = ''  
    with fileobj as inFile:  
    	for line in inFile:
    	#for chunk in iter(partial(fileobj.read, buffersize), ''):
         #buffer += line         
         #while buffer:
            try:
                #print(line);
                hashtags, time, parse_error = CustomDecoder(line)                         
                if (not parse_error):
                	yield hashtags, time                   
                buffer = '' #buffer[index:]                
            except ValueError as e:
				# JSON loader fails if there are more than one tweets in one line                
                print(e)
  

                

def ProcessTweets(input_file, output_file):	
	# Graph initialization
	graph = tweets.Graph()

	# 60 second window ordered list
	sixty_seconds_window = []

	# I\O initialization 
	out_file_obj = open(output_file,"w")
	in_file_obj = open(input_file,'r')

	# the file reader can handle file sizes of several TeraBytes
	generator_input = JsonParse(in_file_obj)

	# Main loop	
	for i in generator_input:
		# Instantiate a valid tweet object
		try:
			temp_tweet = tweets.Tweet(i[1],i[0])
		except ValueError as e:
		    #print(e)
		    temp_tweet = tweets.Tweet('Thu Oct 29 17:53:30 +0000 2000',"")		    		    				
		# New incoming tweet object		
		if sixty_seconds_window:
			last_tweet_in_queue = sixty_seconds_window[0]
			time_window_start = last_tweet_in_queue.time
		else:
			time_window_start = 0
		#print(total_tweets)	
		#print(temp_tweet.nodes)
		if (temp_tweet.time >=  time_window_start):      			

			# Add the new tweet to the graph and the queue
			# temp_tweet.TweetToGraph()
			graph.AddTweetToGraph(temp_tweet)		
			insort_right(sixty_seconds_window, temp_tweet)

			#Remove expired objects from the queue
			last_tweet_in_queue=sixty_seconds_window[-1]
			if (last_tweet_in_queue.time > 60):
				index_start = bisect_left(sixty_seconds_window,last_tweet_in_queue.time-60)
				sixty_seconds_window = sixty_seconds_window[index_start:]
			

			# Writing average degree to output		
		if (len(graph.graph_nodes)>0):		
			# average degrees of all nodes = sum(deg(Nodes))/ |Nodes| = 2 * |Edges| /|Nodes|	
			out_file_obj.write('{0:.2f}'.format((len(graph.graph_edges)*2/len(graph.graph_nodes)))+ '\n')
		elif (len(graph.graph_nodes)==0):	
			out_file_obj.write('{0:.2f}'.format(0.00)+ '\n')

	# releasing files 		
	out_file_obj.close()
	in_file_obj.close()

# main program	
def main():
	if len(sys.argv) != 3:
		print ('usage: python average_degree.py ./tweet_input/tweets.txt ./tweet_output/output.txt')
		sys.exit(1)				
	import timeit
	input_file = (sys.argv[1]);
	output_file = (sys.argv[2]);	
	if input_file:
		#t = time.time()
		ProcessTweets(input_file, output_file)
		#print(time.time()-t)

if __name__ == '__main__':
	main()

