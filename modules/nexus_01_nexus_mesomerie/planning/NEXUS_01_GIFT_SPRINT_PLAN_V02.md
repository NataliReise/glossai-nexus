# Nexus 01 Sprintplan — Geschenkfassung

## Document status

- Version: 0.2
- Status: Current
- Date: 2026-07-18
- Supersedes: Version 0.1
- Purpose: Current gift-release sprint plan after the Slice 1 technical inventory and the repeatable Resonance-cycle clarification.

## Ziel

Bis zur Übergabe entsteht eine atmosphärisch überzeugende, sichere und gut zugängliche Geschenkfassung von Nexus 01.

## Sprintprinzip

> Erst die Spielgrammatik sichern.  
> Dann die kleinste funktionierende Umsetzung bauen.  
> Danach spielen, prüfen und nur noch gezielt verbessern.

---

## Rollen im Sprint

### Natali

- trifft die konzeptionellen und sprachlichen Entscheidungen;
- bewertet das tatsächliche Spielgefühl;
- führt die entscheidenden manuellen Durchläufe aus;
- entscheidet über Commit, Push und Merge.

### Synthea

- bündelt die Ideen;
- trennt Architektur, Spielerlebnis und Text;
- formuliert enge Codex-Aufträge;
- prüft Codex-Berichte und Diffs;
- bewahrt den roten Faden und warnt vor unnötiger Ausweitung.

### Codex

- untersucht die vorhandene Implementierung;
- setzt klar abgegrenzte Änderungen um;
- ergänzt fokussierte Tests;
- führt nur die ausdrücklich erlaubten Befehle aus;
- erstellt keine Branches oder Pushes ohne ausdrückliche Freigabe.

---

# A. Sprintregeln

## Git-Sicherheit

Während einer Umsetzungsscheibe:

```text
keine neue Branch
kein Branchwechsel
kein Pull
kein Fetch
kein Merge
kein Rebase
kein Cherry-pick
kein Reset
kein Restore
kein Stash
kein Push
```

Commits werden nur für zuvor klar abgegrenzte und geprüfte Dateien erstellt.

Vor technischen Änderungen:

```bash
cd ~/Schreibtisch/glossai-nexus
git branch --show-current
git status --short
git diff --stat
git diff > ~/Schreibtisch/nexus-01-sprint-backup.patch
```

Die Patch-Datei ist nur eine zusätzliche Rettungskopie und verändert das Repository nicht.

## Scope-Schutz

Neue Ideen werden nicht verworfen, aber in drei Gruppen eingeordnet:

```text
MUSS in die Geschenkfassung
SOLLTE hinein, falls klein und sicher
SPÄTER
```

Während einer laufenden Umsetzungsscheibe wird der Scope nicht erweitert.

---

# B. Bereits erreicht

- [x] First Spark ist in das gemeinsame Atrium integriert.
- [x] Die Resonance Chamber besitzt die drei gegenwärtigen Eintrittsgestalten:
  - `COMPOSE`
  - `ANSWER`
  - `BLOCKED_ANSWER_RECOVERY`
- [x] Geschenk-, Antwort- und Rückgabewege sind technisch vorhanden.
- [x] Die sichere Trennung von Einladung und privatem Return Workspace ist umgesetzt.
- [x] Die kompakte Nachhallform ist festgelegt.
- [x] Die gemeinsame Nexus-01-Spielgrammatik ist lokal dokumentiert.
- [x] Die erste sprachliche Überarbeitung der Resonance-Flows ist lokal umgesetzt.
- [x] Das kanonische Status- und Ergebniskonzept wurde als V0.1 formuliert.
- [x] Die technische Bestandsaufnahme für Slice 1 wurde ohne Dateiänderungen abgeschlossen.
- [x] `TerminalChamberIO` wurde als kleinste Interaktionsnaht bestätigt.
- [x] Die Resonance Chamber wurde konzeptionell als wiederholbarer Raum mit unabhängigen Resonanzzyklen präzisiert.
- [x] Keine Branch- oder Push-Operation wurde im aktuellen Sprintstand vorgenommen.

---

# C. Verbindliche Spielidee

