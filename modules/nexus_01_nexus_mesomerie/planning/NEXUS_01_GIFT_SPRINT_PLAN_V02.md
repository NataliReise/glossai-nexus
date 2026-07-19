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
- [x] Slice 4A ist korrekt und bleibt bestehen: `/results` zeigt das jüngste erfolgreiche COMPOSE- oder ANSWER-Ergebnis derselben Prozess-/Controller-Sitzung.
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

Das Return Artifact ist zunächst ein Transportobjekt, nicht bereits das stabile
lokale Ergebnis. Dieses entsteht erst durch ein späteres erfolgreiches,
absichtliches Return Opening gegen den strukturell passenden Return Slot.

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

Die drei Ergebnisstufen bleiben getrennt:

```text
1. COMPOSE
   -> originating contribution
   -> travelling invitation
   -> private Return Workspace

2. ANSWER
   -> answer contribution
   -> Return Artifact

3. RETURN OPENING
   -> returned Return Artifact
   + matching Return Slot
   -> stable local Resonance result
```

Das durch ANSWER erzeugte Return Artifact ist zunächst ein Transportobjekt. Das
stabile lokale Ergebnis existiert erst nach erfolgreichem absichtlichem Return
Opening gegen den passenden Return Slot. Die abgeschlossene read-only Inventur
bestätigt für den Geschenk-Sprint genau eine autoritative stabile Markdown-Datei
mit dem kompakten Nachhall als vollständiger sichtbarer Ergebnisform. Ihr
technischer Trace und unklassifizierte manuelle Ergänzungen sind nicht
player-facing. Separate Produktionsdateien für Resonance Artifact oder Nexus
Echo werden nicht eingeführt.

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

**Status:** implementiert, geprüft, getestet und manuell akzeptiert. Slice 4A ist
korrekt und bleibt bestehen.

- [x] jüngstes erfolgreiches COMPOSE- oder ANSWER-Ergebnis der aktuellen
  Prozess-/Controller-Sitzung;
- [x] Resonance-only, process-local und view-only;
- [x] bekannte erzeugte Pfade ohne Dateisystemsuche;
- [x] keine Registry, Regeneration, Opening, Mutation, Übertragung oder
  Veröffentlichung durch `/results`.

## Scheibe 4B — Persistente bestehende Quellen

**Status:** Inventur abgeschlossen, Entscheidungen getroffen und Planung
aktualisiert; nicht implementiert und nicht zur Umsetzung freigegeben.

Die Inventur fand mehrere quellspezifische read-only Loader, aber keine bereits
bestehende generische Known-source-Ladegrenze. Scheibe 4B bleibt auf bewusst
bekannte autoritative Quellen nach Prozessneustart begrenzt und vollständig
read-only:

- [ ] private First-Spark-Nachricht;
- [ ] statischer Resonance Node;
- [ ] ausgewählter getragener Token;
- [ ] ausdrücklich bekannter bestehender Resultatpfad;
- [ ] keine allgemeine Registry oder Dateisystemsuche;
- [ ] kein Return Opening, Matching, Generieren oder Mutieren;
- [ ] keine automatische Discovery oder Auswahl einer unbekannten Quelle.

Die wichtigste noch offene Architekturfrage lautet:

```text
Wie gelangt der exakte autoritative stabile Resultatpfad
nach einem Prozessneustart bewusst zur Resonance Chamber?
```

Während des bestehenden Openings liegt dieser Pfad als
`LocalResonanceResult.path` vor und wird von der CLI ausgegeben. Er kann außerdem
aus einem bewusst bekannten privaten Return Workspace und `slot.result_file`
bestimmt werden. Die Resonance Chamber erhält oder persistiert ihn derzeit nicht.
Eine Registry, automatische Suche, Ergebnisdatenbank, Schattenkopie oder zweite
Persistenzschicht bleibt ausgeschlossen.

Der nächste separate read-only Schritt untersucht deshalb die kleinste bereits
vorhandene Übergabenaht: Konstruktion und Eintritt der Resonance Chamber nach
Neustart, explizite Pfadparameter, Launcher- oder Aktivierungskontext, bestehende
Controller-Eingaben, bewusst bekannte Workspace-Pfade sowie paketrelative oder
lokale Source-Übergaben. Eine spätere Lösung muss bewusst, lokal, explizit, ohne
Registry, ohne Discovery, ohne zweite Persistenzschicht und ohne Kopplung an
Opening arbeiten.

