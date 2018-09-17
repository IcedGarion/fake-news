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

from pattern.metrics import ttr
import re

#class morfological_complexity:
#	def score(record):
#		return 0

#	def mean():
#		return lambda x, y: (x+y) / 2


class lexical_variety:
	''' pattern.metrics.ttr: average percentage of unique words (types)
		for each n successive words (tokens) in the text. '''

	def __init__(self):
		self.min_text = 3

	def score(self, record):
		return ttr(record["text"], n=len(re.split("\W+", record["text"]))) \
			if isinstance(record["text"], str) and len(record["text"]) > self.min_text \
			else 0

	def mean(self, scores):
		return sum(scores) / len(scores)

	def __str__(self):
		return "lexical_variety"