## Gemeinsame Erkundungsgrammatik

```text
Raum wahrnehmen
-> Umgebung erkunden
-> Spuren entdecken
-> lokales Vokabular erschließen
-> bei Bedarf Hilfe oder Führung anfordern
-> handeln
-> Veränderung beobachten
```

## Unterschiedliche Textebenen

| Ebene | Aufgabe |
|---|---|
| Raumtext / `look` | Atmosphäre, Gegenstände und Veränderungen zeigen |
| Spuren / `trace` | Aufmerksamkeit poetisch lenken |
| `help` | gegenwärtige Befehle und Eingaben erklären |
| Chamber-Stimme | lokal und zustandsabhängig antworten |
| `walkthrough` | nach Zustimmung Schritt für Schritt führen |
| Systemtext | technische Folgen knapp bestätigen |
| `results` | vorhandene lokale Ergebnisse erneut zugänglich machen |

## Grundsatz

> Der Raum zeigt.  
> Die Spuren deuten.  
> Die Hilfe erklärt.  
> Die Stimme antwortet.  
> Der Walkthrough führt — aber nur, wenn er eingeladen wird.  
> Das System bestätigt nur, was wirklich geschehen ist.

## Terminaldarstellung

Die Ausgabe der Chamber soll leicht vom linken Terminalrand abgesetzt werden, damit längere Texte angenehmer lesbar sind.

```text
0 Leerzeichen   Überschriften, Eingabeprompts, wichtige Systemgrenzen
2 Leerzeichen   Raumtexte, Chamber-Stimme, Traces, Help-Einträge, Auswahlmöglichkeiten
4 Leerzeichen   Ergebnisdetails und lokale Dateipfade
```

Die Einrückung ist eine Darstellungsregel und soll nicht einzeln in die literarischen Texte eingebaut werden.

Für den Sprint genügt eine kleine zentrale Formatierungsfunktion innerhalb der Resonance Chamber. Dynamische Terminalbreiten und aufwendiger automatischer Zeilenumbruch werden vertagt.

Nach `look`, `help`, `trace` oder einer abgelehnten Walkthrough-Aktivierung wird der vollständige unveränderte aktuelle Eingabekontext erneut dargestellt.

---

# D. Zustandsmodell

Wir unterscheiden sechs unabhängige Ebenen.

## 1. Atriumstatus

```text
nicht aktiviert / nicht sichtbar
offen
Recovery-Zugang
mindestens ein erfolgreicher Zyklus abgeschlossen
```

Das Atrium entscheidet über Sichtbarkeit, Betretbarkeit und modulweite Meilensteine.

Ein abgeschlossener Zyklus verbraucht die Resonance Chamber nicht.

## 2. Eintrittsgestalt

```text
COMPOSE
ANSWER
BLOCKED_ANSWER_RECOVERY
LEGACY_CONTROLLER
```

Der Eintrittspfad bestimmt die Grundgestalt der Resonance Chamber.

`LEGACY_CONTROLLER` bleibt ein technischer Kompatibilitätspfad und kein vierter kanonischer `ResonanceMode`.

## 3. Resonanzzyklus

Jeder produktive Durchlauf besitzt einen eigenen Zustand:

```text
nicht begonnen
aktiv
abgebrochen
fehlgeschlagen
erfolgreich abgeschlossen
```

Nicht die gesamte Chamber, sondern ein einzelner Resonanzzyklus wird abgeschlossen.

Nach einem erfolgreichen Zyklus darf kein weiterer Lauf automatisch beginnen. Ein neuer unabhängiger Zyklus kann nur durch eine ausdrückliche Wahl gestartet werden.

## 4. Mechanischer Fortschritt

### COMPOSE

```text
image
-> scent
-> movement
-> wish_word
-> review
-> confirmation
-> local creation
```

Ein erfolgreicher COMPOSE-Zyklus erzeugt:

```text
einen neuen Resonance Token
+ eine neue travelling invitation
+ einen eigenen privaten Return Workspace
+ einen eigenen matching Return Slot
```

Beliebig viele unabhängige COMPOSE-Zyklen sind konzeptionell erlaubt.

