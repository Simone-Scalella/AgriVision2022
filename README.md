# Forecasting vegetation indexes and yield prediction to monitor agricultural fields.

# Obiettivi

Il progetto per il corso di computer vision e deep learning dell'anno accademico 2021/2022, ha due obiettivi principali. Il primo è quello di fare previsione di indici vegetali. Il secondo è quello di predire la resa del campo agricolo.

# Creazione del dataset

## Recupero delle immagini

Per acquisire le immagini dei campi agricoli abbiamo utilizzato sentinel hub [(link)](https://www.sentinel-hub.com/).
Utilizzando uno script fornito dal professore abbiamo potuto scaricare le immagini dei campi, tali immagini vengono salvate nel formato .tiff, e hanno 12 bande. Di seguito riportiamo un piccolo esempio dello script utilizzato.

```
function setup() {
  return {
    input: [{
      bands: ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"],
      units: "DN"
    }],
    output: {
      id: "default",
      bands: 12,
      sampleType: SampleType.UINT16
    }
  }
}
```
Il resto dello script è visibile in questo [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/ScaricaDataset.ipynb).
Oltre alle immagini il nostro dataset di partenza aveva anche una cartella scl e una cartella yield all'interno delle quali sono presenti altre immagini che utilizzeremo e descriveremo successivamente.
Di seguito riportiamo un esempio di immagine dei campi agricoli.

![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/campi.png)

Una volta scaricate tutte le immagini si è proceduto utilizzando la libreria gdal per aprire le immagini all'interno del file jupyter, e abbiamo iniziato a studiarne le dimensioni per proseguire con la fase di etl. Dall'analisi è emerso che tutte le immagini hanno le stesse dimensioni. Di seguito riportiamo le dodici bande di un'immagine del campo agricolo.

Bande dei campi: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/bande_raw.png)

## Visualizzazione delle serie temporali

Successivamente si è proceduto a creare una prima bozza delle serie temporali, per capire quali operazioni di etl erano necessario. Come prima cosa le immagini dei campi sono state ordinate sull'asse temporale; successivamente, si è creata una struttura dati a quattro dimensioni, che sono l'asse delle x, delle y, delle bande e del tempo, e al suo interno, seguendo l'ordine temporale definito precedentemente, sono state inserite tutte le immagini con le loro bande.
Al termine di questa operazione siamo andati a calcolare gli indici vegetali d'interesse, che sono l'[NDVI](https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/id_58.js) e l'[NDRE](https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/id_223.js). Tale calcolo avviene combinando tra loro alcune bande appartenenti alle immagini dei campi.
Successivamente si è proceduto con il calcolo dell'andamento medio degli indici, in quanto ogni pixel ha la sua serie temporale.
Di seguito riportiamo le due serie temporali.

Indice NDVI non pulito: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/ndvi_raw.png)

Indice NDRE non pulito: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/ndre_raw.png)

Dalle immagini è possibile osservare diverse problematiche legate al fatto che i dati non sono stati puliti; infatti, nonostante gli indici abbiano un valore compreso tra -1 e 1, è possibile osservare dei picchi di valore molto superiore, inoltre, il picco massimo dovrebbe essere a Maggio, e noi lo troviamo molto prima. Ci sono altri picchi con valori anomali, e, infine, l'andamento degli indici durante l'anno è sbagliato.
Terminata questa prima fase di creazione e analisi del dataset procediamo con la fase di etl.

# ETL

## Prima fase di ETL

In questa fase si è proceduto con la pulizia del dataset.
All'interno delle immagini sono presenti dei pixel che non dobbiamo tenere in considerazione, infatti, sono immagini del campo agricolo coperte da nuvole, ombre di nuvole, e altre problematiche che invalidano i valori. Per ulteriori informazioni si può utilizzare il seguente [link](https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm).
Per realizzare questa operazione di pulizia abbiamo utilizzato le immagini presenti nella cartella scl, la quale contiene un'immagine dove i valori dei pixel sono associati a una specifica categoria. Questa categoria ci permette di discriminare i pixel non validi, infatti, ad ogni tipo di pixel è associato un valore intero.
Inoltre, abbiamo utilizzato le immagini presenti nella cartella yield. All'interno di questa cartella sono contenuti degli shape file relativi ai campi agricoli; le informazioni contenute in questi campi sono di varia natura, ad esempio abbiamo informazioni relative alla resa, il prodotto secco, etc..
Di seguito riportiamo un esempio di immagini relative alla cartella scl e yield.