## Scheibe 5 — Rückkehr, lokaler Abschluss und spätere Ergebnisanzeige

**Status:** nur geplant, nicht implementiert und nicht zur Umsetzung freigegeben.

### 5A — Return Opening

**Ziel:** Das manuell zurückgebrachte Return Artifact wird absichtlich gegen den
wartenden passenden Return Slot geöffnet und erzeugt genau ein stabiles lokales
Resonance-Ergebnis.

**Status:** Inventur abgeschlossen und Entscheidung getroffen; operative
technische Infrastruktur vorhanden, aber die integrierte, gehärtete und manuell
akzeptierte Spielscheibe ist nicht implementiert und nicht zur Umsetzung
freigegeben.

Das gegenwärtige operative Return Opening wird von
`open_resonance_return.py` und der zentralen Funktion
`open_resonance_return_files()` getragen. Der bestehende Produktionspfad erzeugt
atomar und ohne Überschreiben genau eine stabile Markdown-Datei unter:

```text
<private Return Workspace>/results/<ReturnSlot.result_file>
```

Diese vorhandene Markdown-Datei mit dem kompakten Nachhall ist für den
Geschenk-Sprint das autoritative stabile lokale Produktionsresultat. Sie enthält
den sichtbaren kompakten Nachhall, einen eingebetteten technischen Trace und
möglicherweise spätere manuelle Ergänzungen. Im aktuellen Produktionspfad ist
der kompakte Nachhall nicht nur eine optionale spätere Komponente, sondern die
vollständige sichtbare stabile Ergebnisform. Für den Geschenk-Sprint werden
keine neuen separaten Produktionsdateien für Resonance Artifact oder Nexus Echo
eingeführt; vorhandene entsprechende Renderer und Begriffe gehören zum
Legacy-Bestand.

Die bewusste Return-Handlung ist entschieden:

```text
Artifact bewusst nach incoming/ kopieren
-> OPEN_RETURN.sh ausdrücklich starten
-> bei genau einem Artifact dieses verwenden
-> bei mehreren Artifacts jede automatische Auswahl verweigern
```

Das ist hinreichend bewusst, weil das Artifact manuell in den privaten Return
Workspace gebracht und das Opening danach ausdrücklich gestartet wird. Es gibt
nur eine begrenzte Ermittlung innerhalb des ausdrücklich bekannten
`incoming/`-Verzeichnisses, automatische Verwendung nur bei genau einem bewusst
dort abgelegten Kandidaten, keine Auswahl bei Mehrdeutigkeit und keine allgemeine
Discovery. Null Kandidaten werden abgelehnt; mehrere werden aufgelistet, aber
nicht automatisch ausgewählt. Für genau einen bewusst abgelegten Kandidaten ist
kein zusätzlicher Auswahlprompt erforderlich.

- [ ] Return Artifact ausschließlich manuell zurückbringen;
- [ ] Artifact bewusst in `incoming/` des bekannten privaten Return Workspace
  ablegen und `OPEN_RETURN.sh` ausdrücklich starten;
- [ ] keine allgemeine Dateisystemsuche, Kandidatenauswahl, Übertragung,
  Synchronisierung, Cloud-Publikation oder Rückkehr;
- [ ] strukturelle Zusammengehörigkeit von Return Artifact und Return Slot
  prüfen;
- [ ] fremde, beschädigte, unvollständige, inkompatible, veraltete oder
  mehrdeutige Artifacts sicher ablehnen;
- [ ] bei mehreren Kandidaten niemals automatisch auswählen;
- [ ] bei fehlgeschlagener Validierung oder Zuordnung nichts schreiben;
- [ ] beim ersten erfolgreichen Validieren und Opening genau ein stabiles
  lokales Ergebnis erzeugen;
- [ ] spätere Openings zeigen dasselbe gespeicherte Ergebnis unverändert;
- [ ] bestehende Ergebnisse niemals regenerieren, ersetzen oder überschreiben;
- [ ] Recovery-, Missing-, Mismatch- und Ambiguity-Meldungen ruhig und
  handlungsorientiert formulieren;
- [ ] Opening bleibt eine ausdrückliche Spielerhandlung und wird niemals durch
  `/results` ausgelöst.