### ANSWER

```text
image_response
-> scent_response
-> movement_response
-> return_word
-> review
-> confirmation
-> local creation
```

Ein ANSWER-Zyklus bezieht sich auf den aktuell ausgewählten Resonance Token und erzeugt ein Return Artifact für dessen Resonanzweg.

Ein weiterer ANSWER-Zyklus setzt einen anderen bewusst ausgewählten oder aktivierten Resonance Token voraus.

Für denselben individuellen Return Slot bleibt im Sprint zunächst die Semantik:

```text
ein passendes Return Artifact
-> ein stabiles lokales Ergebnis
-> später unverändert erneut betrachtbar
```

Mehrere Return Artifacts für unterschiedliche Slots und Resonanzzyklen bleiben vorgesehen.

## 5. Erkundungsfortschritt

```text
Raum ungesehen
Raum betrachtet
Spur entdeckt
Spur gelesen
Hilfe aufgerufen
Stimme angesprochen
Walkthrough aktiviert
```

Der Erkundungszustand bleibt zunächst transient und gehört der Chamber.

## 6. Ergebnisverfügbarkeit

```text
keine Ergebnisse
ein Ergebnis
mehrere Ergebnisse aus unterschiedlichen Resonanzzyklen
```

Ergebnisverfügbarkeit ist unabhängig davon, ob gerade ein produktiver Resonanzzyklus läuft.

---

# E. Ergebnisprinzip

## Die Resonance Chamber als lokaler Erinnerungsraum

Sie darf innerhalb des lokalen Nexus-Moduls anzeigen:

### Private lokale Ergebnisse

- die geöffnete persönliche First-Spark-Nachricht;
- die getragene Ursprungsresonanz;
- gewählte Resonance-Entscheidungen;
- Wunsch- und Rückkehrwort;
- Antwortbeitrag;
- Nachhall;
- Ergebnisse aus mehreren unabhängigen Resonanzzyklen.

### Öffentliche sichere Ergebnisse

- den unveränderten statischen Resonance-Node-Text;
- neutrale Abschluss- und Modulspuren;
- keine später persönlich ergänzten Alias- oder Notizfelder.

### Lokale Pfadreferenzen

- travelling invitation;
- Return Workspace;
- Return Artifact;
- bestehender Nachhall;
- weitere ausdrücklich gespeicherte Ergebnisorte.

Die Chamber darf bekannte Pfade prüfen, aber nicht selbstständig die Festplatte durchsuchen.

## Persistenzregel

> Statische Ergebnisse bleiben über Sitzungen hinweg erneut anzeigbar, solange ihre maßgebliche lokale Quelle und ihr genauer Zugriffspfad vorhanden sind.

Bestehende Artefakte sollen wieder gelesen werden. Es soll keine unnötige zweite Schattenkopie privater Inhalte entstehen.

Für den Sprint wird Persistenz gestuft umgesetzt:

```text
First Spark private message
+ static Resonance Node
-> sitzungsübergreifend aus vorhandenen Quellen

aktuelle Resonance-Auswahl
+ erzeugte Pfade
-> zunächst im aktuellen Prozess

bestehender Nachhall
-> nur über einen bereits bekannten validierten Resultatpfad
```

## Eigentumsregel

```text
Jede Chamber besitzt ihr vollständiges Ergebnis.

Die Resonance Chamber darf ausdrücklich zugängliche lokale Ergebnisse anzeigen.

Das Atrium kennt höchstens Verfügbarkeit und Meilensteine.

Das Archive erhält nur gesonderte archive-sichere Spuren.
```

---

# F. Sprintumfang

## MUSS in die Geschenkfassung

