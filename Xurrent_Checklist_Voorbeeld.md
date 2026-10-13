# Voorbeeld — de ANPR/CCTV checklist in Xurrent (native)

Doel: laten zien **hoe** je jouw Excel 1-op-1 (of dicht benaderend) in Xurrent krijgt, met twee mechanismen:

1. **Checklist in Instructions** — het afvinkbare lijstje in het *Instructions*-veld van een task-/requesttemplate.
2. **UI Extension** — aangepaste velden (dropdowns, tekst, datum) op diezelfde template, met secties, voorwaarden en validatie.

> Let op: de Instructions-checklist is **enkel afvinken (aan/uit)**. Status OK/NOK/WARN, meetwaarden en opmerkingen per punt horen in **UI-Extension-velden** of in de **Note**. Daarom combineren we beide.

---

## 1. Structuur: van Excel-secties naar Xurrent-taken

In plaats van de per-camera **matrix** (7 rijen × 6 kolommen) — die Xurrent niet als echt grid kan — is de elegante vertaling: **één taak per camera** binnen één workflow. Zo wordt de matrix opgesplitst in kleine, mobiel-vriendelijke taken.

**Workflowtemplate: "Preventief onderhoud ANPR & CCTV"**

| # | Taak | Inhoud |
|---|---|---|
| 1 | Algemene info & locatie | UI Extension-velden (ticket, site-ID, technieker, GPS, locatietype) |
| 2 | Checklist straatkast & voeding | Instructions-checklist (16 punten) + UI Extension (status/waarde/opmerking) |
| 3 | Camera 1 (+ 2, 3 …) | Per camera: Instructions-checklist (5 punten) + foto's |
| 4 | As-built inventarisatie | UI Extension-velden per component (of vast blok) |
| 5 | Afwijkingen & acties | UI Extension (vrije tekst + ja/nee-velden) |
| 6 | Clôture & afmelding | UI Extension (call, contactpersoon, tijdstip) |

---

## 2. Instructions-checklist (concreet, knippen & plakken)

Zet dit in het **Instructions**-veld van de tasktemplates. Selecteer de regels en klik op het checklist-icoon (zoals bij een bullet-lijst).

### Taak 2 — Checklist straatkast & voeding
```
[ ] 1.  Visuele inspectie, reiniging & ontstoffing binnenzijde straatkast
[ ] 2.  Staat van kast, behuizing, deur, slot & handgreep gecontroleerd
[ ] 3.  Waterdichtheid, afdichtingen & afwezigheid corrosie/roest
[ ] 4.  Interne bekabeling: voeding, UTP & glasvezel (buigradius OK)
[ ] 5.  Glasvezel patchbox & lascassette / pigtails (GigaMedia / FO)
[ ] 6.  Voedingsmodule MeanWell EDR-150-24 (spanning & werking)
[ ] 7.  DC-UPS module Phoenix Contact QUINT (status & werking)
[ ] 8.  Industriële switch & M2M 4G router / antenne (Westermo e.a.)
[ ] 9.  230V voeding, automaten/disjoncteurs (Q1, Q2) & PoE-injectoren
[ ] 10. Aardingsverbindingen & klemmenstroken (borniers) aangespannen
[ ] 11. Etikettering (Danger sticker, BPS plaatje, kabeltags) aanwezig & leesbaar
[ ] 12. Relais voor coupure op afstand gecontroleerd
[ ] 13. I/O-module HW Group (LEDs, IN1 deur, IN2 automaat, IN3 UPS)
[ ] 14. UPS tempo-instelling gecontroleerd (gefixeerd op 10 min)
[ ] 15. UPS autonomietest uitgevoerd (2 min netonderbreking, voeding behouden)
[ ] 16. Toestand UPS-batterijen gecontroleerd / vervangen
```

### Taak 3 — Camera X (per camera, identieke template)
```
[ ] 1. Reiniging optiek & caisson
[ ] 2. IR & status-LEDs
[ ] 3. Fixatie en montage
[ ] 4. Zichtveld cfr. referentie
[ ] 5. ANPR-lezingen
```
> Voeg per camerataak de foto's toe als **bijlage op de note** van die taak → foto's zijn dan automatisch **per type/per camera** gegroepeerd.

---

## 3. UI Extension-velden (Designer) — mapping van de Excel

Maak per taaktemplate een UI Extension. In de **Designer** (Settings > UI Extensions > Add) voeg je velden en secties toe; je kan voorwaarden en validatie instellen. (FR-labels kan je toevoegen als tweede regel of in de labeltekst.)

### Sectie 1 — Algemene informatie
| Veldlabel (NL / FR) | Type | Opmerking |
|---|---|---|
| Ticket / Referentie | tekst (verplicht) | ISD- / ticketnr |
| ID Site / Site-ID | tekst | |
| Interventienummer | tekst | |
| Interventiedatum | datum | |
| Technicus(sen) | tekst | of person-suggest |
| Adres / Locatie | tekst | |
| Gemeente / Stad | tekst | |
| Aankomstuur / Vertrekuur | tekst (HH:MM) | |
| Contactpersoon Irisnet / Klant | tekst | |
| Aantal stuurkasten op site | getal | |

### Sectie 2 — Geografische locatie & GPS
| Veldlabel | Type | Opmerking |
|---|---|---|
| Stuurkast / Armoire ID | tekst | |
| GPS Kast (N / E) | tekst | manueel |
| Camera 1 ID & Type | tekst | |
| GPS Cam 1 (N / E) | tekst | manueel |
| Mast / Paal referentie | tekst | |
| Locatietype publiek domein | select | Kruispunt, Straat, School, … |

> GPS is in Xurrent **manueel** (geen toestel-GPS). Wil je automatische GPS → Fase 1 (Power Apps).

