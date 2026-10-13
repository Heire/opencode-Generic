# Uitwerking Fase 0 & Fase 1 — Digitale onderhoudschecklist

**Context:** `JACOPS_Preventief_Onderhoud_ANPR_CCTV_V2.xlsx` digitaal maken binnen de bestaande ecosystemen (Xurrent + O365/Teams) en gratis opties. Later eventueel een betaald platform.

**Uitgangspunt extra:** de ingevulde checklist mag ook gewoon **gestructureerde data** zijn die daarna via een **AI-prompt** in de eigen templatesjabloon tot een (intern) rapport wordt verwerkt. Dat verlaagt de eisen: we hebben dan geen kant-en-klare PDF-flow nodig.

Twee scenario's:

- **Fase 0 — Xurrent-native** (enkel Xurrent, geen extra tooling)
- **Fase 1 — Power Platform in de eigen tenant** (Power Apps + SharePoint + Power Automate + Teams, gratis met M365)

---

## Fase 0 — Xurrent-native

### Opzet
1. **Task-/requesttemplate** "Preventief onderhoud ANPR & CCTV".
2. **Checklist in Instructions**: de 16 straatkast-controles als afvinkbare lijst in het *Instructions*-veld van de template.
3. **UI Extension** op de template: aangepaste velden voor de secties die geen simpele afvinking zijn (status, GPS, as-built, afwijkingen, afmelding).
4. **Note + Attachments**: opmerkingen en foto's als bijlagen op de taak/request.
5. Technieker werkt af via de **Xurrent mobiele app** (checklist + custom fields renderen ook daar).

### Wat kan wél
| Onderdeel Excel | Fase 0 |
|---|---|
| Afvinklijst 16 controles | ✅ checklist in instructions (met audit trail) |
| Status OK/NOK/WARN | ✅ via UI-Extension-veld (select) per sectie/controle |
| Algemene info, site-ID, technieker | ✅ via UI-Extension-velden |
| GPS-coördinaten | ✅ als **tekstveld** (manueel ingevuld) |
| As-built inventaris | ✅ als vaste veldset (of deels in note) |
| Afwijkingen/acties, offerte nodig, etc. | ✅ select/text velden |
| Foto's | ⚠️ als **bijlage op de taak** (niet per item gekoppeld) |
| Koppeling aan ticket | ✅ **native** (het ís het ticket/de taak) |
| Structuur als data voor AI | ✅ custom fields = JSON, uitleesbaar via API |