Priorisierter 5A-Härtungsbefund: Doppelte identische Return-Slot-Identitäten
werden im allgemeinen Produktionspfad möglicherweise erst nach der
Ergebnisdateierzeugung beim Slot-Update eindeutig abgelehnt. Dadurch kann der
partielle Zustand `Ergebnisdatei existiert -> Slot-Update scheitert wegen
Mehrdeutigkeit` entstehen. Die Eindeutigkeit der maßgeblichen Slot-Identität muss
vor jeder Generierung oder Dateierzeugung vollständig geprüft werden. Diese
Härtung ist nicht implementiert, nicht freigegeben, muss vor oder innerhalb der
5A-Integration separat umgesetzt und getestet werden und darf nicht mit 5B
vermischt werden.

Die vorhandenen Produktionsgrenzen bleiben verbindlich: bestehende Ergebnisse
werden unverändert gelesen; ein geöffneter Slot ohne Ergebnis wird hart und ohne
Regeneration abgelehnt; atomare Erzeugung überschreibt nichts; Symlinks und
unsichere Ziele werden abgelehnt; manuelle Ergänzungen bleiben erhalten; nach
einem fehlgeschlagenen Slot-Update kann das vorhandene Ergebnis später ohne
Regeneration zur Slot-Reparatur dienen. 5A soll diese Infrastruktur verwenden
und nicht durch eine parallele Opening-Architektur ersetzen.

**Definition of Done:**

```text
COMPOSE
-> travelling invitation + private Return Workspace
-> ANSWER
-> Return Artifact
-> manual return
-> deliberate validation against the matching Return Slot
-> exactly one stable local result
-> unchanged reopening of the same stored result
```

### 5B — Local Result Revisit

**Ziel:** Nach erfolgreichem Return Opening kann das bereits erzeugte stabile
lokale Ergebnis durch die Resonance Chamber erneut read-only angezeigt werden.

**Status:** Inventur abgeschlossen und Architekturlage entschieden; nicht
implementiert und nicht zur Umsetzung freigegeben.

Der bestehende öffentliche Opening-Orchestrator ist kein zulässiger Reader für
`/results`. Er kann je nach Zustand Ergebnisse erzeugen, Return Artifact und
Return Slot matchen, den Generator aufrufen, den Slotstatus verändern oder
Recovery und Slot-Reparatur ausführen. Der einzige bestehende reine Dateireader
ist derzeit ein privater Helfer innerhalb dieses mutierenden Opening-Pfads.

Damit gilt Option C:

```text
Vor einer Slice-5B-Integration ist eine schmale Trennung
zwischen „bestehendes Ergebnis lesen“ und „Return öffnen“ erforderlich.
```

5B darf später nur die bereits bestehende autoritative Markdown-Datei über einen
explizit bekannten Pfad read-only lesen. Es darf Opening-Orchestrierung,
Return-Artifact-Parsing als Voraussetzung für Revisit, Slot-Matching, Generator,
Slot-Update, Regeneration, Reparatur, Kandidatensuche oder Kandidatenauswahl weder
importieren noch aufrufen.

Die erste verbindliche Rendering-Allowlist lautet:

```text
[private local]
gespeicherter kompakter Nachhall

[local path]
exakter bewusst bekannter Resultatpfad
Verfügbarkeit dieses Pfades
```

Die ganze Markdown-Datei darf niemals ungefiltert dargestellt werden. Nicht
player-facing sind technischer Trace, `artifact_identity`, `slot_identity`,
Route-, Package-, Slot- und Origin-IDs, deterministischer Seed und
Seed-Ableitung, Composition Plan, Generatorinternas, Profil- oder Source-IDs,
Slotstatus, Slotnotizen, generische Objektrepräsentationen und unklassifizierte
manuelle Anhänge.

Manuelle Notizen bleiben eine interessante mögliche spätere persönliche
Erweiterung, gehören aber nicht zur ersten 5B-Allowlist. Vor einer eigenen
Datenschutz-, Format- und Spielerlebnisentscheidung werden sie weder automatisch
erkannt noch automatisch dargestellt.

`/results` darf niemals:

- ein Return Artifact öffnen;
- einen Return Slot validieren oder verändern;
- Resonance Artifact oder Nexus Echo erzeugen;
- Nachhall erzeugen oder regenerieren;
- ein stabiles lokales Ergebnis erzeugen, ersetzen oder überschreiben;
- nach Workspaces oder Ergebnisdateien suchen;
- zwischen mehreren Kandidaten auswählen;
- Opening-Code direkt oder indirekt aufrufen.

Die Reihenfolge ist zwingend:

