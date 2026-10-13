# Handover — Xurrent-flow "Preventief onderhoud ANPR & CCTV"

**Voor:** BI-/IT-team (configuratie + ontsluiting)
**Van:** analyse digitale onderhoudschecklist
**Doel:** de Excel-checklist (`JACOPS_Preventief_Onderhoud_ANPR_CCTV_V2.xlsx`) omzetten naar een native Xurrent-flow, met gestructureerde data die nadien via API ontsloten wordt (BI + AI-rapport).

**Scope van deze opdracht:** **Fase 0 — Xurrent-native**. Geen extra tooling, geen Power Apps, geen licentiekost.
**Buiten scope:** offline werking, automatische GPS, digitiale handtekening, branded PDF (zie §12 — latere fases).

---

## 1. In één oogopslag

**Te bouwen objecten in Xurrent:**

| Object | Aantal | Doel |
|---|---|---|
| Request template | 1 | Registratie van de interventie |
| Workflow template | 1 | Structuraliseert de beurt in taken |
| Task templates | 6 | Algemene info / Straatkast / Camera / As-built / Afwijkingen / Clôture |
| UI Extensions (Designer) | 5 | Gestructureerde velden per taaktemplate |
| Instructions-checklists | 2 | Afvinklijst straatkast + camera |

**Kernprincipes:**
1. **Checklist in Instructions** = afvinken (aan/uit). **UI Extension** = status/waarde/opmerking.
2. **Per-camera matrix → taak per camera** (Xurrent heeft geen echt grid).
3. **Foto's per camera/type** via bijlagen op de betreffende taak + vaste notetitel-conventie.
4. Alle custom fields worden **JSON** opgeslagen → **API-ontsluitbaar** voor BI en AI-rapport.

---

## 2. Randvoorwaarden & rollen

| Vereiste | Detail |
|---|---|
| Xurrent-account | Productie- **en** QA-account aanwezig |
| Rollen om te configureren | **Account Administrator** (UI Extensions, settings), **Account Designer** (templates + UI Extensions), **Service Desk Manager** (request templates) |
| Email Policy | "Allow inbound email to generate new requests" **aan** (indien later e-mailbrug gewenst, §11) |
| Personen/teams | Team "Techniekers PM" aanmaken/toewijzen |
| App | Xurrent mobiele app op toestellen van techniekers |
| Assets (optioneel) | Site/CI-records voor de straatkasten (koppeling achteraf) |

**Aanbevolen werkwijze:** alles **eerst in QA** bouwen en testen, daarna uitrollen naar productie via de UI-Extension **`reference`** (zie §10).

---

## 3. Naamgevingsconventie

| Type | Patroon | Voorbeeld |
|---|---|---|
| Request template | `JACOPS — PM <domein>` | `JACOPS — PM ANPR & CCTV` |
| Workflow template | `JACOPS — PM ANPR & CCTV (workflow)` | |
| Task template | `PM — <nr>. <naam>` | `PM — 2. Checklist straatkast` |
| UI Extension | `UE — PM <taak>` | `UE — PM Checklist straatkast` |
| UI Extension reference | `je-pm-<taak>` (lowercase, uniek) | `je-pm-checklist-kast` |

> De **reference** van de UI Extension is de sleutel om QA → productie te synchroniseren. Kies ze **nu** definitief en wijzig ze niet meer.

---

## 4. Bouwstap 1 — Request template

**`JACOPS — PM ANPR & CCTV`**

| Veld | Waarde |
|---|---|
| Subject | `Preventief onderhoud ANPR & CCTV — {{site}}` |
| Category | (kies/aanmaken) `Onderhoud` |
| Service | `PM ANPR & CCTV` (service aanmaken indien nodig) |
| Impact | `low` |
| Team (default) | `Techniekers PM` |
| Instructions | Korte instructie + link naar werkinstructie |
| Workflow template | koppel `JACOPS — PM ANPR & CCTV (workflow)` |
| Registration hints | "Vul site-ID en ticketnummer in; start daarna de taken" |

**Aandachtspunt:** in de **Instructions** van de *request template* komt de **korte** samenvatting; de **volledige** checklists staan op de **taaktemplates** (§6).

---

## 5. Bouwstap 2 — Workflow template

