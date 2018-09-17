ESPLORAZIONE FEATURES 

Preso un dataset da kaggle (esempio: https://www.kaggle.com/c/fake-news/data),
con notizie vere e false (annotate reliable / unreliable), estrarre diverse features dai testi:

1 - NLP:
- varieta' lessicale: numero vocaboli diversi, rapportato al resto del corpus
- complessita' morfologica: profondita' dell'albero di parsing della frase (e non solo, 
  prova anche altre cose piu' fini)

2 - FONTI ESTERNE:
Per ogni news, usa il titolo (o una parte del testo) come ricerca per le api di twitter,
per trovare il numero di tweet inerenti alla notizia.


SCOPRIRE SE:
Ci sono significativamente piu' (o meno) tweet correlati a notizie vere o correlati a quelle false?
E quindi i tweet corrrelati sono una buona feature per discriminare le notizie vere da quelle false?

Le fake news si possono riconoscere grazie ad una complessita' lessicale / morfologica particolarmente
alta / bassa rispetto alle notizie vere?


COME FARE
Una volta estratte le features di cui sopra (che devono dare come risultato un numero 0/1), applicarle
a tutte le notizie vere e tutte quelle false del dataset, dopo aver aggregato con medie, e poi
produrre una tabella:

		feature1	feature2	feature3
								(come ridurre la lista di scores in un valore solo,
reliable	0.2		0.3		0.1		  specificato nella feature stessa)
unreliable	0.21		0.3		0.9


Cosi' si nota se una certa feature ha un valore molto diverso fra notizie vere e false.
Cerca di ottenere una feature che si comporta cosi', in modo da poi poterla approfondire.


SISTEMA
Cercare di scrivere un codice che permetta facilmente di testare, di inserire nuove features
quando si vuole e di poterle provare producendo una tabella. (esempio, ogni feature e' una
classe che estende una superclasse feature).
