Subsistema de sensors i actuadors (alumnat que no està en “Dual Intensiva”)

Cal revisar en quin punt real ens trobem pel que fa al desenvolupament del subsistema IoT. Fer una documentació inicial, per tal de concretar quin és l’estat real pel que fa a:

    -El diagrama de disseny de subsistema: existeix? s’aprova?

    -Quin model de dades s’utilitzarà.

    -A partir de les proves que ja teniu fetes, decidir quines funcionalitats del subsistema (posició, etc.) accepteu i decidiu continuar desenvolupant.

    -Com implementareu l’actuador on/off

    -Què necessitareu a partir d’ara que no tingueu

Les conclusions de l’anterior, ens serviran per a saber on estem.

El aquest sprint, l’objectiu és:

    -Escollir sensors

    -Deixar el subsistema operatiu. Així només quedarà pendent per al següent sprint la integració de la sensòria amb el prototip que fan els d’automoció.

Notes:

Recordeu que Laravel i el subsistema han de comunicar-se via API / webhooks, i que serà Laravel qui servirà les dades al front-end (és a dir, no comunicació directa Frontend - Subsistema)
