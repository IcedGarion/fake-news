# CONFIGURATIONS

* stanford parser path: python/Features.py -> `morfological_complexity.__init__` (parser_base_dir)
* dataset path: python/Dataset.py -> `kagglecontest_dataset.__init__` (dataset_path)
* twitter API tokens: python/Features.py -> `twitter_search.__init__`
* results table width (when adding / removing features): python/`features_exploration.py.out_tab_width`
* Call with number of rcords to be processed: `python python/features_exploration.py 20`


# PARAMETERS

* morfological_complexity:
	* stanford_parser.raw_parse_sents / parse_sents ?
	* raw_parse_sents si aspetta una lista di frasi: bisogna splittare le frasi del tweet; e' stato fatto con
	   una regex endsentence_punctuation, che potrebbe cambiare
	* SCORE: Una volta ottenuto il parse tree, e' stato usato il metodo height su ogni Tree di frase:
	   essendoci molte frasi in un record, e' stato tenuto il valore massimo fra tutte le frasi nel rec,
	   ma si puo' provare anche con media, o altre metriche.
	   Per ora: valore max fra le profondita' delle frasi di tutto il record
	* MEAN: Per mettere insieme tutti i valori dei reliable / unreliable, e ottenere un numero fra 0 e 1, (in "mean")
	   e' stata usata una funzione tipo: (sum(scores) / len(scores)) / max(scores)
	   Ma si puo' cambiare

* lexical_variety:
	* SCORE: utilizata la funzione pattern.metrics.ttr sul testo del tweet; prende in input
	   punctuation (default) e n numero di tokens del testo: usata una regex per splittare con \W+,
	   ma puo' cambiare regex oppure usare un tokenizer per fare il conto
	* MEAN: per ridurre i risultati di reliable / unreliable ad un unico valore 0-1, e' stata usata
	   una semplice media aritmetica, ma si puo' cambiare


# SYSTEM

* Main: features_extraction.py
  Carica il dataset scelto, prepara le strutture dati, acquisisce tutte le features scritte nel file Features.py e poi fa scorrere tutti i record
  Per ogni record, chiama tutte le features presenti, passandogli il record stesso (e una mappa contenente i nomi dei campi, presa dal dataset).
  Le features produrranno uno SCORE basato sul record, e il main file salva li tutti nella struttura dati results.
  Finiti i records (ci mette troppo; impostare un valore massimo di records passando un argomento numerico al programma, oppure CTRL^C mentre va),
  si avra' una struttura con una lista di score per le reliable e una lista di scores per le unreliable, per ogni features.
  Vengono divise due liste con le scores di notizie reliable e unreliable (fake). Poi queste 2 liste vengono passate a tutte le features:
  ognuna le riduce ad un singolo valore con il metodo MEAN.
  Poi il risultato viene presentato in una tabella, nella quale, per ogni feature, viene affiancata la media per le notizie reliable alla media
  per le notizie unreliable.

* Features: Features.py
  In questo file, tutte le "class ...x" presenti verranno caricate come features da utilizzare.
  Ogni class feature deve avere almeno 2 metodi: score e mean (init senza parametri per inizializzare e --str-- per il nome della feature).
  SCORE deve ritornare un valore fra 0 e 1, che rappresenta il valore di quella feature applicato a quel record. Le features possono fare
  qualsiasi tipo di operazione sui campi del record e vengono aiutate da namesmap, dict che indica il nome degli attributi del record da usare.
  MEAN indica come raggruppare tutti i valore di score per produrre un unico rappresentante per le classi di notizie reliable e unreliable.
  lavora sulle 2 liste separate di scores, e deve produrre una sorta di media (sempre fra 0 e 1)
  Volendo quindi aggiungere una feature, basta scrivere una nuova class_y con i metodi score, mean e --str-- che ritornano quanto specificato.
  Per i parametri basta guardare quelle gia' presenti; per escludere una feature dalla computazione, commentarla.

* Dataset: Dataset.py
  Contiene i vari dataset (uno, per ora). Ogni dataset e' un iteratore (--iter--) che fornisce, uno per uno, i record presenti in un certo file o
  database. La classe dataset inoltre contiene un attributo self.namesmap che indica il mappaggio fra i nomi degli attributi.
  Volendo aggiungere un nuovo dataset, basta scrivere una nuova class dataset_x con il metodo --iter-- che fa yield record per record;
  poi un attributo namesmap, dict che associa i nomi standard degli attributi usati nel main (vedere namesmap gia' presenti) coi nomi veri delle
  "colonne" presenti nel file usato dal dataset;
  poi, nel main features_extraction.py, modificare la riga dataset = dataset_y() con dataset = dataset_che_si_vuole_usare


==================================================================================================================================================

# REQUISITES

## ESPLORAZIONE FEATURES

Preso un dataset da kaggle (esempio: https://www.kaggle.com/c/fake-news/data),
con notizie vere e false (annotate reliable / unreliable), estrarre diverse features dai testi:


**1 - NLP:**

* varieta' lessicale: numero vocaboli diversi, rapportato al resto del corpus
* complessita' morfologica: profondita' dell'albero di parsing della frase (e non solo, 
  prova anche altre cose piu' fini)

**2 - FONTI ESTERNE:**

Per ogni news, usa il titolo (o una parte del testo) come ricerca per le api di twitter,
per trovare il numero di tweet inerenti alla notizia.


**SCOPRIRE SE:**

Ci sono significativamente piu' (o meno) tweet correlati a notizie vere o correlati a quelle false?
E quindi i tweet corrrelati sono una buona feature per discriminare le notizie vere da quelle false?

Le fake news si possono riconoscere grazie ad una complessita' lessicale / morfologica particolarmente
alta / bassa rispetto alle notizie vere?


**COME FARE**

Una volta estratte le features di cui sopra (che devono dare come risultato un numero 0/1), applicarle
a tutte le notizie vere e tutte quelle false del dataset, dopo aver aggregato con medie, e poi
produrre una tabella:

type of news | feature1 | feature2 | feature3
------------ | -------- | -------- | --------
reliable | 0.2 | 0.3 | 0.4
unreliable | 0.21 | 0.3 | 0.9

(come ridurre la lista di scores in un valore solo, e' specificato nella feature stessa "mean")

Cosi' si nota se una certa feature ha un valore molto diverso fra notizie vere e false.
Cerca di ottenere una feature che si comporta cosi', in modo da poi poterla approfondire.


**SISTEMA**

Cercare di scrivere un codice che permetta facilmente di testare, di inserire nuove features
quando si vuole e di poterle provare producendo una tabella. (esempio, ogni feature e' una
classe che estende una superclasse feature).

