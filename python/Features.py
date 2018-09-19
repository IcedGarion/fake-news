''' Features class with score(record) and mean(scores) methods.
	each feature returns a score based on a record (and a dict for dataset column names),
	and has a method for reducing the list of obtained scores
	into a single value.
	"mean" accepts 2 lists and returns a tuple with 2 values: mean for unreliable scores; mean for reliable scores
'''
''' want to plug in / out a feature? Simply write a new class or comment / uncomment it '''

from nltk.parse import stanford
from pattern.metrics import ttr
import numpy, re, os, twitter, functools, itertools


#class twittersearch_related:
#	def __init__(self):
#		pass
#		#self.api =twitter.Api(consumer_key="123", \
#		#		consumer_secret="123", \
#		#		access_token_key="123", \
#		#		access_token_secret="123")
#
#	def score(self, record, namesmap):
#		#print(self.api.VerifyCredentials())
#		#search = self.api.GetSearch(record[namesmap["title_attribute"]])
#		#for tweet in search:
#		#	print(tweet.id, twwet.text)
#		return 0
#
#	def mean(self, scores):
#		return 0
#
#	def __str__(self):
#		return "twittersearch_related"
#

class morfological_complexity:
	''' stanford parser: complexity of the sentences parsing tree '''

	def __init__(self, namesmap):
		self.namesmap = namesmap
		# stanford parser setup
		parser_base_dir = "/home/debian/UNIMI/InformationRetrieval/PROGETTO/fake-news/parser/stanford-parser-full-2018-02-27"
		modelpath = model_path=parser_base_dir + "/englishPCFG.ser.gz"
		os.environ['CLASSPATH'] = parser_base_dir
		os.environ['STANFORD_PARSER'] = parser_base_dir
		os.environ['STANFORD_MODELS'] = parser_base_dir
		self.parser = stanford.StanfordParser(model_path=modelpath, encoding='utf8')
		# parameters: sentences must be split for raw_parse_sents
		self.endsentence_punctuation_regex = "[.?!]+"
		self.min_text = 3

	def score(self, record):
		# converts to unicode-utf8 for compatibility problems with python2 (& splits sentences)
		sentences = [sentence for sentence in \
			re.split(self.endsentence_punctuation_regex, unicode(record[self.namesmap["text_attribute"]], "utf-8")) \
			if len(sentence) >= self.min_text]
		# parse tree of every sentence in the record
		parse_tree = self.parser.raw_parse_sents(sentences)
		# reduce sentences heights with max
		return functools.reduce(lambda x, y: max(x, y), itertools.chain(*[[sentence.height() for sentence in line] for line in parse_tree]))

	def mean(self, unreliable_scores, reliable_scores):
		tot = []
		tot.extend(unreliable_scores)
		tot.extend(reliable_scores)
		max_of_all = max(tot)
		# mean / max_of_all + normalized stddev for unreliable and reliable
		unreliable_mean = float(sum(unreliable_scores) / len(unreliable_scores))
		reliable_mean = float(sum(reliable_scores) / len(reliable_scores))
		return ("m {:.4}, std {:.4}".format(unreliable_mean / max_of_all, numpy.std(numpy.array(unreliable_scores)) / unreliable_mean), \
			"m {:.4}, std {:.4}".format(reliable_mean / max_of_all, numpy.std(numpy.array(reliable_scores)) / reliable_mean))

	def __str__(self):
		return "morfological_complexity"


class lexical_variety:
	''' pattern.metrics.ttr: average percentage of unique words (types)
		for each n successive words (tokens) in the text.
		https://www.clips.uantwerpen.be/pages/pattern-metrics'''

	def __init__(self, namesmap):
		# min text length
		self.min_text = 3
		self.namesmap = namesmap

	def score(self, record):
		# applies ttr function to "text", with n the number of distinct tokens (use a tokenizer ?)
		# checks for the text not being a string or "empty"
		return ttr(record["text"], n=len(re.split("\W+", record[self.namesmap["text_attribute"]]))) \
			if isinstance(record["text"], str) and len(record[self.namesmap["text_attribute"]]) > self.min_text \
			else 0

	def mean(self, unreliable_scores, reliable_scores):
		tot = []
		tot.extend(unreliable_scores)
		tot.extend(reliable_scores)
		max_of_all = max(tot)
		# mean / max_of_all + normalized stddev for unreliable and reliable
		unreliable_mean = (sum(unreliable_scores) / len(unreliable_scores))
		reliable_mean = (sum(reliable_scores) / len(reliable_scores))
		return ("m {:.4}, std {:.4}".format(unreliable_mean / max_of_all, numpy.std(numpy.array(unreliable_scores)) / unreliable_mean), \
			"m {:.4}, std {:.4}".format(reliable_mean / max_of_all, numpy.std(numpy.array(reliable_scores)) / reliable_mean))

	def __str__(self):
		return "lexical_variety"
