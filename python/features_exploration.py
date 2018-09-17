''' DATASET IMPORT '''
from Dataset import dataset
dataset_path = "../data/train.csv"
data = dataset(dataset_path)


''' FEATURES IMPORT '''
import Features, inspect

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
		results[str(feature)][record["label"]].append(feature.score(record))
	break
	# DA TOGLIERE IL BREAK!!!!!!!!

''' RESULTS REDUCING & FORMATTING '''
print("\t\t" + "\t".join([str(f) for f in feats]))
print("unreliable\t" + "\t".join([str(f.mean(results[str(f)][1])) for f in feats]))
print("reliable\t" + "\t".join([str(f.mean(results[str(f)][0])) for f in feats]))

