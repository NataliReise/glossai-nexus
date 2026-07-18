# Nexus 01 Sprintplan — Geschenkfassung

## Document status

- Version: 0.1
- Status: Baseline
- Date: 2026-07-18
- Purpose: Initial gift-release sprint plan before the Slice 1 technical inventory.

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
- erstellt keine Branches, Commits oder Pushes.

---

# A. Sprintregeln

## Git-Sicherheit

Während des Sprints:

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
kein Commit
kein Push
```

bis die aktuelle Gesamtänderung geprüft und ausdrücklich freigegeben wurde.

Vor der nächsten technischen Änderung:

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
- [x] Codex meldete für den damaligen Stand eine erfolgreiche kanonische Testsuite.
- [x] Keine Branch-, Commit- oder Push-Operation wurde im aktuellen Sprintstand vorgenommen.

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

Empfohlene Darstellungsregel:

```text
0 Leerzeichen   Überschriften, Eingabeprompts, wichtige Systemgrenzen
2 Leerzeichen   Raumtexte, Chamber-Stimme, Traces, Help-Einträge, Auswahlmöglichkeiten
4 Leerzeichen   Ergebnisdetails und lokale Dateipfade
```

Die Einrückung ist eine Darstellungsregel und soll nicht einzeln in die literarischen Texte eingebaut werden.

Für den Sprint genügt eine kleine zentrale Formatierungsfunktion. Dynamische Terminalbreiten und aufwendiger automatischer Zeilenumbruch werden vertagt.

---

# D. Zustandsmodell

Wir unterscheiden fünf unabhängige Ebenen.

## 1. Atriumstatus

```text
nicht sichtbar
offen
Recovery-Zugang
abgeschlossen und erneut betretbar
```

Das Atrium entscheidet nur, ob eine Tür sichtbar und betretbar ist.

## 2. Eintrittsgestalt

```text
COMPOSE
ANSWER
BLOCKED_ANSWER_RECOVERY
LEGACY_CONTROLLER
```

Der Eintrittspfad bestimmt die Grundgestalt der Resonance Chamber.

## 3. Mechanischer Fortschritt

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

## 4. Erkundungsfortschritt

```text
Raum ungesehen
Raum betrachtet
Spur entdeckt
Spur gelesen
Hilfe aufgerufen
Stimme angesprochen
Walkthrough aktiviert
```

## 5. Ergebnisverfügbarkeit

```text
keine Ergebnisse
ein Ergebnis
mehrere Ergebnisse
```

Ergebnisverfügbarkeit ist unabhängig davon, ob der aktuelle Resonance-Vorgang bereits abgeschlossen wurde.

---

# E. Ergebnisprinzip

## Die Resonance Chamber als lokaler Erinnerungsraum

Sie darf innerhalb des lokalen Nexus-Moduls anzeigen:

### Private lokale Ergebnisse

- die geöffnete persönliche First-Spark-Nachricht;
- gewählte Resonance-Entscheidungen;
- Wunsch- und Rückkehrwort;
- getragene Resonanz;
- Antwortbeitrag;
- Nachhall;
- erzeugte Dateien und ihre gewählten Speicherorte.

### Öffentliche sichere Ergebnisse

- den unveränderten statischen Resonance-Node-Text;
- neutrale Abschluss- und Modulspuren;
- keine später persönlich ergänzten Alias- oder Notizfelder.

### Lokale Pfadreferenzen

- Einladung;
- Return Workspace;
- Return Artifact;
- weitere ausdrücklich gespeicherte Ergebnisorte.

Die Chamber darf bekannte Pfade prüfen, aber nicht selbstständig die Festplatte durchsuchen.

## Persistenzregel

> Statische Ergebnisse bleiben über Sitzungen hinweg erneut anzeigbar, solange ihre maßgebliche lokale Quelle noch vorhanden ist.

Bestehende Artefakte sollen wieder gelesen werden. Es soll keine unnötige zweite Schattenkopie privater Inhalte entstehen.

## Eigentumsregel

```text
Jede Chamber besitzt ihr vollständiges Ergebnis.

Die Resonance Chamber darf ausdrücklich zugängliche lokale Ergebnisse anzeigen.

Das Atrium kennt höchstens Verfügbarkeit und Abschluss.

