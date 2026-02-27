# Subsistema

## Diagrama de disseny

El diagrama de disseny del subsistema **existeix** i es troba al mateix repositori:

[Veure diagrama](./diagrama.png)

Estat: **Pendent d’aprovació**

---

## Model de dades

**Base de dades:** MongoDB Atlas

---

## Funcionalitats acceptades

A partir de les proves realitzades (enviament de dades des de la Raspberry i recepció mitjançant webhook), es decideix continuar amb:

### Funcionalitats principals

- Mostrar ubicació (GPS)
- Actuador ON/OFF per consultar estat del vehicle

### Proves extra (fase posterior)

- Sonar – Mesurar distància entre objecte i vehicle  
- Càmera – Visualització interior del vehicle en temps real  

---

## Implementació actuador ON/OFF

### Hardware
- Relé connectat a un pin digital de la placa
- Permet tallar o donar pas al corrent

### Lògica
- El microcontrolador consulta l’estat a l’API de Laravel  
- `0 = OFF`  
- `1 = ON`  
- Activa/desactiva el relé segons el valor rebut

### Comunicació
- Comunicació exclusiva via **API/Webhooks** entre Laravel i el subsistema
- El frontend **no** es comunica directament amb el hardware

---

## Necessitats pendents

Cada equip ha de disposar de:

- Relé (10 amperes)
- Pila  
- GPS  
- Ampliador de cobertura  
