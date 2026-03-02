# Guida al Testing Responsive - Queue Ordini

Questo documento ti aiuta a testare il design responsive della pagina **queue.html** su diversi dispositivi.

## Breakpoints Implementati

### 📱 Smartphone Piccolo (max 320px)
- Samsung Galaxy S8, iPhone 5/SE
- Header ridotto al minimo
- Singola colonna per gli ordini
- Font sizes ottimizzati per visibilità

### 📱 Smartphone Standard (321px - 480px)
- Samsung Galaxy A12, iPhone 6/7/8
- Header compatto (75px)
- Singola colonna fluid
- Pulsanti ottimizzati per touch (min 40x40px)

### 📱 Smartphone Landscape (481px - 768px)
- iPhone XR in landscape
- 2 colonne di ordini
- Header leggermente ridotto
- Testo e pulsanti scalabili

### 📱 Tablet (769px - 1024px)
- iPad Mini, Samsung Galaxy Tab A
- Header 85px
- 2-3 colonne di ordini
- Font sizes intermedi

### 🖥️ Desktop (1025px - 2559px)
- Laptop standard
- Header pieno (90px)
- 3+ colonne di ordini
- Tutti gli elementi visibili

### 🖥️ Ultra-Wide (2560px+)
- Monitor extra-wide
- Padding maggiori
- Margini aumentati
- Lettere più grandi

---

## Come Testare

### 1. **Su Browser Desktop (Chrome/Firefox/Edge)**

#### Opzione A: Developer Tools
```
1. Apri queue.html nel browser
2. Premi F12 (Developer Tools)
3. Clicca su "Toggle device toolbar" (Ctrl+Shift+M)
4. Seleziona diversi dispositivi dalla lista presettata:
   - iPhone SE (375px)
   - iPhone 12 Pro (390px)
   - iPhone 12 Pro Max (428px)
   - iPad (768px)
   - iPad Pro (1024px)
5. Prova anche dimensioni personalizzate:
   - 320x640 (smartphone piccolo)
   - 480x854 (smartphone grande)
   - 600x800 (tablet piccolo)
   - 768x1024 (tablet)
   - 1920x1080 (desktop)
```

#### Opzione B: Resize Manuale
```
1. Apri queue.html a schermo pieno
2. Ridimensiona lentamente la finestra da larghezza massima a minimum
3. Osserva i cambiamenti ai seguenti breakpoints:
   - 320px - Smartphone piccolo
   - 480px - Smartphone grande
   - 768px - Tablet piccolo
   - 1024px - Tablet grande
   - 2560px - Ultra-wide
```

### 2. **Smartphone Reale - Samsung Galaxy Z Fold 5**

#### Schermo Esterno (Chiuso)
```
- Dimensioni: ~6.2" (400x892px)
- Comportamento: Come smartphone normale
- Test: Scrollare, leggere ordini, modificare stato
```

#### Schermo Interno (Aperto)
```
- Dimensioni: ~7.6" landscape (1768x1008px)
- Comportamento: Layout tablet/desktop
- Test: Verificare che mostra 2-3 colonne di ordini
- Test: Controllare che la piega del display non interferisce
```

### 3. **Dispositivi Reali da Testare**

Prova ogni dispositivo con questi test:

| Dispositivo | Risoluzione | Orientamento | Note |
|------------|------------|--------------|------|
| iPhone SE | 375x667 | Portrait | Schermo piccolo |
| iPhone 14 Pro | 390x844 | Portrait | Notch superiore |
| iPhone 14 Pro Max | 428x926 | Portrait | Massima larghezza |
| Samsung Galaxy S23 | 360x800 | Portrait | Display AMOLED |
| Samsung Galaxy Z Fold 5 | 400x892 / 1768x1008 | Entrambi | **FOLDABLE** |
| iPad 7 | 810x1080 | Portrait | Tablet standard |
| iPad Pro 12.9" | 1366x1024 | Landscape | Tablet grande |
| MacBook 13" | 1440x900 | - | Laptop portatile |
| Dell 27" UHD | 3840x2160 | - | Ultra-wide |

---

## Cosa Verificare in Ogni Test

