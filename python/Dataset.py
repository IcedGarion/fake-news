''' DATASET: provide iterator over csv file
	record is dict: { attribute_name: attribute_value }
'''

import pandas

def kagglecontest_dataset(path):
	'''	RECORD structure:
	        id: unique id for a news article
	        title: the title of a news article
	        author: author of the news article
	        text: the text of the article; could be incomplete
	        label: a label that marks the article as potentially unreliable
	            1: unreliable
	            0: reliable
	'''
        corpus = pandas.read_csv(path, low_memory=False)
        attributes = corpus.keys()
        values = corpus.values
        for record in values:
                yield ({ name: value for name, value in zip(attributes, record)})
