import sys

''' SYSTEM PARAMETERS '''
# 20800 records nel dataset; vanno limitati, altrimenti non finisce piu' (12+ sec a record)
max_records = 4 if len(sys.argv) < 2 else int(sys.argv[1])
output_tab_width = 20
dataset_path = "/home/debian/UNIMI/InformationRetrieval/PROGETTO/fake-news/data/train.csv"


''' DATASET IMPORT '''
from Dataset import *
dataset = kagglecontest_dataset(dataset_path)


''' FEATURES IMPORT '''
import Features, inspect
feats = []
for name, obj in inspect.getmembers(Features):	# se importi una classe in Features.py, compare anche qua... evita :(
	if inspect.isclass(obj):
		feats.append(obj())


''' FEATURES EXPLORATION
	applying features to the dataset '''
# results: { feature x: { reliables: [ 0.1, 0.2, 0.3, ...], unreliables: [ 0,4, 0.5, 0.6, ...] } }
results = { str(feat): { 0: [], 1: []} for feat in feats }
try:
	print("Processing records...")
	for i, record in enumerate(dataset):
		print("Record {}... ({})".format(i, record["label"]))
		for feature in feats:
			# applying feature's method "score"
			results[str(feature)][record["label"]].append(feature.score(record))

		# BREAK PER TROPPI RECORDS
		if i >= max_records:
			break
except KeyboardInterrupt:
	print("\nSkipping...")


''' RESULTS REDUCING & FORMATTING '''
print("Done! Printing results\n")
formt = "{:^" + str(output_tab_width) + ".5}"
print("\t\t" + "\t\t".join([str(f) for f in feats]))
# applying feature's method "mean"
print("unreliable\t" + "\t".join([formt.format(str(f.mean(results[str(f)][1]))) for f in feats]))
print("reliable\t" + "\t".join([formt.format(str(f.mean(results[str(f)][0]))) for f in feats]))

