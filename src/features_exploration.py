import os, time, pandas

# output: un file csv per ogni feature, una riga per ogni record, in cui ogni riga e':
# id_record, label (fake/non), score_feature_x

''' DATASET IMPORT '''
from Dataset import *
dataset = kagglecontest_dataset(13049)


''' FEATURES IMPORT '''
import Features, inspect
feats = []
# imports only the subclasses of "Feature"
for name, obj in inspect.getmembers(Features):
	if inspect.isclass(obj) and issubclass(obj, Features.Feature) and obj != Features.Feature:
		feats.append(obj(dataset.namesmap))
print("Features found: {}".format([str(feature) for feature in feats]))


''' RESULTS FILES
	opens a file for each feature, naming them with a counter
	+ writes the column names in each file'''
out_path = ".." + os.sep + "out" + os.sep
preexistents = os.listdir(out_path)
out_files = []
for feature in feats:
	filename = str(feature)
	out_files.append(filename)
	if filename not in preexistents:
		f = open(out_path + filename, 'w')
		f.write("id,label," + str(feature) + "\n")
		f.close()
print("Writing output results to {}".format([out_path + str(feature) for feature in feats]))


''' FEATURES EXPLORATION
	applying features to the dataset '''
# results: { feature x: { unreliables: [ 0.1, 0.2, 0.3, ...], reliables: [ 0,4, 0.5, 0.6, ...] } }
results = { str(feat): { dataset.namesmap["fake_label"]: [], dataset.namesmap["nonfake_label"]: []} for feat in feats }
skipped_count = 0
count = 0

try:
	print("\nProcessing records... (CTRL^C to stop)")
	for record in dataset:
		try:
			print("Record {}...".format(count))
			count += 1

			# applying feature's method "score" and writing the results to the right files
			for i, feature in enumerate(feats):
				# record: fake or not?
				label = "fake" if record[dataset.namesmap["fake_attribute"]] == dataset.namesmap["fake_label"] \
					else "not_fake"
				dataframe = { "id": record[dataset.namesmap["id_attribute"]], \
						"label": label, \
						str(feature): feature.score(record) }
				pandas.DataFrame.from_records([dataframe], index="id").to_csv(out_path + out_files[i], header=False, mode='a', \
								columns=["label", str(feature)])

		# anything not ok (empty record / text): skip
		except Exception as e:
			print(e)
			# twitter rate limit exceeded: wait 15 min
			try:
				if e.message[0]["code"] == 88:
					print("Waiting for limit to restore...")
					for t in range(0, 15):
						print("Sleeping for 1 minute... {} to go".format(15-t))
						time.sleep(60)
			except Exception:
				print(e)

			skipped_count += 1
			continue

except KeyboardInterrupt:
	skipped_count += 1
	print("\n\nSkipping...")


print("{} records processed.\nWritten {} lines in files: {}{}".format(count, (count-skipped_count), out_path, [str(feature) for feature in feats]))
