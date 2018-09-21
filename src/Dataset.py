''' DATASET: provide iterator over csv file
	and namesmap: mapping between standard names used and real attribute names
	record is dict: { attribute_name: attribute_value }
'''
''' want to plug in a new dataset? provide an iterator and a namesmap, like below,
	then switch the dataset name in the main features_exploration.py '''

import pandas

class kagglecontest_dataset:
	'''	https://www.kaggle.com/c/fake-news/data
		RECORD structure:
	        id: unique id for a news article
	        title: the title of a news article
	        author: author of the news article
	        text: the text of the article; could be incomplete
	        label: a label that marks the article as potentially unreliable
	            1: unreliable
	            0: reliable
	'''
	def __init__(self, first_record=8000):
		self.first_record = first_record
		# csv import
		dataset_path = "/home/debian/UNIMI/InformationRetrieval/PROGETTO/fake-news/data/train.csv"
		data = pandas.read_csv(dataset_path, low_memory=False)
		self.attributes = data.keys()
		self.values = data.values
		# namesmap: label for the "reliable" / "unreliable" attribute, value for "unreliable", value for "reliable", label for "text"
		self.namesmap = { "fake_attribute": "label", "fake_label": 1, "nonfake_label": 0, \
				"text_attribute": "text", "title_attribute": "title" }


	# riparte dal record 3363: cambiare
	def __iter__(self):
		for i, record in enumerate(self.values):
			if i > self.first_record:
				yield ({ name: value for name, value in zip(self.attributes, record)})
