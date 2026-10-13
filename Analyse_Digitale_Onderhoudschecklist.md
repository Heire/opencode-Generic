# Analyse — Digitale onderhoudschecklist ANPR & CCTV

**Doel:** het huidige Excel-formulier (`JACOPS_Preventief_Onderhoud_ANPR_CCTV_V2.xlsx`) omzetten naar een terreinvriendelijke digitale checklist voor techniekers (tablet/gsm), met maximale inzet van de **bestaande ecosystemen (Xurrent + O365/Teams)** en gratis opties. Pas later een betaald platform indien nodig.

**Status:** analyse / fase 0 — nog geen implementatie.

---

## 1. Wat het huidige Excel bevat

- Tweetalig (NL/FR), 9 secties: algemene info, GPS-coördinaten, algemene status, **16 straatkast-controles** (OK/NOK/WARN), **per-camera matrix** (5 controlepunten + overall), as-built inventaris, afwijkingen/acties, afmelding/closure, handtekeningen.
- Apart **fotoreportage-blad** met 8 fotoblokken + bijschriften.
- Vaste keuzelijsten (OK, GOED, Ja/Nee, N.v.t.) en vaste merkmodellen (MeanWell, Phoenix, HW Group, Westermo, GigaMedia…).

### Waarom Excel op terrein knelt
- Moeilijk invullen op gsm/tablet (touch, handschoenen, regen).
- Geen echte **offline** werking.
- Foto's **manueel** invoegen, geen koppeling aan de juiste sectie.
- **GPS manueel** intypen.
- Geen **digitale handtekening**.
- Geen **validatie** (bv. NOK verplicht opmerking/foto).
- Resultaat **handmatig overtypen** naar het Xurrent-ticket.

---

## 2. Functie-eisen (afgeleid uit het formulier)

| # | Eis | Prioriteit |
|---|-----|-----------|
| R1 | Offline kunnen werken op terrein | Hoog (vaak beslissend) |
| R2 | Foto's maken + bijschrift/annotatie per sectie | Hoog |
| R3 | Automatische GPS-coördinaten | Middel |
| R4 | Digitale handtekening (technicus + validatie) | Hoog |
| R5 | Gestructureerde checklist (OK/NOK/WARN + per-camera matrix) | Hoog |
| R6 | Herhalende rijen (per camera, as-built inventaris) | Middel |
| R7 | Tweetalige labels NL/FR | Middel |
| R8 | PDF-output naar eindklant in huisstijl | Hoog |
| R9 | Terugvloeien naar Xurrent-ticket (ISD-/ticketnr) | Hoog |
| R10 | Conditionele validatie (NOK → opmerking/foto verplicht) | Middel |
| R11 | Audit trail (wie/wat/wanneer) | Middel |

---

## 3. Analyse van de bestaande/gratis tools

### 3.1 Xurrent (bestaand)

| Functie | Wat kan | Wat niet |
|---|---|---|
| **Checklists in Instructions** | Afvinklijst in request/task-template; wordt geauditeerd, uitleesbaar via API | Enkel afvinken — geen status/waarde, foto, GPS of handtekening per item |
| **Task-/workflowtemplates** | Onderhoudsbeurt als gestructureerde taak | Geen veldformulier |
| **Bijlagen op request/task** | Foto's/PDF als bijlage | Manueel; niet gekoppeld aan checklist-item |
| **UI Extensions** (visuele designer) | Eigen formulier/scherm met aangepaste velden, secties, keuzelijsten; kan Xurrent-API aanroepen | Draait in browser → **geen offline**; rijke device-features beperkt |
| **Mobiele app** | Technieker vinkt af en werkt tickets af | Offline-gedrag te verifiëren |
| **REST API** (`developer.xurrent.com`) | Requests/taken/notities/bijlagen aanmaken en uitlezen | — |

**Verdict:** uitstekend voor ticket-tracking en de afvinklijst; **zwak op terrein** (foto/GPS/handtekening/offline).

### 3.2 Microsoft Forms (gratis met O365)
- ✅ Structuur, tweetalig, branchlogica, resultaten in Excel/SharePoint.
- ❌ **Geen offline**, geen echte handtekening, GPS niet automatisch, bestandsupload beperkt.
- **Verdict:** ongeschikt voor terrein.

### 3.3 Power Apps canvas app + SharePoint Lists (seeded licentie, gratis)
- ✅ Camera-control, pen-handtekening, locatie-connector (standaard), herhalende databron, validatie, tweetalige labels.
- ✅ PDF via Word-template + Power Automate; te publiceren als **Teams-tab**.
- ✅ Koppeling naar Xurrent via de REST API (HTTP-actie of custom connector).
- ⚠️ **Offline:** native offline werkt **niet** met SharePoint; enkel via de DIY `SaveData()/LoadData()`-methode — werkbaar maar fragiel, foto's lastig, geen achtergrond-sync.
- **Verdict:** het **hoogste gratis niveau** in het ecosysteem — volledig online prima, offline beperkt.

### 3.4 Dataverse for Teams (gratis met Teams)
- ✅ Krachtige datalaag, relationeel, file/image, apps direct in Teams.
- ❌ **Geen mobile offline**, geen API-toegang, 2 GB/team.
- **Verdict:** mooie gratis opstap, maar lost offline niet op.