### ✅ Layout
- [ ] Header non è danneggiato
- [ ] Ordini si dispongono correttamente (1, 2 o 3 colonne)
- [ ] Nessun overflow orizzontale
- [ ] Footer visibile e raggiungibile scrollando

### ✅ Testo
- [ ] Tutto è leggibile (nessun testo tagliato)
- [ ] Font size è appropriato per la dimensione dello schermo
- [ ] Nessun testo sovrapposto
- [ ] Abbreviazioni funzionano (#ordine, €, ✓)

### ✅ Pulsanti
- [ ] Pulsanti sono toccabili facilmente (min 40x40px)
- [ ] Hover states funzionano su desktop
- [ ] Click/tap funzionano su mobile
- [ ] Nessun pulsante nascosto

### ✅ Colori e Contrasto
- [ ] Testo bianco è leggibile su sfondo scuro
- [ ] Status tags sono facilmente distinguibili
- [ ] Stripe colorate sono visibili
- [ ] Live pill è evidente

### ✅ Performance
- [ ] Carica rapidamente
- [ ] Scrolling è fluido
- [ ] Nessun lag quando cambi stato ordini
- [ ] Load time < 2 secondi

### ✅ Dispositivi Foldable (Z Fold 5)
- [ ] Schermo esterno: comportamento normale smartphone
- [ ] Schermo interno: comportamento tablet/desktop
- [ ] Piega: non interferisce con contenuto importante
- [ ] Transizione: fluida quando passi da una schermata all'altra

---

## CSS Features Implementate

1. **Responsive Breakpoints**
   - 5 breakpoints principali (320px, 481px, 769px, 1025px, 2560px)
   - Media queries per orientamento (portrait/landscape)
   - Support foldable devices

2. **Safe Area Support**
   - Notch devices (iPhone X+)
   - Punch-hole displays (Samsung S21+)
   - Curved edges
   - Folding screens

3. **Touch Optimization**
   - Pulsanti touch-friendly (min 40px)
   - Rimosso tap-highlight-color
   - Padding maggiore su mobile

4. **Performance**
   - Ridotto-motion support
   - Font-smoothing ottimizzato
   - CSS efficiente

---

## Problemi Comuni e Soluzioni

### Problema: Testo troppo piccolo
**Soluzione:** Il browser ingrandirà automaticamente se zoom è < 100%

### Problema: Pulsanti troppo vicini
**Soluzione:** Usa modal/dropdown su dispositivi piccoli (non implementato attualmente)

### Problema: Layout spezzato sul Z Fold 5
**Soluzione:** Media query specifico per fold attivato (1700px x 800px)

### Problema: Scrolling orizzontale indesiderato
**Soluzione:** Usa `overflow-x: hidden` su body (già implementato)

---

## Browser Compatibility

| Browser | Desktop | Mobile | Note |
|---------|---------|--------|------|
| Chrome | ✓ | ✓ | Pieno supporto |
| Firefox | ✓ | ✓ | Pieno supporto |
| Safari | ✓ | ✓ | Safe-area supportato |
| Edge | ✓ | ✓ | Pieno supporto |
| Samsung Internet | ✓ | ✓ | Per Z Fold 5 |

---

## Consigli per il Testing

1. **Usa Chrome DevTools per debugging rapido**
   - F12 → Device Toolbar → Seleziona device

2. **Controlla alla velocità originale (non slow motion)**
   - Per verificare actual performance

3. **Testa sia online che offline**
   - Simula connessioni lente (Slow 3G in DevTools)

4. **Prova gesti specifici su mobile**
   - Tap doppio
   - Swipe
   - Long-press

5. **Documenta problemi con screenshot**
   - Device name + risoluzione
   - Descrizione del problema
   - Steps per riprodurre

---

## Contatti e Feedback

Se trovi problemi di responsività:
1. Nota il dispositivo esatto e risoluzione
2. Descrivi cosa non funziona
3. Fornisci screenshot se possibile
4. Comunica attraverso il sistema di issue tracking

---

**Ultimo aggiornamento:** Febbraio 2026
**Versione queue.html:** Fully Responsive v1.0
