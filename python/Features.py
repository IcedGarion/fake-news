''' Features class with score(record) and mean() methods.
	each feature must return a score based on a record:

	id: unique id for a news article
	title: the title of a news article
	author: author of the news article
	text: the text of the article; could be incomplete
	label: a label that marks the article as potentially unreliable
	    1: unreliable
	    0: reliable
'''

from pattern.metrics import ttr


#class morfological_complexity:
#	def score(record):
#		return 0

#	def mean():
#		return lambda x, y: (x+y) / 2


# average percentage of unique words (types) for each n successive words (tokens) in the text.
class lexical_variety:
	def score(self, record):
		#return pattern.en.metrics.ttr(record["text"], n=100, punctuation='.,;:!?()[]{}`''\"@#$^&*+-|=~_')
		return ttr(record["text"], punctuation='.,;:!?()[]{}`''\"@#$^&*+-|=~_')

	def mean():
		return lambda x, y: (x+y) / 2

	def __str__(self):
		return "lexical_variety"
