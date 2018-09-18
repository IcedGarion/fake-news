import pandas

def kagglecontest_dataset(path):
	''' DATASET: provide iterator over csv file
		record is dict: { attribute_name: attribute_value }'''
        corpus = pandas.read_csv(path, low_memory=False)
        attributes = corpus.keys()
        values = corpus.values
        for record in values:
                yield ({ name: value for name, value in zip(attributes, record)})
