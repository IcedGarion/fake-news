''' DATASET: provide iterator over csv file
	record is dict: { attribute_name: attribute_value }
'''

import pandas

class kagglecontest_dataset:
	'''	RECORD structure:
	        id: unique id for a news article
	        title: the title of a news article
	        author: author of the news article
	        text: the text of the article; could be incomplete
	        label: a label that marks the article as potentially unreliable
	            1: unreliable
	            0: reliable
	'''
	def __init__(self, path):
		data = pandas.read_csv(path, low_memory=False)
		self.attributes = data.keys()
		self.values = data.values

	def __iter__(self):
		for record in self.values:
			yield ({ name: value for name, value in zip(self.attributes, record)})