Resa dei campi: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/campi_yield.png)

Da questa immagine è possibile osservare come i campi 4 e 6 siano in realtà scomposti in due campi, quindi, utilizzando qgis abbiamo generato i poligoni convessi che rappresentavano tutto il campo.

Immagine scl: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/scl_example.png)

E' possibile osservare come l'immagine scl rappresenti una porzione dell'Italia, quindi, abbiamo bisogno di tagliare solo il pezzo relativo ai di interesse. La seguente immagine mostra le porzioni di interesse.

Area di interesse: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/ritaglio.png)

Prima del taglio abbiamo dovuto effettuare una operazione di riordinamento dei file scl, in qunato si presentavano all'interno di diverse cartelle, quindi si è deciso di spostarle, in maniera ordinata, all'interno di un unica cartella. Il codice utilizzato è nel seguente [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/ETL1.ipynb).
Di seguito carichiamo un'immagine della directory precedente.

Vecchia directory: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/scl_directory.png)

Si è notato che alcune immagini scl avevano i metadati rovinati, quindi, si è proceduto a rigenerarli. Il codice utilizzato è nel seguente [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/ETL1.ipynb).

## Seconda fase di ETL

Durante questa fase siamo andati a tagliare le porzioni d'interesse sia dai file scl che dai file .tiff, usando le coordinate degli shape file. Abbiamo utilizzato il metodo Mask della libreria rasterio [(link)](https://rasterio.readthedocs.io/en/latest/api/rasterio.mask.html), inoltre, per ogni nuova immagine abbiamo dovuto generare dei nuovi metadati. Il codice utilizzato si trova nel seguente [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/ETL2.ipynb).
Al termine di questa operazione ci siamo resi conto che le dimensioni della maschera tagliata erano più piccole rispetto a quelle del campo. Quindi, abbiamo utilizzato la libreria Resampling [(link)](https://rasterio.readthedocs.io/en/latest/topics/resampling.html#resampling-methods), di rasterio. Usando come parametro 'nearest' abbiamo effettuato un operazione di upsampling senza modificare il contenuto informativo della maschera. Al termine dell'esecuzione, le dimensioni delle maschere e dei campi erano uguali.
Di seguito carichiamo un esempio del taglio della maschera (ridimensionata) e del campo.

Maschera e campo: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/mask.png)

A questo punto possiamo applicare la maschera al campo per togliere tutti i pixel che non sono d'interesse per le analisi. Il codice utilizzato si trova nel seguente [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/ETL2.ipynb).
Di seguito carichiamo un esempio di campo filtrato.

Campo filtrato: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/afterMask.png)

A questo punto andiamo, nuovamente, a calcolare gli indici vegetali ndvi e ndre.
Riportiamo di seguito un'immagine sull'andamento dell'ndvi di un pixel.

NDVI dopo la maschera: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/ndvi_mask.png)

Abbiamo eliminato picchi anomali e valori non corretti, però, dobbiamo migliorare la qualità della curva. Per fare questo utilizziamo una funzione di smoothing [(link)](https://github.com/cerlymarco/tsmoothie). Di seguito riportiamo un esempio del risultato ottenuto.

NDVI con smoothing: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/ndvi_smooth.png)

## Terza fase di ETL

In questa fase siamo andati a pulire ulteriormente le curve, e poi, si è effettuata un'operazione di data augmentation.
Dalle curve sono stati eliminati periodi temporali che non erano d'interesse per il progetto e i pixel che avevano sempre valore uguale a zero. Di seguito riportiamo tutte le curve dell'ndvi per ogni pixel, dopo questa operazione di pulizia.

NDVI di tutti i pixel: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/NDVI_4All.png)

Successivamente si è proceduto con l'operazione di data augmentation, utilizzando la libreria scikit-fda [(link)](https://fda.readthedocs.io/en/latest/auto_examples/plot_fpca.html).
La FPCA ci permette di estrarre una funzione continua dalle nostre serie temporali, quindi, abbiamo una curva composta da 150 punti.
Di seguito mostriamo l'immagine della funzione.

FPCA: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/fpca.png)

Ottenuta la funzione procediamo a sommarla a tutti i pixel, in questo modo aumentiamo le dimensioni delle serie temporali.
Il risultato ottenuto non è ideale, possiamo osservare dalla prossima immagine, i picchi relativi ai valori reali, che possono discostare dalla funzione.