```text
Return Artifact deliberately opened
-> stable local result already exists

then:

/results
-> read and display that existing stable result
```

Spielerperspektiven bleiben getrennt:

- **antwortende Person:** sieht den abgeschlossenen Antwortbeitrag und den Pfad
  des erzeugten Return Artifact;
- **ursprünglich wartende Person:** sieht nach manueller Rückkehr und
  erfolgreichem Opening allowlist-basiert den gespeicherten kompakten Nachhall,
  den bekannten lokalen Ergebnisort und dessen Verfügbarkeit.

Beide Perspektiven werden nicht ohne spätere Designentscheidung in ein
generisches Ergebnisobjekt zusammengeführt.

Scheibe 5B wendet die sichere Known-source-Grenze aus 4B auf das besondere, von
5A erzeugte stabile lokale Ergebnis an oder erweitert sie begründet. Sie schafft
keine zweite unabhängige Persistenz- oder Ladearchitektur, bleibt read-only und
ruft niemals 5A-Opening auf. Damit ist sie weder identisch mit 4B noch bereits
implementiert.

**Definition of Done:**

```text
successful Return Opening
-> stable local result already stored
-> deliberate known source available
-> read-only revisit through /results
-> no Opening, generation, regeneration, search, or mutation
```

### Inventurergebnis und nächste Planungsreihenfolge

Die Inventurbefunde und Entscheidungen sind dokumentiert. Die nächste
vorsichtige Arbeitsreihenfolge ist:

```text
1. separate read-only Inventur der bewussten Pfadübergabe
2. kleinste Known-source-Lesegrenze bestimmen
3. 5A-Härtung: doppelte Slot-Identitäten vor jedem Schreiben ablehnen
4. bestehendes Opening als bewussten Spielschritt integrieren
5. reinen Stable-result-Reader schaffen
6. 5B allowlist-basiert an /results anbinden
7. Recovery- und Ergebnistexte sprachlich bearbeiten
```

Dies ist eine Planungsreihenfolge und keine Implementierungsfreigabe. Slice 4A
bleibt abgeschlossen und unverändert. Slice 4B, 5A und 5B bleiben nicht
implementiert und nicht zur Umsetzung freigegeben. Unmittelbar nächster
technischer Schritt ist die separate read-only Inventur der bewussten
Pfadübergabe.

### Ausgeschlossen aus Scheibe 5

- allgemeine Ergebnis-Registry;
- allgemeine Dateisystemsuche oder automatische Auswahl bei mehreren
  Artifacts;
- Cloud-Synchronisierung oder Archivintegration;
- automatische Rückkehr, Publikation oder Opening;
- erneute ANSWER-Erzeugung;
- Regeneration von Resonance Artifact, Nexus Echo oder Nachhall;
- Überschreiben gespeicherter Ergebnisse;
- neue Persistenzarchitektur ohne vorherige read-only Inventur.

Ältere Dokumente und Legacy-Module beschreiben Resonance Artifact und Nexus Echo
teilweise noch als Ergebnisform. Der aktuelle Produktionscode und die aktuelle
Richtung verwenden den kompakten Nachhall als vollständiges stabiles Ergebnis.
Diese Begriffe werden in einer späteren Dokumentationsbereinigung synchronisiert;
historische Dokumente bleiben in dieser Aktualisierung unverändert.

## Scheibe 6 — Sprachliche Endredaktion

- [ ] Raumtexte;
- [ ] Trace-Texte;
- [ ] Chamber-Stimme;
- [ ] Help-Texte;
- [ ] Walkthrough-Führung;
- [ ] Post-run-Raumgestalt;
- [ ] Results-Menü;
- [ ] technische Meldungen;
- [ ] Return-Opening-Prompts und Bestätigungen;
- [ ] Recovery- und Missing-Artifact-Meldungen;
- [ ] Mismatch-, beschädigte- und unvollständige-Artifact-Meldungen;
- [ ] Ambiguity- und Multiple-candidate-Meldungen;
- [ ] Texte für die erneute Anzeige stabiler Ergebnisse;
- [ ] klare sprachliche Trennung zwischen Opening und `/results`;
- [ ] konsistente Einrückung und Zeilenlängen.

## Scheibe 7 — Tests und manuelle Spielprüfung

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
- [ ] Return Artifact manuell in den privaten Return Workspace zurückbringen;
- [ ] bewusst in `incoming/` des bekannten privaten Return Workspace ablegen
  und `OPEN_RETURN.sh` ausdrücklich starten;
