import sys

''' SYSTEM PARAMETERS
	call with # of records to be processed, or CTRL^C'''
# 20800 records nel dataset; vanno limitati, altrimenti non finisce piu' (12+ sec a record)
max_records = 4 if len(sys.argv) < 2 else int(sys.argv[1])
output_tab_width = 20


''' DATASET IMPORT '''
from Dataset import *
dataset = kagglecontest_dataset()


''' FEATURES IMPORT '''
import Features, inspect
feats = []
for name, obj in inspect.getmembers(Features):	# se importi una classe in Features.py, compare anche qua... evita :(
	if inspect.isclass(obj):
		feats.append(obj())


''' FEATURES EXPLORATION
	applying features to the dataset '''
# results: { feature x: { unreliables: [ 0.1, 0.2, 0.3, ...], reliables: [ 0,4, 0.5, 0.6, ...] } }
results = { str(feat): { dataset.namesmap["fake_label"]: [], dataset.namesmap["nonfake_label"]: []} for feat in feats }
try:
	print("Processing records...")
	for i, record in enumerate(dataset):
		print("Record {}... ({})".format(i, record[dataset.namesmap["fake_attribute"]]))
		for feature in feats:
			# applying feature's method "score" and passing the dataset's records attributes names (namesmap)
			results[str(feature)][record[dataset.namesmap["fake_attribute"]]].append(feature.score(record, dataset.namesmap))

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
print("unreliable\t" + "\t".join([formt.format(str(f.mean(results[str(f)][dataset.namesmap["fake_label"]]))) for f in feats]))
print("reliable\t" + "\t".join([formt.format(str(f.mean(results[str(f)][dataset.namesmap["nonfake_label"]]))) for f in feats]))

