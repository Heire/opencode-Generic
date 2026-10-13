# AI-modelroutering voor OpenCode — installatie en gebruik

Deze map bevat:

| Bestand | Wat |
|---|---|
| `opencode.json` | Kant-en-klare configuratie: taakrouter + 8 specialist-agents + 7 commando's |
| `rapport-ai-modellen-jacops.pdf` | Volledig rapport (analyse, kostenanalyse OpenCode vs. directe API's, privacy-analyse) |
| `rapport-ai-modellen-jacops.html` | HTML-bron van het rapport (huisstijl aanpasbaar) |
| `genereer_rapport.py` | Python-script dat het rapport opnieuw genereert (WeasyPrint; valt automatisch terug op Microsoft Edge headless als GTK-bibliotheken ontbreken — wat op deze pc het geval is) |

---

## 1. Installeren

Kopieer `opencode.json` naar één van deze locaties:

- **Per project** (aanbevolen voor JACOPS-projecten): projectroot, naast `README.md`
- **Globaal** (voor al je sessies): `~/.config/opencode/opencode.json`

Daarna in OpenCode:
1. Verbind minstens één provider: `/connect` → **OpenCode Go** (abonnement) en/of **OpenCode Zen** (pay-as-you-go).
2. Controleer de modellen: `/models`.
3. De router staat standaard aan (`default_agent: "router"`).

> Modellen die via Zen lopen (Claude Sonnet 5.5, Mistral Large 4, Qwen3.8 Max) vereisen Zen-saldo.
> Wil je enkel met het Go-abonnement werken? Vervang in `opencode.json`:
> - `opencode/claude-sonnet-5-5` → `opencode-go/glm-5.3-flash`
> - `opencode/qwen3.8-max` → `opencode-go/qwen3.8-flash`
> - `opencode/mistral-large-4` → `opencode-go/deepseek-v4.1-flash`

## 2. Hoe de automatische keuze werkt

OpenCode heeft geen ingebouwde promptclassificatie; de configuratie gebruikt drie officiële mechanismen:

| Mechanisme | Werking | Gebruik |
|---|---|---|
| **Router-agent** (`default_agent`) | Een goedkoop model (GPT-6 Luna) leest je vraag, klasseert ze en delegeert via de Task-tool naar de juiste specialist-subagent. Elke specialist heeft zijn eigen model. | Automatisch — gewoon je vraag typen |
| **Subagents** (`@naam`) | Je roept zelf een specialist aan. | `@lastenboek-analist analyseer bijlage 4` |
| **Commando's** (`/naam`) | Deterministische route met vast model. | `/vba macro.xlsm`, `/pdf interventierapport werf 12` |

Handmatig wisselen blijft mogelijk met **Tab** (primaire agents: router / build / plan).

### Taaktype → model (samengevat)

| Taaktype | Agent | Model | Prijs/sessie (90M-mix) |
|---|---|---|---|
| Routeren/classificeren | router | GPT-6 Luna (Go) | ~$0,01 |
| PDF maken & styling | pdf-designer | Claude Sonnet 5.5 | ~$35,64 |
| OCR & PDF lezen | ocr-extractie | Qwen3.8 Max | ~$37,33 |
| Excel & Word | office-excel-word | Claude Sonnet 5.5 | ~$35,64 |
| VBA & Office-automatisering | vba-specialist | Claude Sonnet 5.5 | ~$35,64 |
| Lastenboeken & bestekken | lastenboek-analist | Mistral Large 4 (EU) | ~$11,48 |
| Vertrouwelijk werk (EU) | vertrouwelijk-werk | Mistral Large 4 (EU) | ~$11,48 |
| Snelle assistentie | snelle-vraag | Claude Haiku 5.5 (Go) | ~$1,78 |
| Dagelijks coderen | build | DeepSeek V4.1 Flash (Go) | ~$1,59 (off-peak) |
| Alles uit het algemene | general | DeepSeek V4.1 Flash (Go) | ~$1,59 |

## 3. Tips

- **Piekuren DeepSeek** (Go/direct): 01:00–04:00 en 06:00–10:00 UTC op weekdagen = vol tarief; alle andere uren halve prijs.
- **Caching**: laat sessies lang genoeg leven zodat de promptcache rendeert (95%+ cache-hits zijn realistisch in OpenCode).
- **Nooit vertrouwelijke data** naar Contributor-modellen (Muse Spark 1.3 Contributor) of gratis modellen met trainingsclausule (Big Pickle, Cat Jam, Exo, MiMo-free, Ling-free, Nemotron-free).
- **Budgetbewaking**: in de console kun je maandlimieten instellen; op Go valt het systeem bij limietoverschrijding terug op gratis modellen (of je Zen-saldo als "Use balance" aan staat).