### 3.5 Microsoft To Do / Planner / Forms in Teams (gratis)
- ✅ Alleen eenvoudige afvinklijsten.
- ❌ Geen foto/GPS/handtekening/PDF-verslag.
- **Verdict:** tussenoplossing voor "afvinken", niet voor het verslag naar de klant.

### 3.6 Gratis tiers van gespecialiseerde formulier-tools (buiten ecosysteem)
- Voorbeelden: Jotform, SafetyCulture, Kizeo Forms, GoCanvas, Fulcrum, Formstack.
- ✅ Offline-first, foto+annotatie, GPS, handtekening, PDF in huisstijl, conditionele logica, API/Zapier-koppeling.
- ❌ Gratis laag is meestal **te krap** (limiet op inzendingen/gebruikers/opslag); nog een extra eiland.
- **Verdict:** ideaal voor een **pilot** om te bewijzen dat het werkt, niet voor volledige uitrol.

---

## 4. Vergelijkingsmatrix

| Tool | R1 Offline | R2 Foto | R3 GPS | R4 Handtekening | R5–R7 Structuur/NL-FR | R8 PDF | R9 Xurrent | Kost |
|---|---|---|---|---|---|---|---|---|
| Xurrent native | ⚠️ te verifiëren | ❌ (bijlage) | ❌ | ❌ | ✅ / ✅ | ⚠️ | ✅ native | Inbegrepen |
| Microsoft Forms | ❌ | ⚠️ | ❌ | ❌ | ✅ / ✅ | ✅ (via PA) | Via PA | Inbegrepen |
| Power Apps + SharePoint (seeded) | ⚠️ DIY | ✅ | ✅ | ✅ | ✅ / ✅ | ✅ | Via API | Inbegrepen |
| Dataverse for Teams | ❌ | ✅ | ✅ | ✅ | ✅ / ✅ | ✅ | Via API* | Inbegrepen |
| Form-tool (gratis laag) | ✅ | ✅ | ✅ | ✅ | ✅ / ✅ | ✅ | Via API/Zapier | Gratis (limieten) |

\* API-toegang op Dataverse for Teams is beperkt.

**Conclusie:** het enige écht gratis knelpunt is **R1 (offline)**. Alles behalve offline is gratis haalbaar in het ecosysteem. Offline is precies het punt dat later een betaalde licentie of platform rechtvaardigt.

---

## 5. Gefaseerd voorstel (gratis → betaald)

### Fase 0 — Quick win in Xurrent (nu, gratis)
- Onderhoudsbeurt als **task-template** met **checklist in instructions**.
- Foto's voorlopig als **bijlagen** op de taak/request.
- **Resultaat:** directe verbetering t.o.v. Excel (afvinken op gsm, gekoppeld aan ticket), **geen** volwaardig veldformulier.

### Fase 1 — Power Apps in het ecosysteem (gratis, seeded licentie)
- **Canvas app** op **SharePoint Lists** (of Dataverse for Teams): checklist, per-camera matrix, as-built, foto, GPS, handtekening.
- **Power Automate**: PDF genereren (Word-template) + naar Xurrent-ticket duwen via de API; notificatie/approval via Teams.
- Publiceren als **Teams-tab**.
- **Resultaat:** volwaardig digitaal formulier, in jullie tenant, zonder extra licentie. **Offline = beperkt (DIY).**

### Fase 2 — Power Apps Premium + Dataverse (betaald, blijft in ecosysteem)
- **$20/gebruiker/maand** (per-app SKU wordt uitgefaseerd sinds jan 2026).
- **Échte offline-first** canvas/model-driven app + Dataverse, achtergrond-sync, robuuste foto-opslag.
- **Resultaat:** professionele terrein-app binnen Microsoft. Meest logische "aankoop op termijn".

### Fase 3 — Gespecialiseerde field-form-tool (betaald, dedicated)
- SafetyCulture / Kizeo / GoCanvas / Fulcrum e.d.: offline-first, snel live, beste terrein-UX.
- **Nadeel:** extra platform + licentiekost + integratie naar Xurrent.

---

## 6. Het kantelmoment

> **Zolang offline niet strikt nodig is, kan alles gratis in het ecosysteem (Fase 0/1).** Zodra offline betrouwbaar moet werken met foto's en sync, is dat het punt waarop een betaalde licentie (Fase 2) of een gespecialiseerde tool (Fase 3) zich terugverdient.

---

## 7. Aanbevolen eerste stappen

1. **Verifieer in jullie tenant** welke Power Platform-rechten in de M365-licenties zitten (seeded Power Apps + Power Automate standaardconnectors).
2. **Test offline-gedrag van de Xurrent mobiele app** op een straatkast-zonder-bereik.
3. **Bepaal hoe vaak** techniekers écht zonder bereik werken → bepaalt of Fase 1 volstaat of Fase 2 nodig is.
4. **Bouw een Fase 1-prototype**: SharePoint-lijstenschema + Power Apps-schermen + Power Automate-flow (PDF + Xurrent).
5. **Pilot met 1–2 techniekers**, evalueer, en beslis daarna over Fase 2/3.

---

## 8. Nog te verifiëren

- Exacte Power Platform-rechten per M365-plan in jullie tenant.
- Offline-capaciteit Xurrent mobiele app.
- Of de Location-connector onder de seeded licentie valt.
- Exacte Xurrent API-mogelijkheden voor het wegschrijven van checklist-resultaten en foto's.
