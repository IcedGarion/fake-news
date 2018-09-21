import time

# non serve piu' stampare i risultati: scrivi un nuovo file notebook python che plotta il file prodotto da questo .py
# quindi non serve piu' neanche il metodo "mean" delle features!
# Il file sara' un csv, con una riga per ogni record, in cui ogni riga e':
# id_record, label (fake/non), score_feature1, score_feature2, score_featuren
# se usi una sola feature per run, e vuoi mettere i risultati in una nuova colonna (score_feature_k) insieme ad un file di out gia' esistente,
# devi farlo a mano!

# mettere la scrittura file nel ciclo; scrivere il nuovo notebook.


''' DATASET IMPORT '''
from Dataset import *
dataset = kagglecontest_dataset()


''' FEATURES IMPORT '''
import Features, inspect
feats = []
# se importi una classe in Features.py, compare anche qua... Da sistemare! magari estendere una superclasse Feature, e fare qua controllo tipo
for name, obj in inspect.getmembers(Features):
	if inspect.isclass(obj):
		feats.append(obj(dataset.namesmap))



''' OUT FILE '''
# apri il file di out con pandas (tipo out/results.csv)



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
	print("Processing records... (CTRL^C to stop)")
	for record in dataset:
		try:
			# record: reliable or not?
			reliable = record[dataset.namesmap["fake_attribute"]]
			print("Record {}... ({})".format(i, reliable))
			if reliable == dataset.namesmap["nonfake_label"]:
				reliable_count += 1
			elif reliable == dataset.namesmap["fake_label"]:
				unreliable_count += 1
			else:
				unknown_count += 1

			# applying feature's method "score" and passing the dataset's records attributes names (namesmap)
			for feature in feats:
				results[str(feature)][record[dataset.namesmap["fake_attribute"]]].append(feature.score(record))
# qua scrivi il risultato su file, invece che in memoria... scrivi record per record su file mentre calcola, non tutto alla fine!
# usa pandas.write_csv o qialcosa di simile

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
	print("\nSkipping...")




# non serve piu' stampare i risultati: scrivi un nuovo file notebook python che plotta il file prodotto da questo .py
# quindi non serve piu' neanche il metodo "mean" delle features!
# Il file sara' un csv, con una riga per ogni record, in cui ogni riga e':
# id_record, label (fake/non), score_feature1, score_feature2, score_featuren
# se usi una sola feature per run, e vuoi mettere i risultati in una nuova colonna (score_feature_k) insieme ad un file di out gia' esistente,
# devi farlo a mano!


''' RESULTS REDUCING & FORMATTING '''
#print("Done! Printing results\n")
#formt = "{:^" + str(output_tab_width) + "}"
#output_tab_width = 20
## applying feature's method "mean": passa 2 liste (scores unreliable e scores reliables; ottiene tupla (mean_unreliable, mean_reliable)
#reduced_results = [f.mean(results[str(f)][dataset.namesmap["fake_label"]], results[str(f)][dataset.namesmap["nonfake_label"]]) for f in feats]
#
#print("\t\t\t" + "\t\t".join([str(f) for f in feats]))
#print("(" + str(unreliable_count) + ") unreliable\t" + "\t".join([formt.format(result[0]) for result in reduced_results]))
#print("(" + str(reliable_count) + ") reliable\t\t" + "\t".join([formt.format(result[1]) for result in reduced_results]))
#print("\n" + str(unknown_count) + " unknown\n" + str(skipped_count) + " skipped\n" + str(i) + " processed records")