- [x] gemeinsames Status- und Ergebniskonzept dokumentieren;
- [x] technische Bestandsaufnahme ohne Änderungen;
- [ ] Resonance Chamber atmosphärisch betreten können;
- [ ] `look`;
- [ ] `help`;
- [ ] `trace`;
- [ ] Informationsbefehle verändern den aktuellen Resonance-Schritt nicht;
- [ ] vollständiger aktueller Prompt erscheint nach Informationsbefehlen erneut;
- [ ] leichte Einrückung der Chamber-Ausgabe;
- [ ] `walkthrough` mit Spoilerwarnung;
- [ ] Chamber-Stimme übernimmt beim Walkthrough die schrittweise Führung;
- [ ] bestehende COMPOSE- und ANSWER-Mechanik bleibt funktional unverändert;
- [ ] kein automatischer Neustart nach einem erfolgreichen Zyklus;
- [ ] ein neuer COMPOSE-Zyklus kann ausdrücklich begonnen werden;
- [ ] lokale und freiwillige Übergabe bleibt klar;
- [ ] alle relevanten Tests bestehen;
- [ ] manueller COMPOSE-Durchlauf;
- [ ] manueller zweiter unabhängiger COMPOSE-Zyklus;
- [ ] manueller ANSWER-Durchlauf;
- [ ] manueller Abbruch- und Recovery-Durchlauf.

## SOLLTE hinein

- [ ] Post-run-Zustand der Resonance Chamber;
- [ ] `results` erscheint, sobald Ergebnisse vorhanden sind;
- [ ] persönliche First-Spark-Nachricht in `results`;
- [ ] statischer First-Spark-Resonance-Node in `results`;
- [ ] Resonance-Entscheidungen in `results`;
- [ ] mehrere Resonanzzyklen unterscheidbar anzeigen;
- [ ] Nachhall in `results`;
- [ ] lokale Speicherpfade in `results`;
- [ ] bereits vorhandene statische Ergebnisse über Neustarts erneut lesbar.

## SPÄTER

- [ ] freier natürlichsprachlicher Dialog mit der Chamber;
- [ ] allgemeines Ergebnisregister für beliebig viele zukünftige Chambers;
- [ ] automatische Wiederentdeckung beliebiger verschobener Ergebnisdateien;
- [ ] mehrere Return Artifacts für denselben Return Slot;
- [ ] persistenter Erkundungsfortschritt;
- [ ] komplexe Gegenstände mit `inspect`;
- [ ] umfangreiche `read <trace-name>`-Struktur;
- [ ] Archivintegration;
- [ ] modulübergreifende Ergebnisansichten;
- [ ] grafische Oberfläche;
- [ ] langfristig veränderliche Chamber-Stimmen;
- [ ] dynamische Terminalbreiten und komplexes Text-Wrapping.

---

# G. Umsetzungsscheiben

## Scheibe 0 — Konzept einfrieren

**Status:** abgeschlossen.

- [x] Zustandsachsen;
- [x] Textebenen einschließlich Chamber-Stimme;
- [x] Zyklus- statt Verbrauchssemantik;
- [x] Ergebnisarten und Datenschutzgrenzen;
- [x] Persistenzregel;
- [x] Terminaldarstellung;
- [x] vertagte Funktionen.

## Scheibe 1 — Technische Bestandsaufnahme

**Status:** abgeschlossen.

Wesentliche Ergebnisse:

- `TerminalChamberIO` ist die kleinste gemeinsame Eingabenaht.
- Ein optionaler Informationsbefehl-Handler genügt.
- Der aktuelle mechanische Schritt wird bereits übergeben und muss nicht doppelt gespeichert werden.
- COMPOSE- und ANSWER-Flows können unangetastet bleiben.
- Resonance-only indentation ist sprinttauglich.
- `open_resonance_return_files()` ist kein allgemeiner read-only Viewer.
- Pfade aus COMPOSE und ANSWER werden derzeit nicht dauerhaft indexiert.
- Post-run und mehrere Zyklen müssen ausdrücklich statt automatisch behandelt werden.

## Scheibe 2A — Erkundungsnaht und Einrückung

**Ziel:** Die Resonance Chamber wird als Raum erfahrbar, ohne ihre Mechanik zu verändern.

Umfang:

- [ ] optionaler Informationsbefehl-Handler in `TerminalChamberIO`;
- [ ] `look`;
- [ ] `help`;
- [ ] `trace`;
- [ ] COMPOSE und ANSWER;
- [ ] vollständige Wiederholung des aktuellen unveränderten Prompts;
- [ ] keine Zustandsmutation;
- [ ] Resonance-only indentation;
- [ ] `/cancel` nur dort anzeigen, wo es unterstützt wird.