**`JACOPS — PM ANPR & CCTV (workflow)`** — taken in deze volgorde:

| # | Task template | Toewijzing |
|---|---|---|
| 1 | `PM — 1. Algemene info & locatie` | Technieker |
| 2 | `PM — 2. Checklist straatkast` | Technieker |
| 3 | `PM — 3. Camera` (× aantal camera's) | Technieker |
| 4 | `PM — 4. As-built inventarisatie` | Technieker |
| 5 | `PM — 5. Afwijkingen & acties` | Technieker |
| 6 | `PM — 6. Clôture & afmelding` | Technieker |

**Camera-taken:** genereer **1 taak per camera** (configureerbaar aantal; standaard 3, extra optioneel). Dit vervangt de matrix.

---

## 6. Bouwstap 3 — Instructions-checklists (exacte tekst)

Selecteer de regels in het **Instructions**-veld en klik het **checklist-icoon** (zoals bullet-lijst).

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

### Taak 3 — Camera (per camera)
```
[ ] 1. Reiniging optiek & caisson
[ ] 2. IR & status-LEDs
[ ] 3. Fixatie en montage
[ ] 4. Zichtveld cfr. referentie
[ ] 5. ANPR-lezingen
```

> Zet de FR-vertaling als tweede regel per punt indien tweetalig vereist.

---

## 7. Bouwstap 4 — UI Extension-specificatie

Per taaktemplate één UI Extension (Settings > UI Extensions > Add > Designer). Velden verschijnen als **custom fields (JSON)** op de taak.

> **Types** hieronder zijn de *intentie*; kies het overeenkomstige veldtype in de Designer. `select` = keuzelijst, `text` = tekst, `date` = datum, `number` = getal, `bool` = ja/nee. Markeer **V** = verplicht, **C** = voorwaardelijk (voorwaarde/validatie instellen).

### UE — PM 1. Algemene info & locatie
| Veld | Type | Opties | Verpl. |
|---|---|---|---|
| Ticket / Referentie | text | | V |
| ID Site | text | | V |
| Interventienummer | text | | |
| Interventiedatum | date | | V |
| Technicus(sen) | text / person | | V |
| Adres / Locatie | text | | |
| Gemeente / Stad | text | | |
| Aankomstuur / Vertrekuur | text (HH:MM) | | |
| Contactpersoon Irisnet / Klant | text | | |
| Aantal stuurkasten op site | number | | |
| Stuurkast / Armoire ID | text | | |
| GPS Kast N | text | | |
| GPS Kast E | text | | |
| Mast / Paal referentie | text | | |
| Locatietype publiek domein | select | Kruispunt / Straat / School / Zone 30 / Overig | |
| Camera 1 ID & Type | text | | |
| GPS Cam 1 N / E | text | | |

> GPS = **manueel** (native). Automatische GPS → latere fase.

### UE — PM 2. Checklist straatkast (alleen afwijkingen vastleggen)
| Veld | Type | Opties | Verpl. |
|---|---|---|---|
| Algemene status interventie | select | OK / NOK / WARN | V |
| Algemene opmerkingen site | text (meerregelig) | | |
| Status afwijkend punt (nummer) | number | | |
| Status OK/NOK/WARN (afwijkend punt) | select | OK / NOK / WARN | C |
| Meetwaarde | text | | |
| Opmerking | text | | |

> Ontwerpkeuze: op de 16 punten geen 48 velden maken. Technieker vinkt de checklist af; **enkel afwijkingen** worden in de UI Extension geregistreerd (nummer + status + waarde + opmerking). Wil je tóch status per punt, dan per punt een `select` (16 velden). **Beslis dit vóór de bouw.**

### UE — PM 3. Camera (hetzelfde op elke camerataak)
| Veld | Type | Opties | Verpl. |
|---|---|---|---|
| Camera ID / Positie | text | | V |
| 1. Reiniging optiek & caisson | select | OK / NOK / WARN | V |
| 2. IR & status-LEDs | select | OK / NOK / WARN | V |
| 3. Fixatie en montage | select | OK / NOK / WARN | V |
| 4. Zichtveld cfr. referentie | select | OK / NOK / WARN | V |
| 5. ANPR-lezingen | select | OK / NOK / WARN | V |
| Overall status | select | OK / NOK / WARN | V |
| Opmerkingen | text | | |

### UE — PM 4. As-built inventarisatie
| Veld | Type | Opties |
|---|---|---|
| Merk & model | text | |
| Serienummer | text | |
| IP-adres / poort | text | |
| As-built OK? | select | Ja / Nee / N.v.t. |
| Opmerking | text | |

> Componenten: Camera 1–3, Voeding (PSU 24V, MeanWell EDR-150-24), DC-UPS (Phoenix Contact QUINT), I/O Controller (HW Group), Switch/Router/M2M (Westermo/GigaMedia), Glasvezel Patchbox (GigaMedia/FO).

### UE — PM 5. Afwijkingen & acties
| Veld | Type | Opties |
|---|---|---|
| Vastgestelde afwijkingen / schade | text (meerregelig) | |
| Uitgevoerde acties | text (meerregelig) | |
| Ter plaatse hersteld? | select | Ja / Nee |
| Offerte nodig? | select | Ja / Nee |
| Vervangonderdeel nodig? | select | Ja / Nee |

### UE — PM 6. Clôture & afmelding
| Veld | Type | Opties |
|---|---|---|
| Afmeld-call naar Irisnet vóór vertrek | select | Ja / Nee |
| Contactpersoon gesproken | text | |
| Tijdstip afmelding | text (HH:MM) | |
| Zware schade/anomalie gemeld in ticket | select | Ja / Nee |

> De **handtekeningen** (technicus + validatie) zijn native niet voorzien → latere fase of als losse bijlage/foto.

---

## 8. Foto's — afspraken

| Regel | Detail |
|---|---|
| Koppeling | Foto's als **bijlage op de note van de betreffende taak** (camera → camerataak) |
| Notetitel-conventie | `FOTO <blok> — <omschrijving>` bv. `FOTO 1.1 — Stuurkast interieur` |
| Fotoblokken | 1: Stuurkast (1.1 interieur, 1.2 exterieur, 1.3 glasvezel) · 2: Camera's (2.1–2.3) · 3: Omgeving (3.1) · 4: Schade (4.1) |
| Bijschrift | Als **notetekst** onder de bijlage |
| Toestelcamera | Werkt rechtstreeks via de Xurrent mobiele app |
| Intern vs extern | "Schade/anomalie" → kan als **interne bijlage** indien niet naar klant |

---

## 9. Bouwstap 5 — Configuratie-checklist (af te vinken door BI-team)

- [ ] Team `Techniekers PM` aangemaakt + leden toegevoegd
- [ ] Service `PM ANPR & CCTV` aangemaakt
- [ ] Request template `JACOPS — PM ANPR & CCTV` aangemaakt (velden §4)
- [ ] Workflow template `JACOPS — PM ANPR & CCTV (workflow)` aangemaakt (taken §5)
- [ ] 6 taaktemplates aangemaakt met Instructions-checklists (§6)
- [ ] 5 UI Extensions gebouwd per specificatie (§7), met **references** (§3)
- [ ] UI Extensions gekoppeld aan de juiste taaktemplates
- [ ] Verplichte velden + voorwaarden/validatie ingesteld
- [ ] Foto-conventie gedocumenteerd en gedeeld met techniekers
- [ ] Test uitgevoerd in QA (§10)
- [ ] Uitrol naar productie

---

## 10. Testen (QA → productie)

**Testscenario's:**
1. Request registreren vanuit de template → controleer of workflow + taken correct gegenereerd worden.
2. In de **mobiele app**: een taak openen, checklist afvinken, UI-Extension-velden invullen, foto toevoegen.
3. **Validatie**: verplichte velden blokkeren het afronden; NOK-conditie toont de juiste velden.
4. Camera: 3 camerataken aangemaakt, elk met eigen velden + foto's.
5. Afronden van alle taken → request status correct.
6. **Data-check**: custom fields verschijnen als JSON via de API (§11).

**Uitrol naar productie:** exporteer de UI Extensions en importeer ze in de productie-account met dezelfde **reference**. Verifieer dat de **templateId's** correct gekoppeld zijn.

---

## 11. Data-ontsluiting voor BI (API)

Alle custom fields staan als **JSON** op het record. Checklist-items zijn eveneens via de API uitleesbaar.

**Basis:**
| Item | Waarde |
|---|---|
| Base URL | `https://api.xurrent.com/v1/` |
| Authenticatie | OAuth2 (personal access token / client credentials) |
| Account-header | `X-Xurrent-Account: <account>` bij meerdere accounts |
| Docs | `https://developer.xurrent.com/` |

**Relevante endpoints:**
| Endpoint | Gebruik |
|---|---|
| `GET /requests?fields=...` | Requests ophalen (o.a. `sourceID`, `subject`, `custom_fields`, `template`) |
| `GET /requests/{id}` | Detail incl. `custom_fields` + `custom_fields_attachments` |
| `GET /tasks` / `GET /tasks/{id}` | Taken + hun `custom_fields` |
| `GET /request_templates`, `/task_templates` | Template-metadata |
| Bulk API | Grote export in één call |
| Webhooks API | Real-time notificatie bij wijziging (voor BI-sync of AI-trigger) |

**Praktische BI-query (concept):**
```
GET /requests?template=JACOPS — PM ANPR & CCTV
    &fields=id,sourceID,subject,custom_fields,created_at,completed_at
```
Daarna `custom_fields` (JSON) flattten naar kolommen; taken joinen op `request.id`.

**Voor het AI-rapport:** de `custom_fields` + checklist-items vormen samen de gestructureerde input voor de AI-prompt (zie `Uitwerking_Fase0_Fase1.md`).

**Idempotentie / herkenning:** gebruik `sourceID` (bv. ISD-/ticketnummer) als externe sleutel.

---

## 12. Wat native NIET kan (latere fases)

| Gemis | Impact | Oplossing later |
|---|---|---|
| Offline | Groot op bereikloze locaties | Fase 1 (Power Apps) of Fase 2 (Dataverse) |
| Automatische GPS | Manueel veld | Fase 1 (Location-connector) |
| Digitale handtekening | Niet native | Fase 1 (Pen input) of maatwerk-HTML |
| Echt grid/matrix | Opgelost via taak-per-camera | — |
| Branded PDF-export | Geen native PDF | AI-prompt of Power Automate (premium) |

---

## 13. Openstaande beslissingen (vóór de bouw)

1. **Status per checklistpunt of enkel afwijkingen?** (bepaalt het aantal UI-extension-velden)
2. **Aantal camerataaken** standaard (3? configureerbaar?) en of "extra camera's" als vrije taak.
3. **Tweetalig** verplicht op elk veld/checklistpunt of enkel op het eindrapport?
4. **Handtekeningen** in scope of niet (native niet mogelijk).
5. **E-mailbrug** gewenst? (enkel relevant als later met een veld-app gewerkt wordt — zie §14)
6. Koppeling aan **Sites/CI's** nu of later.

---

## 14. Belangrijk: de e-mailbrug (context voor BI-team)

De e-mailbrug (Xurrent Mail API: nieuwe request via inbound mail, of update met `source`/`sourceID` vooraan de body) is **niet nodig** zolang de technieker **in Xurrent zelf** werkt — dan is er niets te overbruggen.

De brug wordt **pas relevant in Fase 1**, wanneer de technieker in een **Power App** werkt en het resultaat naar Xurrent moet. Het is dan puur **dataoverdracht** (voorkomt manueel overtypen), geen UX-verbetering. Alternatieven zodra premium beschikbaar is: **HTTP/API** of **Xurrent iPaaS/Workato**.

---

## 15. Definition of Done

- Een technieker kan in de **mobiele app** een PM-beurt volledig uitvoeren: checklist afvinken, status/waarden/opmerkingen invullen, foto's per type toevoegen.
- Alle gegevens zijn **gestructureerd** terug te vinden (custom fields JSON) via de API.
- De flow is **gedocumenteerd** (deze handleiding + interne werkinstructie voor techniekers).
- Getest in QA, uitgerold naar productie, foto-conventie gekend bij de techniekers.

---

## Bijlagen
- `Xurrent_Checklist_Voorbeeld.md` — detailvoorbeeld + klassieke HTML-snippet.
- `Uitwerking_Fase0_Fase1.md` — Fase 0 vs Fase 1 + AI-rapport + JSON-schema/prompt.
- `Analyse_Digitale_Onderhoudschecklist.md` — oorspronkelijke analyse & opties.
