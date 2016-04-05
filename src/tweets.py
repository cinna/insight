import datetime
import codecs
from functools import partial
import re
import sys
import time
from collections  import deque 
import itertools

class Tweet:
	time = 0
	text = ""
	#hashtags = nodes
	nodes = list()
	edges = list()

#	def __init__(self,timestamp,text):
#		self.time = self.TimestampParser(timestamp)
#		self.text = text

	def __init__(self,timestamp,hashtags):		
		try:
			self.time = timestamp
			if (len(hashtags)>1):
				self.nodes = hashtags
				self.edges = list(itertools.combinations(self.nodes,2))
		except:
			raise 	

	def __lt__(self, other):
	 return (self.time < other.time)
	 	
	def TweetToGraph(self):
		self.nodes = self.HashtagParser(self.text)
		self.edges = list(itertools.combinations(self.nodes,2))
		#return nodes and edges
		return self.nodes, self.edges
	
	def HashtagParser(self,text):
		# to avoid duplicates we define list of hashtags as a set
		hashtags=set()
		escapes='[' + re.escape(''.join([',','.',';','&','(',')','^',':',"'","\""])) + ']'
		for term in sorted(text.split()):
			if (term[0]=='#'):
				clean_term	= re.sub(escapes,'', term) 
				hashtags.add(clean_term)			
		return list(hashtags)
	
	def TimestampParser(self,timestamp):
		try:
			time_ = time.strptime(timestamp, '%a %b %d %H:%M:%S %z %Y')			
			return(time.mktime(time_))
		except ValueError as e:
		    print(e)

class Graph: 
	graph_edges = dict()
	graph_nodes = dict()
	
	def __init__(self, nodes = dict(), edges = dict()):
		self.graph_nodes = nodes
		self.graph_edges = edges
	
	def AddTweetToGraph(self, tweet):
		#nodes, edges = TweetToGraph(tweet)	
		if len(tweet.nodes)>1 :
			for node in tweet.nodes:
				if node in self.graph_nodes:
					self.graph_nodes[node] += 1
				else:
					self.graph_nodes[node] = 1
			for edge in tweet.edges:
				if edge in self.graph_edges:					
					self.graph_edges[edge] += 1
				else:
					self.graph_edges[edge] = 1		
	
	def RemoveTweetFromGraph(self, tweet):	
		if len(tweet.nodes)>1 :	
			for node in tweet.nodes:
				if node in graph_nodes:
					self.graph_nodes[node] -= 1					
					if self.graph_nodes[node]  <= 0:
						self.graph_nodes.pop(node,None)						
				else:
					raise ValueError('Graph error: no such a node in the graph')			
			for edge in tweet.edges:
				if edge in graph_edges:
					self.graph_edges[edge] -= 1
					if self.graph_edges[edge]  <= 0:
						self.graph_edges.pop(edge,None)
				else:
					raise ValueError('Graph error: no such an edge in the graph')
