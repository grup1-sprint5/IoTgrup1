
El diagrama de disseny de subsistema: existeix? s’aprova?



Quin model de dades s’utilitzarà.
MongoDB Atlas

A partir de les proves que ja teniu fetes, decidir quines funcionalitats del subsistema (posició, etc.) accepteu i decidiu continuar desenvolupant.
Tenim fetes diferents proves, com ara, enviar dades desde la raspberry i enviant les dades a un webhook com a prova inicial.

Les funcionalitats que mantindrem són:

Mostrar l’ubicació de la raspberry (GPS)
Actuador on/off per veure l’estat del vehicle
Proves Extra (fer quan tinguem lo principal ja fet)
Sonar: Per medir la distància entre un objecte i el vehicle
Càmara: Per veure l’interior del vehicle en qualsevol moment


Com implementareu l’actuador on/off
-Hardware: S'utilitzarà un relé connectat a un pin digital de la placa per tallar/permetre el pas de corrent.
-Lògica: El microcontrolador consultarà l'estat a l'API de Laravel (0=OFF / 1=ON) i activarà el relé segons correspongui.
-Comunicació: Via API/Webhooks exclusiva entre Laravel i el subsistema; el frontend mai parlarà directament amb el hardware.

Què necessitareu a partir d’ara que no tingueu

Ens hem d’assegurar que cada equip tingui:

- Relé
	- PIla
	- Gps 
	- Ampliador de cobertura

