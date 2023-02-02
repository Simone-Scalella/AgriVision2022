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

Di seguito riportiamo un esempio di immagine dei campi agricoli.

Immagine dei campi: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/campi.png)

Una volta scaricate tutte le immagini si è proceduto utilizzando la libreria gdal per aprire le immagini all'interno del file jupyter, e abbiamo iniziato a studiarne le dimensioni per proseguire con la fase di etl. Di seguito riportiamo le dodici bande di una immagine del campo agricolo.

Bande dei campi: 
![alt text](https://github.com/Accout-Personal/AgriVision2022/blob/main/readImage/bande_raw.png)