Das Archive erhält nur gesonderte archive-sichere Spuren.
```

---

# F. Sprintumfang

## MUSS in die Geschenkfassung

- [ ] gemeinsames Status- und Ergebniskonzept dokumentieren;
- [ ] Resonance Chamber atmosphärisch betreten können;
- [ ] `look`;
- [ ] `help`;
- [ ] `trace`;
- [ ] `walkthrough` mit Spoilerwarnung;
- [ ] Informationsbefehle verändern den aktuellen Resonance-Schritt nicht;
- [ ] Chamber-Stimme übernimmt beim Walkthrough die schrittweise Führung;
- [ ] bestehende COMPOSE- und ANSWER-Mechanik bleibt funktional unverändert;
- [ ] lokale und freiwillige Übergabe bleibt klar;
- [ ] leichte Einrückung der Chamber-Ausgabe;
- [ ] alle relevanten Tests bestehen;
- [ ] manueller COMPOSE-Durchlauf;
- [ ] manueller ANSWER-Durchlauf;
- [ ] manueller Abbruch- und Recovery-Durchlauf.

## SOLLTE hinein

- [ ] abgeschlossene Resonance Chamber erneut betretbar;
- [ ] kein zweiter produktiver Lauf nach Abschluss;
- [ ] `results` erscheint, sobald Ergebnisse vorhanden sind;
- [ ] persönliche First-Spark-Nachricht in `results`;
- [ ] statischer First-Spark-Resonance-Node in `results`;
- [ ] Resonance-Entscheidungen in `results`;
- [ ] Nachhall in `results`;
- [ ] lokale Speicherpfade in `results`;
- [ ] Ergebnisse über Neustarts erneut lesbar.

## SPÄTER

- [ ] freier natürlichsprachlicher Dialog mit der Chamber;
- [ ] allgemeines Ergebnisregister für beliebig viele zukünftige Chambers;
- [ ] persistenter Erkundungsfortschritt;
- [ ] komplexe Gegenstände mit `inspect`;
- [ ] umfangreiche `read <trace-name>`-Struktur;
- [ ] automatische Dateisuche;
- [ ] Archivintegration;
- [ ] modulübergreifende Ergebnisansichten;
- [ ] grafische Oberfläche;
- [ ] langfristig veränderliche Chamber-Stimmen;
- [ ] dynamische Terminalbreiten und komplexes Text-Wrapping.

---

# G. Umsetzungsscheiben

## Scheibe 0 — Konzept einfrieren

**Ziel:** Codex erhält eine eindeutige Grundlage.

- [ ] Konzeptdokument anlegen:  
  `NEXUS_01_CHAMBER_STATES_AND_RESULTS_V01.md`
- [ ] Zustandsachsen festhalten;
- [ ] Textebenen einschließlich Chamber-Stimme definieren;
- [ ] Bedeutung von `completed` definieren;
- [ ] Ergebnisarten und Datenschutzgrenzen definieren;
- [ ] Persistenzregel festhalten;
- [ ] Terminaldarstellung und Einrückung festhalten;
- [ ] ausdrücklich vertagte Funktionen nennen.

**Definition of Done:**

- eine einzige verständliche Quelle;
- keine Produktionsänderung;
- keine offenen Widersprüche zwischen Atrium, Chamber, Resultaten und Archiv.

**Timebox:** ungefähr 30–45 Minuten.

---

## Scheibe 1 — Technische Bestandsaufnahme

**Ziel:** Kleinsten sicheren Implementierungsweg finden.

Codex soll nur untersuchen:

- Wo können `look`, `help`, `trace` und `walkthrough` am kleinsten abgefangen werden?
- Wie kann ein Informationsbefehl zum unveränderten Prompt zurückkehren?
- Wo lässt sich eine kleine zentrale Einrückungsfunktion ergänzen?
- Welche Ausgaben sollten eingerückt bleiben und welche linksbündig?
- Welche exakten Output-Tests würden dadurch berührt?
- Welche bestehenden Quellen enthalten:
  - private First-Spark-Nachricht,
  - statischen Resonance-Node-Text,
  - Resonance-Auswahl,
  - Nachhall,
  - erzeugte Pfade?
- Welche Ergebnisse sind schon persistent?
- Welche minimale Erweiterung ist für wiederholtes Anzeigen nötig?
- Welche Tests schützen die bestehenden Abschlussbedingungen?

**Keine Änderungen.**

**Definition of Done:**

- genaue Dateien und Funktionen;
- kleinster Eingriff;
- Risiken;
- empfohlene Reihenfolge;
- keine spekulative Großarchitektur.

**Timebox:** ungefähr 30–45 Minuten.

---

## Scheibe 2 — Erkundungsgrammatik

**Ziel:** Die Resonance Chamber wird als Raum erfahrbar.

Umfang:

- [ ] `look`
- [ ] `help`
- [ ] `trace`
- [ ] `walkthrough`
- [ ] Spoilerbestätigung;
- [ ] zustandsabhängige Texte;
- [ ] Rückkehr zum selben Prompt;
- [ ] keine Zustandsmutation durch Informationsbefehle;
- [ ] `/cancel` nur dort anzeigen, wo es tatsächlich unterstützt wird;
- [ ] leichte zentrale Einrückung der Chamber-Ausgaben;
- [ ] Prompts und wichtige Systemgrenzen bleiben klar erkennbar.

Chamber-Stimme:

- [ ] übernimmt nach bestätigtem Walkthrough die Führung;
- [ ] nennt nur den nächsten Schritt;
- [ ] trifft keine Auswahl;
- [ ] überspringt keinen Zustand;
- [ ] kann wieder verlassen werden.

**Definition of Done:**

- direkter Durchlauf ohne Hilfen funktioniert weiterhin;
- erkundender Durchlauf funktioniert;
- Walkthrough führt, automatisiert aber nichts;
- Terminaltexte sind besser lesbar;
- fokussierte Tests bestehen.

**Timebox:** ungefähr 90–120 Minuten.

---

## Scheibe 3 — Abschluss und Revisit

**Ziel:** `completed` verändert die Chamber, schließt sie aber nicht aus der Erfahrung aus.

- [ ] abgeschlossene Chamber bleibt sichtbar;
- [ ] erneuter Eintritt startet keinen zweiten produktiven Vorgang;
- [ ] eigene abgeschlossene Raumgestalt;
- [ ] `look`;
- [ ] `help`;
- [ ] `trace`;
- [ ] `results`, falls Ergebnisse vorhanden;
- [ ] `leave`.

**Definition of Done:**

```text
completed
= produktiver Vorgang beendet
+ Chamber weiterhin betretbar
+ keine zweite Erzeugung
```

**Timebox:** ungefähr 45–75 Minuten.

---

## Scheibe 4 — Ergebnisse

**Ziel:** Vorhandene Ergebnisse komfortabel und wiederholt anzeigen.

### First Spark

- [ ] private geöffnete Nachricht;
- [ ] statischer Resonance-Node-Text;
- [ ] keine persönlich ergänzten Node-Inhalte.

### Resonance COMPOSE

- [ ] Image;
- [ ] Scent;
- [ ] Movement;
- [ ] Wish word;
- [ ] Nachhall, sobald vorhanden;
- [ ] Einladungspfad;
- [ ] privater Workspace-Pfad.

### Resonance ANSWER

- [ ] getragene Resonanz;
- [ ] drei Antworten;
- [ ] Return word;
- [ ] Nachhall;
- [ ] Return-Artifact-Pfad.

### Darstellung

```text
results
-> verfügbare Ergebnisgruppen
-> Auswahl
-> Kennzeichnung:
   [private local]
   [public-safe]
   [local path]