Noch nicht:

- aktiver Walkthrough;
- `results`;
- Post-run-Menü;
- BLOCKED-Dialog;
- allgemeine Legacy-Erweiterung.

**Definition of Done:**

- direkter Durchlauf funktioniert unverändert;
- Informationsbefehle werden nicht als falsche Zahl oder falsches Wort behandelt;
- frühere Auswahlen bleiben erhalten;
- keine späteren Optionen werden vorzeitig offengelegt;
- fokussierte Tests bestehen.

**Größe:** klein.

## Scheibe 2B — Geführter Walkthrough

- [ ] Spoilerwarnung;
- [ ] ausdrückliche Zustimmung;
- [ ] Chamber-Stimme;
- [ ] nur aktueller Schritt;
- [ ] Führung beendbar;
- [ ] keine automatische Auswahl;
- [ ] kein wiederholter Führungstext nach jeder ungültigen Eingabe.

**Größe:** klein.

## Scheibe 3 — Post-run, Revisit und neue Zyklen

**Ziel:** Ein abgeschlossener Zyklus führt in einen ruhigen Post-run-Zustand, nicht in eine verbrauchte Chamber.

- [ ] kein automatischer zweiter produktiver Lauf;
- [ ] vorhandene Resultate betrachtbar;
- [ ] neuer unabhängiger COMPOSE-Zyklus ausdrücklich startbar;
- [ ] ANSWER nur mit bewusst ausgewähltem gültigem Token-Kontext;
- [ ] Chamber bleibt betretbar;
- [ ] `look`;
- [ ] `help`;
- [ ] `trace`;
- [ ] `results`, falls vorhanden;
- [ ] `leave`.

**Definition of Done:**

```text
completed cycle
= produktiver Vorgang beendet
+ kein automatischer Neustart
+ Chamber weiterhin betretbar
+ Resultate betrachtbar
+ neuer unabhängiger Zyklus nur nach ausdrücklicher Wahl
```

**Größe:** klein bis mittel.

## Scheibe 4A — Same-process Results

- [ ] First-Spark-Nachricht, soweit bereits verfügbar;
- [ ] statischer Resonance Node;
- [ ] aktuelle Resonance-Auswahl;
- [ ] bekannte erzeugte Pfade;
- [ ] mehrere aktuelle Zyklusresultate unterscheidbar;
- [ ] keine Regeneration;
- [ ] kein Überschreiben;
- [ ] keine Veröffentlichung.

## Scheibe 4B — Persistente bestehende Quellen

Nur dort, wo bereits ein maßgeblicher Pfad vorhanden ist:

- [ ] private First-Spark-Nachricht;
- [ ] statischer Resonance Node;
- [ ] ausgewählter getragener Token;
- [ ] ausdrücklich bekannter bestehender Resultatpfad.

Keine allgemeine Registry im Geschenksprint.

## Scheibe 5 — Sprachliche Endredaktion

- [ ] Raumtexte;
- [ ] Trace-Texte;
- [ ] Chamber-Stimme;
- [ ] Help-Texte;
- [ ] Walkthrough-Führung;
- [ ] Post-run-Raumgestalt;
- [ ] Results-Menü;
- [ ] technische Meldungen;
- [ ] konsistente Einrückung und Zeilenlängen.

## Scheibe 6 — Tests und manuelle Spielprüfung

### Automatisch

- [ ] fokussierte Tests jeder Scheibe;
- [ ] Packaging-Tests;
- [ ] kanonischer Runner;
- [ ] `git diff --check`.

### Manuell durch Natali

#### Geschenkpfad

- [ ] First Spark abschließen;
- [ ] Resonance-Tür erscheint;
- [ ] COMPOSE direkt durchlaufen;
- [ ] COMPOSE mit `look`, `trace` und `help`;
- [ ] Walkthrough ausprobieren;
- [ ] Post-run-Zustand prüfen;
- [ ] zweiten unabhängigen COMPOSE-Zyklus ausdrücklich starten;
- [ ] Ergebnisse unterscheiden und erneut öffnen;
- [ ] Neustart und bereits persistente Quellen prüfen;
- [ ] Lesbarkeit und Einrückung prüfen.

