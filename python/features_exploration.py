import sys, time

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
		feats.append(obj(dataset.namesmap))


''' FEATURES EXPLORATION
	applying features to the dataset '''
# results: { feature x: { unreliables: [ 0.1, 0.2, 0.3, ...], reliables: [ 0,4, 0.5, 0.6, ...] } }
results = { str(feat): { dataset.namesmap["fake_label"]: [], dataset.namesmap["nonfake_label"]: []} for feat in feats }
reliable_count = 0
unreliable_count = 0
unknown_count = 0
skipped_count = 0
i = 0
try:
	print("Processing records...")
	for record in dataset:
		try:
			# record: reliable or not?
			reliable = record[dataset.namesmap["fake_attribute"]]
#			print("Record {}... ({})".format(i, reliable))
			if reliable == dataset.namesmap["nonfake_label"]:
				reliable_count += 1
			elif reliable == dataset.namesmap["fake_label"]:
				unreliable_count += 1
			else:
				unknown_count += 1

			# applying feature's method "score" and passing the dataset's records attributes names (namesmap)
			for feature in feats:
				results[str(feature)][record[dataset.namesmap["fake_attribute"]]].append(feature.score(record))

			# BREAK PER TROPPI RECORDS
			i += 1
			if i >= max_records:
					break

		# anything not ok (empty record / text): skip
		except Exception as e:
			print(e)
			# twitter rate limit exceeded: wait 15 min
			try:
				if e.message[0]["code"] == 88:
					print("Waiting for limit to restore... (record {})".format(i))
					for t in range(0, 15):
#						print("Sleeping for 1 minute... {} to go".format(15-t))
						time.sleep(60)
			except Exception:
				print(e)

			skipped_count += 1
			continue

except KeyboardInterrupt:
	skipped_count += 1
	print("\nSkipping...")


''' RESULTS REDUCING & FORMATTING '''
print("Done! Printing results\n")
formt = "{:^" + str(output_tab_width) + "}"
# applying feature's method "mean": passa 2 liste (scores unreliable e scores reliables; ottiene tupla (mean_unreliable, mean_reliable)
reduced_results = [f.mean(results[str(f)][dataset.namesmap["fake_label"]], results[str(f)][dataset.namesmap["nonfake_label"]]) for f in feats]

print("\t\t\t" + "\t\t".join([str(f) for f in feats]))
print("(" + str(unreliable_count) + ") unreliable\t" + "\t".join([formt.format(result[0]) for result in reduced_results]))
print("(" + str(reliable_count) + ") reliable\t\t" + "\t".join([formt.format(result[1]) for result in reduced_results]))
print("\n" + str(unknown_count) + " unknown\n" + str(skipped_count) + " skipped\n" + str(i) + " processed records")
