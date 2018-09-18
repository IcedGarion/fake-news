''' Features class with score(record) and mean(scores) methods.
	each feature returns a score based on a record,
	and has a method for reducing the list of obtaied scores.

	RECORD structure:
	id: unique id for a news article
	title: the title of a news article
	author: author of the news article
	text: the text of the article; could be incomplete
	label: a label that marks the article as potentially unreliable
	    1: unreliable
	    0: reliable
'''

from nltk.parse import stanford
from pattern.metrics import ttr
import re, os, chardet


class twitter_search:
	def __init__(self):
		pass

	def score(self, record):
		return 0

	def mean(self, scores):
		return 0

	def __str__(self):
		return "twitter search"


#class morfological_complexity:
#	''' stanford parser: complexity of the sentence's parsing tree '''
#
#	def __init__(self):
#		# stanford parser setup
#		parser_base_dir = "../parser/stanford-parser-full-2018-02-27"
#		modelpath = model_path=parser_base_dir + "/englishPCFG.ser.gz"
#		os.environ['CLASSPATH'] = parser_base_dir
#		os.environ['STANFORD_PARSER'] = parser_base_dir
#		os.environ['STANFORD_MODELS'] = parser_base_dir
#		self.parser = stanford.StanfordDependencyParser(model_path=modelpath, encoding='utf8')






	# siamo qua
#	def score(self, record):
#		print(record["text"])
		# converts to unicode-utf8 for compatibility problems with python2

		# controllare api stanford parser: funzione che interessa? parse, raw_parse_sents, parse.... ?
			#sentences = self.parser.parse(unicode(record["text"], "utf-8"))
#			sentences = self.parser.raw_parse_sents(unicode(record["text"], "utf-8"))

#		for sentence in sentences:
#			print(len(list(sentence)))
#		return 0











#	def mean(self, scores):
#		return sum(scores) / len(scores)


class lexical_variety:
	''' pattern.metrics.ttr: average percentage of unique words (types)
		for each n successive words (tokens) in the text.
		https://www.clips.uantwerpen.be/pages/pattern-metrics'''

	def __init__(self):
		# min text length
		self.min_text = 3

	def score(self, record):
		# applies ttr function to "text", with n the number of distinct tokens (use a tokenizer?)
		# checks for the text not being a string or "empty"
		return ttr(record["text"], n=len(re.split("\W+", record["text"]))) \
			if isinstance(record["text"], str) and len(record["text"]) > self.min_text \
			else 0

	def mean(self, scores):
		return sum(scores) / len(scores)

	def __str__(self):
		return "lexical_variety"