### Sectie 3 — Algemene status interventie
| Veldlabel | Type | Opties | Validatie |
|---|---|---|---|
| Status van de interventie | select | OK / NOK / WARN | verplicht |
| Algemene opmerkingen site | tekst (meerregelig) | | |

### Sectie 4 — Checklist straatkast (status per punt)
Koppel deze **aan de 16 checklistpunten**. Alleen invullen waar afgeweken (anders blijft het leeg).
| Veldlabel | Type | Opties |
|---|---|---|
| Status punt 6 — Voeding MeanWell | select | OK / NOK / WARN |
| Meetwaarde punt 6 | tekst | bv. "23.8 V" |
| Opmerking punt 6 | tekst | |
| … (herhaal voor de punten waar je status wil) | | |

> **Tip om het licht te houden:** laat de Instructions-checklist het "gedaan"-vinkje zijn, en gebruik de UI-Extension-statusvelden **alleen voor de punten die afwijken**. Dan hoef je geen 16×3 velden te maken.

### Sectie 5 — Camerataak (per-camera template)
| Veldlabel | Type | Opties |
|---|---|---|
| Camera ID / Positie | tekst | |
| 1. Reiniging optiek & caisson | select | OK / NOK / WARN |
| 2. IR & status-LEDs | select | OK / NOK / WARN |
| 3. Fixatie en montage | select | OK / NOK / WARN |
| 4. Zichtveld cfr. referentie | select | OK / NOK / WARN |
| 5. ANPR-lezingen | select | OK / NOK / WARN |
| Overall status | select | OK / NOK / WARN |
| Opmerkingen | tekst | |
| Foto's | bijlage(n) | zie §5 |

### Sectie 6 — As-built inventarisatie
| Veldlabel | Type |
|---|---|
| Merk & model per component | tekst (of vast blok) |
| Serienummer | tekst |
| IP-adres / poort | tekst |
| As-built OK? | select Ja/Nee |

### Sectie 7 — Afwijkingen & acties
| Veldlabel | Type | Opties |
|---|---|---|
| Vastgestelde afwijkingen / schade | tekst | |
| Uitgevoerde acties | tekst | |
| Ter plaatse hersteld? | select | Ja / Nee |
| Offerte nodig? | select | Ja / Nee |
| Vervangonderdeel nodig? | select | Ja / Nee |

### Sectie 8 — Clôture & afmelding
| Veldlabel | Type | Opties |
|---|---|---|
| Afmeld-call naar Irisnet vóór vertrek | select | Ja / Nee |
| Contactpersoon gesproken | tekst | |
| Tijdstip afmelding | tekst (HH:MM) | |
| Zware schade/anomalie gemeld in ticket | select | Ja / Nee |

---

## 4. De per-camera matrix: 3 opties

| Optie | Hoe | Voor- | Na- |
|---|---|---|---|
| **A. Taak per camera** (aanbevolen) | Workflow genereert taak "Camera 1..N" | Klein & mobiel; foto's per camera; geen grid nodig | Meer taken per workflow |
| **B. Platte velden** | Cam1_Reiniging … Cam3_Overall | Alles in één formulier | Veel velden; "extra camera's" als tekst |
| **C. Matrix in Note** | Rich-text tabel in de Note | 1-op-1 zoals Excel | Slecht invullen op gsm |

---

## 5. Foto's per type — hoe je ze gegroepeerd krijgt

| Manier | Werking | Groepering |
|---|---|---|
| **Bijlage per taak** | Foto's op de note van de taak (bv. de camerataak) | ✅ per taak/camera |
| **Aparte note per fotoblok** | Note "FOTO — Stuurkast interieur", "FOTO — Glasvezel", … | ✅ per type |
| **Alle foto's op één note** | Snelst | ❌ geen groepering |
| **Via API `custom_fields_attachments`** | Programmatisch per custom field | ✅ per veld (maatwerk) |

> Conventie-afspraak (bv. altijd `FOTO 1.1 — …` als notetitel) geeft je groepering zonder maatwerk.
> Toestel-camera: attachments kunnen rechtstreeks vanuit de **Xurrent mobiele app** worden toegevoegd.

---

## 6. Wat je native NIET krijgt (samengevat)

- ❌ **Offline** — verbinding nodig.
- ❌ **Automatische GPS** — manueel tekstveld.
- ❌ **Digitale handtekening** — enkel via custom HTML/JS in de klassieke builder (maatwerk).
- ❌ **Echt grid / herhalende tabel** — opgelost via "taak per camera" (optie A).
- ❌ **Branded PDF-export** — extern (AI-prompt) of Power Automate.

---

## 7. Illustratief: klassieke UI-extension (HTML)

De moderne **Designer** genereert dit voor je. Puur ter illustratie van één select-veld:

```html
<div class="form-group">
  <label for="cam1_overall">Camera 1 — Overall status</label>
  <select name="cam1_overall" id="cam1_overall">
    <option value="OK">OK</option>
    <option value="NOK">NOK</option>
    <option value="WARN">WARN</option>
  </select>
</div>
```
> Xurrent bewaart de waarden als **custom fields (JSON)** → uitleesbaar via de API en dus **AI-klaar**.

---

## 8. Conclusie

Met **tasktemplates + Instructions-checklists + UI Extensions (Designer)** krijg je een **goede, native weergave** van jouw Excel in Xurrent — inclusief structuur, audit trail en ticket-koppeling — **zonder extra tooling**.

Wat je opoffert t.o.v. Excel: foto's zijn bijlagen (niet inline per item), GPS is manueel, geen handtekening en geen echt grid → daarom "**taak per camera**" en een vaste notetitel-conventie voor foto's.