### Wat kan niet / beperkt
| Beperking | Impact |
|---|---|
| **Geen offline** | Web + mobiele app hebben verbinding nodig → grootste pijnpunt op terrein |
| **Geen automatische GPS** | Manueel intypen |
| **Geen digitale handtekening** | Enkel als (hacky) custom HTML in de klassieke builder |
| **Foto's niet per checklist-item** | Alles hangt als losse bijlage aan de taak |
| **Geen echte herhalende tabel** | De per-camera matrix (5 punten × N camera's) is moeilijk als grid; wordt een rij velden per camera of tekst |
| **Veel velden = omslachtig formulier** | 16 controles + matrix + as-built als custom fields wordt lang op een gsm |
| **Geen branded PDF-export** | Xurrent genereert geen ingevuld verslag; moet extern (bv. AI of Power Automate) |

### Wanneer Fase 0 kiezen
- Je wil **snel, zonder extra tooling/kost**, de checklist aan het ticket koppelen.
- De check zonder foto/GPS/handtekening is **"goed genoeg"** als eerste stap.
- Je wil vooral de **ticket-integratie** (wie, wat, wanneer) verbeteren.

---

## Fase 1 — Power Apps + SharePoint + Power Automate + Teams (gratis)

> Draait volledig op de **seeded Power Platform-rechten** in je M365-licenties: canvas apps + Power Automate met **standaardconnectors**. Geen extra licentie nodig zolang je geen premium connectors gebruikt.

### Opzet (architectuur)
```
[Power Apps canvas app op gsm/tablet]
        │  schrijft
        ▼
[SharePoint Lists]  (Hoofdformulier + Checklist-items + Camera-matrix + Foto's)
        │  triggert
        ▼
[Power Automate]  (standaardconnectors)
        ├─ formatteert de inzending tot een nette, AI-klare tekst/JSON
        ├─ e-mailt naar het Xurrent inbound-adres  →  request/note + bijlagen
        └─ post notificatie/kaart in Teams
        ▼
[AI-prompt met eigen templatesjabloon]  →  rapport naar de klant
```

### Wat kan wél
| Onderdeel Excel | Fase 1 |
|---|---|
| Checklist 16 controles + status | ✅ Power Apps + SharePoint-lijst |
| Per-camera matrix | ✅ **herhalende gallery** (echte rijen per camera) |
| As-built inventaris | ✅ herhalende lijst |
| **Foto's** | ✅ **Camera-control** + koppeling aan item, opslag in SharePoint |
| **Automatische GPS** | ✅ Location-connector (standaard) |
| **Handtekening** | ✅ Pen input-control |
| Tweetalige labels NL/FR | ✅ vrije labels |
| Conditionele validatie (NOK → verplicht opmerking/foto) | ✅ formules |
| Koppeling naar Xurrent | ✅ **via e-mail** (standard Outlook-connector) naar Xurrent Mail API → request/note + bijlagen |
| In Teams beschikbaar | ✅ als **Teams-tab** |
| Databron voor AI | ✅ SharePoint-item + JSON export |

### Wat kan niet / beperkt (belangrijk!)
| Beperking | Detail |
|---|---|
| **Offline is niet gratis "native"** | Échte offline-first canvas/mobile offline werkt **alleen met Dataverse** (premium). Met SharePoint moet je de fragiele `SaveData()/LoadData()`-truc zelf bouwen; foto's offline wegschrijven is lastig |
| **Geen premium connectors** | Directe **HTTP-call naar de Xurrent REST API kan niet** op M365-seeded (HTTP = premium). Daarom de **e-mailbrug** (Outlook = standaard) |
| **Geen Word/PDF-flow** | `Populate a Microsoft Word template` + `Convert to PDF` = **Premium** (Word Online Business connector). Gratis alternatief = **AI doet het rapport** |
| **Zelf bouwen & onderhouden** | Geen kant-en-klare tool; je onderhoudt de app zelf (governance, DLP, omgevingen) |
| **Foto-opslag** | Foto's in SharePoint → let op opslag en performance; comprimeer |
| **Actielimiet** | M365-seeded = **6.000 acties/dag**; ruim voldoende voor jullie volume |
| **AI-stap niet automatiseerbaar zonder premium** | AI Builder / Azure OpenAI = premium; gratis = mens paste de output in de AI met de sjabloonprompt |

### Wanneer Fase 1 kiezen
- Je wil **foto, GPS, handtekening, tweetalige velden en echte matrices** — gratis.
- Techniekers hebben **meestal verbinding** (offline is "nice to have").
- Je accepteert **zelf bouwen/onderhouden** in ruil voor €0 extra licentie.

---

## De AI-rapport-route (in beide fases)

Jullie idee: de checklist levert **gestructureerde data**, een AI-prompt maakt daar het rapport in de eigen templatesjabloon van.

### Hoe
1. Technieker vult de digitale checklist in (Fase 0 of 1).
2. De output wordt als **nette, gesectioneerde tekst/JSON** samengevat.
3. Die tekst plak je (of stuurt de flow) in een **AI met vaste prompt + jullie sjabloon** → rapport NL/FR.

### Aanbevolen outputformaat (AI-vriendelijk)
Hou vaste sleutels en secties aan, zodat de prompt stabiel werkt en de AI niets hoeft te raden:

```json
{
  "meta": { "ticket": "ISD-2026-00123", "site_id": "...", "datum": "2026-10-13",
            "technicus": "...", "aankomst": "09:10", "vertrek": "11:40" },
  "locatie": { "stuurkast_id": "...", "gps_kast": "50.123,4.456",
               "gemeente": "...", "locatietype": "Kruispunt" },
  "algemene_status": "OK",
  "algemene_opmerkingen": "...",
  "checklist_kast": [
    { "nr": 1, "punt": "Visuele inspectie binnenzijde", "status": "OK", "waarde": "", "opmerking": "" },
    { "nr": 6, "punt": "Voeding MeanWell EDR-150-24", "status": "NOK", "waarde": "23.8 V", "opmerking": "Onder spanning, vervangen voorgesteld" }
  ],
  "cameras": [
    { "id": "Cam 1", "positie": "links", "reiniging": "OK", "leds": "OK",
      "fixatie": "OK", "zichtveld": "OK", "anpr": "OK", "overall": "OK", "opmerking": "" }
  ],
  "as_built": [ { "component": "Voeding (PSU 24V)", "merk": "MeanWell EDR-150-24",
                  "serienr": "", "ip": "n.v.t.", "ok": true, "opmerking": "" } ],
  "afwijkingen": "...",
  "acties": "...",
  "herstelling_ter_plaatse": false,
  "offerte_nodig": false,
  "vervangstuk_nodig": false,
  "afmelding": { "call_gedaan": true, "contactpersoon": "...", "tijdstip": "11:30",
                 "zware_schade_gemeld": false },
  "fotos": [ { "blok": "1.1", "titel": "Stuurkast interieur", "bijschrift": "..." } ],
  "handtekening_technicus": "aanwezig", "handtekening_validatie": "aanwezig"
}
```

### Voorbeeld AI-prompt (sjabloon)
```
Je bent een technisch verslaggever van Jacops Security.
Hieronder staat de ingevulde preventief-onderhoud checklist ANPR & CCTV als JSON.
Genereer het interventieverslag exact volgens de structuur en huisstijl van het
meegeleverde sjabloon. Regels:
- Tweetalig: Nederlands én Frans, dezelfde secties in dezelfde volgorde.
- Secties: 1 Algemene info, 2 Locatie & GPS, 3 Algemene status, 4 Checklist kast,
  5 Camera's, 6 As-built, 7 Afwijkingen & acties, 8 Afmelding, 9 Handtekeningen.
- Toon per checklistpunt status + opmerking; groepeer NOK/WARN onder "Aandachtspunten".
- Vermeld expliciet of offerte/vervangstuk nodig is en of ter plaatse hersteld is.
- Verzin niets; laat velden leeg indien ontbrekend. Toon waarden en eenheden correct.
- Sluit af met de vertrouwelijkheidsclausule.
DATA:
<<< hier de JSON of de nette tekst >>
```
> Bewaar deze prompt + jullie sjabloon op één vaste plek (bv. Teams-bestand), zodat iedereen hetzelfde rapport krijgt.

### AI-opties (gratis → betaald)
| Optie | Kost | Automatiseerbaar in flow? |
|---|---|---|
| **Microsoft 365 Copilot** (Teams/Word) | vergt M365 Copilot-licentie | ⚠️ beperkt; vooral mens-in-de-lus |
| **Copilot chat / andere chat-LLM** | gratis | ❌ manueel plakken |
| **Power Automate AI Builder (GPT-prompt)** | **premium** | ✅ volledig in de flow |
| **Azure OpenAI** | verbruikskost | ✅ volledig, via API (premium connector of Azure Function) |

**Gratis werkwijze:** checklist → gestructureerde tekst → mens plakt in de AI met de vaste prompt → rapport. Dat vraagt **geen** premium licentie.
**Later (Fase 2/3):** AI-stap in de flow automatiseren (AI Builder/Azure OpenAI) → rapport automatisch bij het ticket.

---

## Vergelijking Fase 0 vs Fase 1

| | Fase 0 — Xurrent-native | Fase 1 — Power Apps + SharePoint |
|---|---|---|
| Kost | €0 (inbegrepen) | €0 (seeded licentie) |
| Bouwinspanning | Laag | Middel–hoog (zelf bouwen) |
| Offline | ❌ | ⚠️ enkel DIY |
| Foto per item | ❌ (losse bijlage) | ✅ |
| Automatische GPS | ❌ | ✅ |
| Handtekening | ❌ (hacky) | ✅ |
| Per-camera matrix | ⚠️ moeizaam | ✅ |
| Tweetalige labels | ✅ | ✅ |
| Koppeling ticket | ✅ native + API | ✅ via Xurrent Mail API (e-mailbrug) |
| PDF/rapport | extern (AI) | extern (AI) — Word/PDF-flow is premium |
| In Teams | Xurrent-app | ✅ als Teams-tab |
| Geschikt als pilot | ✅ snel | ✅ volledig |

---

## Aanbevolen aanpak

1. **Start met Fase 0 als quick win** (deze week te realiseren): task-template + checklist in instructions + UI-Extension-velden + foto's als bijlage. Zo hangt de check meteen aan het ticket.
2. **Bouw Fase 1 als de echte terrein-app** (foto, GPS, handtekening, matrix), gratis, met de **e-mailbrug** naar Xurrent en de **AI-prompt** voor het rapport.
3. **Meet** of techniekers zonder bereik werken. Is offline écht nodig → dan is dat exact het punt om **Fase 2** (Power Apps Premium + Dataverse, ~$20/gebruiker/maand) of een dedicated tool te verantwoorden.

---

## Openstaande verificaties
- Exacte Power Platform-rechten per M365-plan in jullie tenant (seeded Power Apps + Power Automate).
- Offline-gedrag van de Xurrent mobiele app op een bereikloze locatie.
- Xurrent **Email Policy**: staat "Allow inbound email to generate new requests" aan, en welk inbound-adres gebruiken we?
- Beschikbaarheid van Microsoft 365 Copilot in jullie tenant (bepaalt de AI-werkwijze).
