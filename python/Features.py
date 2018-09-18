''' Features class with score(record) and mean(scores) methods.
	each feature returns a score based on a record (and a dict for dataset column names),
	and has a method for reducing the list of obtained scores
	into a single value.
'''
''' want to plug in / out a feature? Simply write a new class or comment / uncomment it '''

from nltk.parse import stanford
from pattern.metrics import ttr
import re, os, twitter, functools, itertools


class twittersearch_related:
	def __init__(self):
		pass
		#self.api =twitter.Api(consumer_key="123", \
		#		consumer_secret="123", \
		#		access_token_key="123", \
		#		access_token_secret="123")

	def score(self, record, namesmap):
		#print(self.api.VerifyCredentials())
		#search = self.api.GetSearch(record[namesmap["title_attribute"]])
		#for tweet in search:
		#	print(tweet.id, twwet.text)
		return 0

	def mean(self, scores):
		return 0

	def __str__(self):
		return "twittersearch_related"


class morfological_complexity:
	''' stanford parser: complexity of the sentences parsing tree '''

	def __init__(self):
		# stanford parser setup
		parser_base_dir = "/home/debian/UNIMI/InformationRetrieval/PROGETTO/fake-news/parser/stanford-parser-full-2018-02-27"
		modelpath = model_path=parser_base_dir + "/englishPCFG.ser.gz"
		os.environ['CLASSPATH'] = parser_base_dir
		os.environ['STANFORD_PARSER'] = parser_base_dir
		os.environ['STANFORD_MODELS'] = parser_base_dir
		self.parser = stanford.StanfordParser(model_path=modelpath, encoding='utf8')
		# parameters: sentences must be split for raw_parse_sents
		self.endsentence_punctuation_regex = "[.?!]+"

	def score(self, record, namesmap):
		# converts to unicode-utf8 for compatibility problems with python2 (& splits sentences)
		sentences = re.split(self.endsentence_punctuation_regex, unicode(record[namesmap["text_attribute"]], "utf-8"))
		# parse tree of every sentence in the record
		parse_tree = self.parser.raw_parse_sents(sentences)
		# reduce sentences heights with max
		return functools.reduce(lambda x, y: max(x, y), itertools.chain(*[[sentence.height() for sentence in line] for line in parse_tree]))

	def mean(self, scores):
		return (float(sum(scores)) / len(scores)) / max(scores)

	def __str__(self):
		return "morfological_complexity"


class lexical_variety:
	''' pattern.metrics.ttr: average percentage of unique words (types)
		for each n successive words (tokens) in the text.
		https://www.clips.uantwerpen.be/pages/pattern-metrics'''

	def __init__(self):
		# min text length
		self.min_text = 3

	def score(self, record, namesmap):
		# applies ttr function to "text", with n the number of distinct tokens (use a tokenizer ?)
		# checks for the text not being a string or "empty"
		return ttr(record["text"], n=len(re.split("\W+", record[namesmap["text_attribute"]]))) \
			if isinstance(record["text"], str) and len(record[namesmap["text_attribute"]]) > self.min_text \
			else 0

	def mean(self, scores):
		return sum(scores) / len(scores)

	def __str__(self):
		return "lexical_variety"
