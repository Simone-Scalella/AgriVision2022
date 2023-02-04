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
Il resto dello script è visibile in questo [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/geoT.ipynb).
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

Prima del taglio abbiamo dovuto effettuare una operazione di riordinamento dei file scl, in qunato si presentavano all'interno di diverse cartelle, quindi si è deciso di spostarle, in maniera ordinata, all'interno di un unica cartella. Il codice utilizzato è nel seguente [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/autoRename.py).
Di seguito carichiamo un'immagine della directory precedente.

Vecchia directory: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/scl_directory.png)

Si è notato che alcune immagini scl avevano i metadati rovinati, quindi, si è proceduto a rigenerarli. Il codice utilizzato è nel seguente [file](https://github.com/Accout-Personal/AgriVision2022/blob/main/geoTLeoMakeTransform.ipynb).

## Seconda fase di ETL

Durante questa fase siamo andati a tagliare le porzioni d'interesse sia dai file scl che dai file .tiff, usando le coordinate degli shape file. Abbiamo utilizzato il metodo Mask della libreria rasterio [(link)](https://rasterio.readthedocs.io/en/latest/api/rasterio.mask.html), inoltre, per ogni nuova immagine abbiamo dovuto generare dei nuovi metadati. Il codice utilizzato si trova nel seguente file...?
Al termine di questa operazione ci siamo resi conto che le dimensioni della maschera tagliata erano più piccole rispetto a quelle del campo. Quindi, abbiamo utilizzato la libreria Resampling [(link)](https://rasterio.readthedocs.io/en/latest/topics/resampling.html#resampling-methods), di rasterio. Usando come parametro 'nearest' abbiamo effettuato un operazione di upsampling senza modificare il contenuto informativo della maschera. Al termine dell'esecuzione, le dimensioni delle maschere e dei campi erano uguali.
Di seguito carichiamo un esempio del taglio della maschera (ridimensionata) e del campo.

Maschera e campo: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/mask.png)

A questo punto possiamo applicare la maschera al campo per togliere tutti i pixel che non sono d'interesse per le analisi. Il codice utilizzato si trova nel seguente file...?
Di seguito carichiamo un esempio di campo filtrato.

Campo filtrato: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/afterMask.png)

A questo punto andiamo, nuovamente, a calcolare gli indici vegetali ndvi e ndre.
Riportiamo di seguito un'immagine sull'andamento dell'ndvi di un pixel.

NDVI dopo la maschera: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/afterMask.png)

Abbiamo eliminato picchi anomali e valori non corretti, però, dobbiamo migliorare la qualità della curva. Per fare questo utilizziamo una funzione di smoothing [(link)](https://github.com/cerlymarco/tsmoothie). Di seguito riportiamo un esempio del risultato ottenuto.

NDVI con smoothing: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/afterMask.png)
