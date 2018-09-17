import pandas

def dataset(path):
        corpus = pandas.read_csv(path, low_memory=False)
        attributes = corpus.keys()
        values = corpus.values
        for record in values:
                yield ({ name: value for name, value in zip(attributes, record)})