Serie temporali più FPCA: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/Fpca%2BTimeSeries.png)

Per risolvere il problema applichiamo nuovamente la funzione di smoothing che abbiamo usato precedentemente.
Di seguito riportiamo le curve dell'indice vegetale che abbiamo ottenuto.

![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/Final%20Time%20Series.png)

La fase di ETL è finita, le curve che abbiamo ottenuto sono pulite e soddisfano tutti i requisiti relativi all'indice vegetale.
Queste curve saranno utilizzate nella fase successiva, che è quella di addestramento dei modelli e previsione.
Le serie temporali sono state salvate in formato pickle per poter essere utilizzate nei file successivi.

# Deep learning

I modelli uttilizzati in questo task sono Neural Prophet, Fb Prophet, GRU e LSTM. Sono state scelte queste reti perchè rappresentano lo stato dell'arte, cioè, sono le reti più moderne e utilizzate per task di forecasting con serie temporali. Abbiamo proceduto nel seguente modo, le reti sono state addestrate con un diverso numero di epoche, tutte le reti sono state addestrate utilizzando la curva media dei pixel, infine, sono state fatte delle previsioni dando in input serie temporali diverse.
L'obiettivo del task è quello di prevedere l'andamento degli indici vegetali, con particolare attenzione al picco massimo, che avviene agli inizi di Maggio. Quindi, le serie temporali date in input al modello, dopo l'addestramento, non saranno mai complete, infatti, saranno troncate prima di 60 giorni, poi di 90, in questo modo andiamo a prevedere il picco massimo, e infine, di 120 giorni, cioè, facciamo previsione con la serie temporale di un solo mese.
Lo scopo è quello di aiutare l'agricoltore, che, se in possesso di queste informazioni, può intervenire, concimando il terreno, per aumentare la resa del suo campo.