- [ ] gegen den richtigen Return Slot öffnen;
- [ ] fremde Artifacts sicher ablehnen;
- [ ] beschädigte, unvollständige, inkompatible oder mehrdeutige Artifacts sicher ablehnen;
- [ ] unter mehreren Artifacts niemals automatisch auswählen;
- [ ] genau ein stabiles lokales Ergebnis erzeugen;
- [ ] dasselbe gespeicherte Ergebnis unverändert erneut öffnen;
- [ ] sicherstellen, dass nichts regeneriert oder überschrieben wird;
- [ ] lokale Pfade prüfen.

#### Post-run

- [ ] erneuter Eintritt startet nicht automatisch produktiv;
- [ ] `results`;
- [ ] gespeichertes lokales Ergebnis durch `/results` erneut anzeigen;
- [ ] bestätigen, dass `/results` weder Opening auslöst noch das Dateisystem durchsucht;
- [ ] ausdrücklich neuer Zyklus;
- [ ] `leave`;
- [ ] keine privaten Inhalte im öffentlichen Node.

#### Vollständiger Bogen

- [ ] `COMPOSE -> ANSWER -> RETURN OPENING -> RESULT REVISIT` manuell vollständig durchspielen.

## Scheibe 8 — Release-Freeze

- [ ] keine neuen Funktionen;
- [ ] nur noch Fehlerkorrekturen;
- [ ] finaler Diff-Review;
- [ ] geänderte Dateien klassifizieren;
- [ ] sinnvolle Commits vorbereiten;
- [ ] Push und PR erst nach ausdrücklicher Freigabe;
- [ ] README und Quick Start prüfen;
- [ ] Geschenkpaket erstellen;
- [ ] Return-Recovery-Anweisungen prüfen;
- [ ] privaten Return Workspace aus Sicht der ursprünglich wartenden Person prüfen;
- [ ] `COMPOSE -> ANSWER -> RETURN OPENING -> RESULT REVISIT` mit den Release-Paketen prüfen;
- [ ] stabile wiederholte Openings sowie No-regeneration und No-overwrite prüfen;
- [ ] unbeabsichtigte Dateisystemsuche ausschließen;
- [ ] Antwortenden- und Wartenden-Ergebnisansichten klar unterscheiden;
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

# I. Gesamte Sprintreihenfolge

Die Liste zeigt den Gesamtverlauf einschließlich bereits abgeschlossener
Schritte. Der aktuell nächste konkrete Schritt steht in Abschnitt J.

```text
1. Planungsdokumente versioniert in Git ablegen
2. Scheibe 2A: Erkundungsnaht und Einrückung
3. fokussierte Tests
4. Scheibe 2B: geführter Walkthrough
5. Post-run und ausdrücklich neue Zyklen
6. Same-process Results
7. persistente bestehende Quellen
8. Return Opening und stabile lokale Ergebniserzeugung
9. read-only Revisit des stabilen lokalen Ergebnisses
10. sprachliche Endredaktion
11. manuelle Durchläufe
12. Release-Freeze
13. Push / PR
```

Nicht parallelisieren:

- Erkundungsgrammatik und Results-Persistenz;
- Produktionscode und große Textredaktion;
- technische Umsetzung und Branchpflege.

---

# J. Nächster konkreter Schritt

Als Nächstes wird in einer separaten read-only Inventur die kleinste vorhandene
Übergabenaht untersucht, über die ein bewusst bekannter autoritativer stabiler
Resultatpfad nach einem Prozessneustart zur Resonance Chamber gelangen kann.

Diese Inventur untersucht insbesondere Chamber-Konstruktion und -Eintritt,
bestehende Controller-Eingaben, explizite Pfadparameter, Launcher- oder
Aktivierungskontext, bewusst bekannte Workspace-Pfade sowie paketrelative oder
lokale Source-Übergaben.

Sie führt keine Implementierung aus und nimmt keine Registry, Discovery, zweite
Persistenzschicht oder Kopplung an Return Opening vorweg. Slice 4B, 5A und 5B
bleiben nicht implementiert und nicht zur Umsetzung freigegeben.

---

## Gemeinsamer Sprintleitsatz

> Wir bauen nicht alles, was denkbar ist.  
> Wir bauen das Kleinste, das sich bereits wie ein vollständiger Nexus anfühlt.
