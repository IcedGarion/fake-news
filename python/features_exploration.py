import pandas, inspect


''' DATASET IMPORT '''
from Dataset import dataset
dataset_path = "../data/train.csv"
data = dataset(dataset_path)


''' FEATURES IMPORT '''
import Features

feats = []
for name, obj in inspect.getmembers(Features):
	if inspect.isclass(obj):
		feats.append(obj())



''' FEATURES EXPLORATION
	applying features on the dataset '''
# results: { feature x: { reliables: [ 0.1, 0.2, 0.3, ...], unreliables: [ 0,4, 0.5, 0.6, ...] } }
results = { str(feat): { 0: [], 1: []} for feat in feats }
for record in data:
	for feature in feats:
		#print(feature.score(record))
		results[str(feature)][record["label"]].append(feature.score(record))
	break


''' RESULTS FORMATTING '''
print(results)