## Neural Prophet
Neural Prophet è il successore di Fb Prophet, è una rete deep basata su pytorch, utilizzata per fare forecasting di serie temporali. Si può utilizzare questo [link](https://neuralprophet.com/) per accedere alla documentazione della rete.
Il file in cui abbiamo implementato la rete è il [seguente](https://github.com/Accout-Personal/AgriVision2022/blob/main/NeuralProphet.ipynb).
Riportiamo di seguito i risultati ottenuti con questa rete, le metriche calcolate sono la mean absolute error (MAE), la mean squared error (MSE) e la Root Mean Squared Error (RMSE).

### Risultati

| Metrica | Numero di epoche  | Scostamento | Valore |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 25  | 60 giorni  | 0.019115 |
| MSE  | 25  | 60 giorni  | 0.000503 |
| RMSE  | 25  | 60 giorni  | 0.022428 |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 50  | 60 giorni  | 0.022401 |
| MSE  | 50  | 60 giorni  | 0.000577 |
| RMSE  | 50  | 60 giorni  | 0.024021 |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 100  | 60 giorni  | 0.012909 |
| MSE  | 100  | 60 giorni  | 0.00023 |
| RMSE  | 100  | 60 giorni  | 0.015166 |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 25  | 90 giorni  | 0.015523 |
| MSE  | 25  | 90 giorni  | 0.000322 |
| RMSE  | 25  | 90 giorni  | 0.017944 |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 50  | 90 giorni  | 0.017523 |
| MSE  | 50  | 90 giorni  | 0.000374 |
| RMSE  | 50  | 90 giorni  | 0.019339 |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 100  | 90 giorni  | 0.013353 |
| MSE  | 100  | 90 giorni  | 0.000226 |
| RMSE  | 100  | 90 giorni  | 0.015033 |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 25  | 120 giorni  | 0.009081 |
| MSE  | 25  | 120 giorni  | 0.000146 |
| RMSE  | 25  | 120 giorni  | 0.012083 |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 50  | 120 giorni  | 0.011511 |
| MSE  | 50  | 120 giorni  | 0.000185 |
| RMSE  | 50  | 120 giorni  | 0.013601 |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 100  | 120 giorni  | 0.00995 |
| MSE  | 100  | 120 giorni  | 0.000154 |
| RMSE  | 100  | 120 giorni  | 0.01241 |

Come si può osservare dai valore della tabella, questa rete restituisce dei risultati ottimi, molto vicini a quelli reali.
Di seguito carichiamo un esempio di predizione, dove alla rete è stata data una serie temporale di 30 giorni, e ha predetto i successivi 120 giorni.

Neural Prophet: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/NeuralProphet.png)

## Fb Prophet

Un'altra rete implementata è Fb Prophet, una rete deep che permette di fare previsioni di serie temporali. Si può utilizzare questo [link](https://facebook.github.io/prophet/) per accedere alla documentazione della rete.

Il file in cui abbiamo implementato la rete è il [seguente](https://github.com/Accout-Personal/AgriVision2022/blob/main/ProhetTest.ipynb).
In questo progetto non è stato possibile utilizzare Fb Prophet, in quanto, il framework utilizzato, permette di fare previsioni solo sulla serie temporale utilizzata per l'addestramento. A differenza di Neural Prophet che si addestrava con la curva media, e faceva previsioni su altri pixel.

Sono stati effettuati dei tentativi di previsione con questa rete, prima di scegliere di non utilizzarla.
I test effettuati prevedevano l'addestramento della rete con una serie che era già troncata.
I risultati ottenuti non sono stati soddisfacenti, in quanto la rete prevedeva bene solo dopo il picco.
Di seguito mostriamo un esempio di previsione di Fb Prophet, dopo averlo addestrato con la serie temporale media troncata di 70 giorni, quindi, a ridosso del picco massimo.

Fb Prophet: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/FbProphet.png)

Il modello non riesce a fare una previsione corretta, quindi, si è deciso di non utilizzarlo.

## GRU and LSTM

Altre due reti che sono state utilizzate sono GRU e LSTM. Queste due reti le abbiamo implementate nello stesso file perchè sono simili, infatti, GRU può essere considerata una variante di LSTM, entrambe sono progettate in modo simile, e, in alcuni casi, producono risultati molto simili. Si può utilizzare questo [link]([https://neuralprophet.com/](https://towardsdatascience.com/understanding-gru-networks-2ef37df6c9be)) per accedere alla documentazione delle reti.
Il file in cui abbiamo implementato le rete è il [seguente](https://github.com/Accout-Personal/AgriVision2022/blob/main/LSTM-GRU.ipynb).
Riportiamo di seguito i risultati ottenuti con questa rete, le metriche calcolate sono la mean absolute error (MAE), la mean squared error (MSE) e la Root Mean Squared Error (RMSE).

### Risultati

| Metrica | Numero di epoche  | Scostamento | Valore | Rete |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| MAE  | 25  | 60 giorni  | 0.020991 | LSTM |
| MSE  | 25  | 60 giorni  | 0.000674 | LSTM |
| RMSE  | 25  | 60 giorni  | 0.025962 | LSTM |
| MAE  | 25  | 60 giorni  | 0.026453 | GRU |
| MSE  | 25  | 60 giorni  | 0.001152 | GRU |
| RMSE  | 25  | 60 giorni  | 0.033941 | GRU |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 50  | 60 giorni  | 0.006274 | LSTM |
| MSE  | 50  | 60 giorni  | 6.6e-05 | LSTM |
| RMSE  | 50  | 60 giorni  | 0.008124 | LSTM |
| MAE  | 50  | 60 giorni  | 0.010113 | GRU |
| MSE  | 50  | 60 giorni  | 0.000168 | GRU |
| RMSE  | 50  | 60 giorni  | 0.012961 | GRU |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 100  | 60 giorni  | 0.003114 | LSTM |
| MSE  | 100  | 60 giorni  | 1.2e-05 | LSTM |
| RMSE  | 100  | 60 giorni  | 0.003464 | LSTM |
| MAE  | 100  | 60 giorni  | 0.003113 | GRU |
| MSE  | 100  | 60 giorni  | 1.2e-05 | GRU |
| RMSE  | 100  | 60 giorni  | 0.003464 | GRU |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 25  | 90 giorni  | 0.027625 | LSTM |
| MSE  | 25  | 90 giorni  | 0.001239 | LSTM |
| RMSE  | 25  | 90 giorni  | 0.035199 | LSTM |
| MAE  | 25  | 90 giorni  | 0.034797 | GRU |
| MSE  | 25  | 90 giorni  | 0.001911 | GRU |
| RMSE  | 25  | 90 giorni  | 0.043715 | GRU |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 50  | 90 giorni  | 0.006617 | LSTM |
| MSE  | 50  | 90 giorni  | 8.6e-05 | LSTM |
| RMSE  | 50  | 90 giorni  | 0.009274 | LSTM |
| MAE  | 50  | 90 giorni  | 0.005844 | GRU |
| MSE  | 50  | 90 giorni  | 5.6e-05 | GRU |
| RMSE  | 50  | 90 giorni  | 0.007483 | GRU |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 100  | 90 giorni  | 0.003008 | LSTM |
| MSE  | 100  | 90 giorni  | 1.1e-05 | LSTM |
| RMSE  | 100  | 90 giorni  | 0.003317 | LSTM |
| MAE  | 100  | 90 giorni  | 0.002748 | GRU |
| MSE  | 100  | 90 giorni  | 1.1e-05 | GRU |
| RMSE  | 100  | 90 giorni  | 0.003317 | GRU |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 25  | 120 giorni  | 0.027043 | LSTM |
| MSE  | 25  | 120 giorni  | 0.001183 | LSTM |
| RMSE  | 25  | 120 giorni  | 0.034395 | LSTM |
| MAE  | 25  | 120 giorni  | 0.02039 | GRU |
| MSE  | 25  | 120 giorni  | 0.000717 | GRU |
| RMSE  | 25  | 120 giorni  | 0.026777 | GRU |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 50  | 120 giorni  | 0.007311 | LSTM |
| MSE  | 50  | 120 giorni  | 0,00009 | LSTM |
| RMSE  | 50  | 120 giorni  | 0.009487 | LSTM |
| MAE  | 50  | 120 giorni  | 0.012483 | GRU |
| MSE  | 50  | 120 giorni  | 0.000241 | GRU |
| RMSE  | 50  | 120 giorni  | 0.015524 | GRU |
| ------------- | ------------- | ------------- | ------------- |
| MAE  | 100  | 120 giorni  | 0.003187 | LSTM |
| MSE  | 100  | 120 giorni  | 1.2e-05 | LSTM |
| RMSE  | 100  | 120 giorni  | 0.003464 | LSTM |
| MAE  | 100  | 120 giorni  | 0.00268 | GRU |
| MSE  | 100  | 120 giorni  | 0,000009 | GRU |
| RMSE  | 100  | 120 giorni  | 0.003 | GRU |

Si può osservare dalla tabella, come le due reti restituiscano un risultato eccellente.
Di seguito carichiamo delle immagini che mostrano un esempio di predizione di entrambe le reti. Negli esempi viene fatta una predizione di 120 e le reti sono state addestrate sulla curva media.

LSTM: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/LSTM.png)

GRU: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/GRU.png)

# Conclusioni

Il task è stato completato con successo. Le curve ottenute sono state utilizzate per addestrare e testare i modelli. I modelli ottenuti predicono gli indici vegetali con grande precisione.

# Yield prediction

Terminato il task di forecasting, si è proceduto con il task di regressione.
L'obiettivo di questo task è quello di prevedere la resa di un pezzetto di campo, a partire da un immagine.

# Estrazione dell'informazione

Per creare il dataset siamo partiti da qgis, in questo caso abbiamo effettuato una conversione di tipo, infatti, l'informazione d'interesse era contenuta negli shape file dei campi, quindi, gli abbiamo convertiti in file raster e gli abbiamo salvati.

# ETL
Il codice utilizzato per questa fase è disponibile nel seguente [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/impResa.ipynb).
Per questo task la fase di etl è stata più semplice rispetto al task precedente, perchè abbiamo utilizzato le immagine dei campi che avevamo precedentemente pulito.
Successivamente, abbiamo creato delle nuove strutture dati che mantenessero la corrispondenza tra i pixel e la resa. Le nuove strutture dati contenevano i pixel in maniera sequenziale, quindi avevamo una sola dimensione, e non più X e Y. Durante questa fase abbiamo anche effettuato un'operazione di normalizzazione dei valori delle bande, dividendo per il valore massimo.
Abbiamo utilizzato la funzione di smoothing usata precedentemente per migliorare la qualità dei valori dei pixel.
Di seguito riportiamo un primo esempio di immagine. Le nuove immagini che abbiamo generato hanno sull'asse delle X le bande, e sull'asse delle Y il tempo.

First example: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/image1.png)

L'ultima operazione di ETL prevede l'utilizzo della funzione [SplineInterpolation](https://fda.readthedocs.io/en/latest/modules/autosummary/skfda.representation.interpolation.SplineInterpolation.html) che ci ha permesso di ottenere dei valori nel continuo. In questo modo abbiamo aumentato la lunghezza della serie temporale e ne abbiamo migliorato, ulteriormente, la qualità.
Di seguito riportiamo un esempio di immagine finale del pixel.

Final image: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/150x12.png)

Infine, abbiamo eliminato i pixel che avevano un valore della resa sbagliato, poi abbiamo salvato i dati in formato pickle.

# Deep learning

In questa fase, come prima cosa, siamo andati a dividere il dataset in training e test, facendo una suddivisione randomica. Poi abbiamo salvato le immagini dei pixel all'interno delle corrispondenti cartelle.

## Problematiche nella fase di Deep learning

Per completare questo task, inizialmente, si era deciso di utizzare due reti che erano VGG16 e VGG19, al seguente [link](https://keras.io/api/applications/vgg/) potete trovare la documentazione delle reti. Dopo aver implementato le reti abbiamo proceduto con la fase di training e test.
Al termine di quest'ultima siamo andati a effettuare delle predizioni, per controllare il risultato che la rete ci generava.
Purtroppo, la rete non generava risultati accettabili, in quanto erano tutti molto vicini al valore medio della resa.
Di seguito riportiamo uno scatter plot dove sugli assi abbiamo il valore reale della resa di un pixel e il valore predetto della resa di quel pixel.

Scatter error: 
<img src="https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/scatter_error.png" width="500">

## Tentativi e soluzione

Per cercare di risolvere questo problema, abbiamo iniziato una fase di diagnosi, per cercare di capire cosa generasse questo problema sull'addestramento dei modelli. Abbiamo fatto diversi tentativi cambiando l'architettura della rete, provando ad aggiungere e rimuovere strati densi, coon diverso numero di neuroni. Abbiamo provato diverse combinazioni di funzioni di attivazione e ottimizzatori. Abbiamo provato a implementare un'altra rete che è mobileNet_V2, l'abbiamo addestrata e testata, però, abbiamo sempre ottenuto gli stessi risultati negativi. Le reti erano addestrate sul dataset ImageNet, quindi, abbiamo provato a sbloccare dei layer convoluzionali, ma senza successo. Però, tutti questi tentativi ci hanno portato a pensare che il problema non fosse la rete, ma il dataset.
Abbiamo iniziato a generare diversi tipi di immagini, aumentandone le dimensioni, mettendo la stessa immagine in serie e in parallelo. Abbiamo usato immagini più piccole, riducendo la serie temporale a 30 giorni, abbiamo cercato di aumentare le differenze nelle immagini. Purtroppo, tutti questi tentativi non hanno migliorato l'addestramento delle reti.
I precedenti tentativi ci hanno portato a pensare di avere un problema di sbilanciamento dei dati, o scarsa correlazione, all'interno del dataset. Quindi abbiamo costruito una funzione ideale che restituiva un valore della resa per un certo valore dell'ndvi. Quindi ad alti valori dell'ndvi abbiamo assogiato alti valori di resa. Successivamente, abbiamo generato un dataset fortemente correlato, che chiameremo dataset sintetico. 
Anche questo tentativo non ha generato i risultati sperati, quindi, l'ultima cosa da diagnosticare era l'input del modello.
Infatti, il problema era la funzione [ImageDataGenerator.flow_from_dataframe()](https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/ImageDataGenerator). Questa funziona generava l'input per il modello. Forse, a causa del tipo di immagini che abbiamo generato, questa funzione generava un input completamente sbagliato, infatti, le immagini erano nere. Di seguito carichiamo un esempio.

Input_error:
<img src="https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/error_input.png" width="200">

Per risolvere il problema abbiamo implementato una funzione che va a creare l'input per i modelli.
Questa funzione ci ha permesso di risolvere il problema. Successivamente, abbiamo addestrato tutti i modelli sopra citati. Riportiamo di seguito alcune scatter plot.

VGG16: 
<img src="https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/vgg16.png" width="550">

VGG19: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/vgg19.png)

MBN: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/mbn_scatter.png)

Riportiamo di seguito i risultati ottenuti con queste reti, le metriche calcolate sono la mean absolute error (MAE), la mean squared error (MSE) e la Root Mean Squared Error (RMSE).

# Conclusioni

Il task è stato terminato con successo. Abbiamo addestrato i modelli con immagini diverse e distribuzioni diverse, per verificare miglioramenti o peggioramenti delle prestazioni. I risultati ottenuti sono abbastanza simili a quelli precedenti, quindi, la qualità della previsione è rimasta la stessa.