#### Rückresonanz

- [ ] gültiger Token → ANSWER;
- [ ] ungültiger Kontext → BLOCKED;
- [ ] Abbruch in verschiedenen Phasen;
- [ ] Return Artifact anzeigen;
- [ ] lokales Ergebnis dem richtigen Resonanzweg zuordnen;
- [ ] lokale Pfade prüfen.

#### Post-run

- [ ] erneuter Eintritt startet nicht automatisch produktiv;
- [ ] `results`;
- [ ] ausdrücklich neuer Zyklus;
- [ ] `leave`;
- [ ] keine privaten Inhalte im öffentlichen Node.

## Scheibe 7 — Release-Freeze

- [ ] keine neuen Funktionen;
- [ ] nur noch Fehlerkorrekturen;
- [ ] finaler Diff-Review;
- [ ] geänderte Dateien klassifizieren;
- [ ] sinnvolle Commits vorbereiten;
- [ ] Push und PR erst nach ausdrücklicher Freigabe;
- [ ] README und Quick Start prüfen;
- [ ] Geschenkpaket erstellen;
- [ ] Paket aus Sicht der empfangenden Person testen.

---

# H. Abbruch- und Vereinfachungsregeln

## Erkundungsgrammatik wird vereinfacht, falls …

- der Handler unerwartet in die mechanischen Flows eingreifen müsste;
- die exakten Output-Tests unverhältnismäßig breit betroffen wären.

Dann beginnt der Sprint nur mit `look`, `help` und `trace` in COMPOSE und ANSWER.

## Chamber-Stimme wird vereinfacht, falls …

ein dauerhaft aktiver Walkthrough-Modus zu groß wird.

Dann zeigt `walkthrough` nur einen bestätigten, nicht-preskriptiven Hinweis für den aktuellen Schritt.

## Post-run wird vereinfacht, falls …

ein vollständiger Revisit-Controller zu riskant wird.

Dann verhindert das Atrium zunächst nur einen automatischen Neustart und bietet:

```text
results
compose another
leave
```

über eine schmale Resonance-eigene Post-run-Auswahl an.

## Ergebnisse werden vereinfacht, falls …

- ein allgemeines Result-Register nötig würde;
- neue Persistenzformate nötig würden;
- bestehende Sicherheitsgrenzen unklar werden.

Dann gilt:

```text
First Spark private message
+ static Resonance Node
+ current-process Resonance summary
+ remembered exact local paths
```

## Terminaldarstellung wird vereinfacht, falls …

die gemeinsame Formatierung zu viele Ausgaben berührt.

Dann wird nur die Resonance-Chamber-Ausgabe leicht eingerückt.

---

# I. Aktuelle Sprintreihenfolge

```text
1. Planungsdokumente versioniert in Git ablegen
2. Scheibe 2A: Erkundungsnaht und Einrückung
3. fokussierte Tests
4. Scheibe 2B: geführter Walkthrough
5. Post-run und ausdrücklich neue Zyklen
6. Same-process Results
7. persistente bestehende Quellen
8. sprachliche Endredaktion
9. manuelle Durchläufe
10. Release-Freeze
11. Push / PR
```

Nicht parallelisieren:

- Erkundungsgrammatik und Results-Persistenz;
- Produktionscode und große Textredaktion;
- technische Umsetzung und Branchpflege.

---

# J. Nächster konkreter Schritt

Die V0.1-Ausgangsfassungen werden zuerst in einem eigenen Dokumentationscommit festgehalten.

Danach werden sie per Git-Rename zu V0.2 weitergeführt und mit den Erkenntnissen aus der technischen Bestandsaufnahme sowie der wiederholbaren Resonanzzyklus-Semantik aktualisiert.

Anschließend beginnt Scheibe 2A.

---

## Gemeinsamer Sprintleitsatz

> Wir bauen nicht alles, was denkbar ist.  
> Wir bauen das Kleinste, das sich bereits wie ein vollständiger Nexus anfühlt.