```

**Definition of Done:**

- keine automatische Veröffentlichung;
- keine Dateisuche;
- keine Regeneration;
- kein Überschreiben;
- maßgebliche lokale Quellen werden gelesen;
- fehlende Quelle führt zu ruhiger, verständlicher Meldung.

**Timebox:** ungefähr 60–120 Minuten, abhängig von der Bestandsaufnahme.

---

## Scheibe 5 — Sprachliche Endredaktion

Erst nach funktionaler Umsetzung:

- [ ] Raumtexte;
- [ ] Trace-Texte;
- [ ] Chamber-Stimme;
- [ ] Help-Texte;
- [ ] Walkthrough-Führung;
- [ ] abgeschlossene Raumgestalt;
- [ ] Results-Menü;
- [ ] technische Meldungen;
- [ ] konsistente Einrückung und Zeilenlängen.

Prüffragen:

- Erklärt der Raum zu viel?
- Ist `help` eindeutig?
- Ist `trace` wirklich andeutend?
- Klingt die Stimme lokal und begrenzt?
- Ist der Walkthrough hilfreich, ohne selbst zu handeln?
- Ist Privates klar als privat-lokal markiert?
- Sind Pfade für wenig technikaffine Menschen verständlich?
- Ist die visuelle Hierarchie im Terminal ruhig und konsistent?

**Timebox:** ungefähr 45–60 Minuten.

---

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
- [ ] Ergebnisse erneut öffnen;
- [ ] Neustart und persistente Ergebnisse prüfen;
- [ ] Lesbarkeit und Einrückung prüfen.

#### Rückresonanz

- [ ] gültiger Token → ANSWER;
- [ ] ungültiger Kontext → BLOCKED;
- [ ] Abbruch in verschiedenen Phasen;
- [ ] Return Artifact anzeigen;
- [ ] lokale Pfade prüfen.

#### Abschluss

- [ ] erneut in completed Chamber eintreten;
- [ ] kein zweiter produktiver Lauf;
- [ ] `results`;
- [ ] `leave`;
- [ ] keine privaten Inhalte im öffentlichen Node.

**Definition of Done:**

- keine unerklärlichen Sackgassen;
- keine falschen Abschlussmarkierungen;
- keine automatische Übertragung;
- keine Dopplung oder Überschreibung;
- wichtige Informationen auch ohne Dateimanager auffindbar;
- Terminaldarstellung gut lesbar.

---

## Scheibe 7 — Release-Freeze

Nach erfolgreicher Spielprüfung:

- [ ] keine neuen Funktionen;
- [ ] nur noch Fehlerkorrekturen;
- [ ] finaler Diff-Review;
- [ ] geänderte Dateien klassifizieren;
- [ ] zwei sinnvolle Commits vorbereiten;
- [ ] Push und PR erst nach ausdrücklicher Freigabe;
- [ ] README und Quick Start prüfen;
- [ ] Geschenkpaket erstellen;
- [ ] Paket aus Sicht der empfangenden Person testen.

---

# H. Abbruch- und Vereinfachungsregeln

Der Sprint braucht eine eingebaute Notbremse.

## Ergebnisse werden vereinfacht, falls …

- ein allgemeines Result-Register viele Produktionsdateien verändern würde;
- neue Persistenzformate nötig würden;
- First Spark dafür stark umgebaut werden müsste;
- bestehende Sicherheitsgrenzen unklar werden;
- die kanonische Suite instabil wird.

Dann gilt für die Geschenkfassung:

```text
First Spark message
+ static resonance node
+ current Resonance result
+ remembered local paths
```

ohne allgemeine zukünftige Registry.

## Chamber-Stimme wird vereinfacht, falls …

ein Dialogsystem zu groß wird. Dann:

```text
walkthrough
-> bestätigte schrittweise Chamber-Führung
```

ohne freien `ask`-Befehl.

## Revisit wird vereinfacht, falls …

die Runtime-Änderung zu riskant wird. Dann erscheint nach Abschluss zunächst ein eigener Ergebnisbefehl im Atrium oder unmittelbar vor der Rückkehr. Die vollständige erneut betretbare Chamber folgt später.

## Terminaldarstellung wird vereinfacht, falls …

eine allgemeine Textformatierung zu viele Ausgaben oder Tests berührt. Dann wird im Sprint nur die Resonance-Chamber-Ausgabe leicht eingerückt; dynamische Breiten, automatisches Wrapping und eine modulweite Formatierungsarchitektur folgen später.

---

# I. Sprintreihenfolge

Die Reihenfolge bleibt strikt:

```text
1. Konzeptdokument
2. Codex-Bestandsaufnahme ohne Änderungen
3. Erkundungsgrammatik
4. Tests
5. Revisit
6. Results
7. sprachliche Endredaktion
8. manuelle Durchläufe
9. Release-Freeze
10. Commit / Push / PR
```

Nicht parallelisieren:

- Erkundungsgrammatik und Results-Persistenz;
- Produktionscode und große Textredaktion;
- technische Umsetzung und Branchpflege.

---

# J. Nächster konkreter Schritt

Als Nächstes entsteht Scheibe 0:

```text
modules/nexus_01_nexus_mesomerie/
NEXUS_01_CHAMBER_STATES_AND_RESULTS_V01.md
```

Darin werden nur die bereits getroffenen Entscheidungen gebündelt:

- Zustandsachsen;
- Textebenen;
- Chamber-Stimme;
- Bedeutung von `completed`;
- Ergebnisarten;
- Datenschutzgrenzen;
- Persistenzregel;
- Terminaldarstellung;
- ausdrücklich vertagte Funktionen.

Danach folgt ein reiner Codex-Untersuchungsauftrag für Scheibe 1.

---

## Gemeinsamer Sprintleitsatz

> Wir bauen nicht alles, was denkbar ist.  
> Wir bauen das Kleinste, das sich bereits wie ein vollständiger Nexus anfühlt.