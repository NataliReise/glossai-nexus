# Nexus 01 Sprintplan — Geschenkfassung V0.3

## Dokumentstatus

- Version: 0.3
- Status: Current
- Datum: 2026-07-19
- Ersetzt: Version 0.2
- Zweck: Abschlussplan nach Fertigstellung der großen technischen Slices.

## A. Ausgangspunkt

- Branch: `gift/nexus-01-chamber-archive`
- Technischer Checkpoint: `59c6595`
- Commit: `feat(nexus-01): read stable local resonance results`
- Upstream: `origin/gift/nexus-01-chamber-archive`
- Checkpoint committed und pushed
- Letzte bestätigte Ausrichtung zu `origin/main`: 17 Commits voraus, 0 zurück
- Letzte kanonische Suite: 43 Testdateien, 408 Tests, 0 Failures, 0 Errors,
  0 Skips

Die großen technischen Slices sind bis einschließlich Stable-result Revisit
abgeschlossen. Offen sind die sprachliche Inventur und Endredaktion, die
kontrollierte vollständige Spielabnahme sowie der Release Freeze.

## B. Verbindliche Abschlussgrenzen

Für den Releaseabschluss gilt:

- keine neue Architektur und kein allgemeines Command- oder Result-Framework;
- keine Workspace-, Downloads-, Token-, Artifact- oder Ergebnis-Discovery;
- keine Registry, automatische Kandidatenauswahl oder Dateinamensvermutung;
- Return Opening und `/results` bleiben strikt getrennt;
- Same-process-Resultate und Stable-source-Resultate bleiben getrennte Modelle;
- keine automatische Übertragung, Regeneration, Reparatur oder Überschreibung;
- keine privaten Pfade oder Inhalte im travelling carrier;
- nur ausdrücklich autorisierte, belegte Abschlusskorrekturen.

## C. Abgeschlossene technische Slices

- **4A — Same-process Results:** Das jüngste erfolgreiche COMPOSE- oder
  ANSWER-Ergebnis derselben Controller-Sitzung ist allowlist-basiert sichtbar.
- **4B.0a — Neutral Resonance Entry:** Der Eintritt öffnet zuerst die ruhige
  `resonance>`-Surface; `/compose` oder `/answer` startet produktive Arbeit.
- **4B.0b — Description, Help and Capabilities:** Pre- und Post-run verwenden
  eine kleine Resonance-lokale Capability-Quelle für Help und Dispatch.
- **4B.0c — BLOCKED Surface:** ausschließlich `/look`, `/help`, `/quit`, ohne
  produktive Arbeit, Suche, Repair oder Resultatlektüre.
- **4B.1 — Explicit Known-source Handoff:** Ein absichtlich angegebener
  absoluter Pfad gelangt process-lokal bis zum Controller.
- **4B.2 — Safe Known-source Boundary:** no-follow, descriptor-basiertes,
  größenbegrenztes read-only Lesen ohne Suche oder Mutation.
- **4C — Atrium Exploration Surface:** Raumbeschreibung und Help sind getrennt;
  Help und Dispatcher teilen die Atrium-lokale Capability-Quelle.
- **Deliberate Return Opening:** Der bestehende manuelle Opening-Pfad bleibt
  erhalten; er erzeugt das stabile lokale Resultat einmal und ohne Overwrite.
- **5A — Return-Slot Identity Hardening:** Slice 5A führte nicht das gesamte
  Opening neu ein, sondern härtete den vorhandenen Pfad durch eine globale
  Duplicate-Prüfung vor jeder produktiven Arbeit und Mutation.
- **5B — Stable-result Revisit:** Explizites `/results` liest einen bekannten
  stabilen Markdown-Pfad lazy, strikt und allowlist-basiert; Same-process hat
  Vorrang.
- **Carrier Packaging:** `known_source.py` und `stable_result.py` stehen in der
  statischen Allowlist und sind isoliert importierbar.

Diese Slices sind technisch implementiert und automatisch verifiziert. Bereits
dokumentierte frühere manuelle Abnahmen bleiben gültig; eine abschließende
sprachweite Slice-7-Spielabnahme der neuen Gesamtstrecke steht noch aus.

## D. Slice 6 — Sprachinventur und sprachliche Endredaktion

### 6A — Read-only Sprachinventur

Zuerst werden alle player-facing Oberflächen ausschließlich lesend erfasst.
Jeder Befund erhält zwei Klassifikationen.

Priorität:

```text
MUSS
SOLLTE
SPÄTER
```

Befundart:

```text
reiner Sprachfehler
Text-/Zustandsmismatch
technischer Fehler
Dokumentationsdrift
```

Die Inventur verändert keine Quelle und trennt technische Defekte von reiner
Endredaktion.

### 6B ff. — Kleine autorisierte Sprachpakete

Mögliche Pakete werden nach der Inventur einzeln geprüft und freigegeben:

1. Atrium + First Spark;
2. Resonance PRE_RUN + produktive Prompts;
3. POST_RUN + `/results`;
4. BLOCKED + Recovery;
5. Return Opening + Stable-result-Anzeige;
6. README, Quick Start und Gift Instructions erst in der späteren Releasephase.

Keine Paketgrenze darf Opening, Resultatmodelle, Capability-Verträge oder
Sicherheitsgrenzen nebenbei verändern.

## E. Slice 7 — Baseline und finale Spielprüfung

### 7A — Kontrollierte Überlappung am eingefrorenen Checkpoint

```text
Frozen checkpoint 59c6595

Track A:
read-only language inventory

Track B:
manual baseline play verification against a fresh carrier/gift copy
```

Während des Baseline-Laufs erfolgen keine Source-Änderungen. Danach werden die
Befunde zusammengeführt. Kleine Sprachpakete benötigen jeweils eine eigene
Freigabe, fokussierte Tests und kurze Wiederholungsdurchläufe. Der vollständige
finale Play Run folgt erst nach den akzeptierten Textänderungen.

### Verbindlicher finaler Spielbogen

```text
COMPOSE
-> ANSWER
-> RETURN OPENING
-> RESULT REVISIT
```

Zusätzlich zu prüfen:

- zweiter unabhängiger COMPOSE-Zyklus;
- BLOCKED;
- Abbruch an maßgeblichen Grenzen;
- das Return Artifact wird bewusst in `incoming/` des bekannten privaten
  Return Workspace zurückgebracht;
- bei mehreren Kandidaten erfolgt niemals eine automatische Auswahl;
- genau ein erfolgreiches Opening;
- wiederholtes unverändertes Opening;
- Same-process-Vorrang vor Stable Source;
- fehlende und ungültige Known Source;
- keine Discovery, Regeneration oder Überschreibung;
- Carrier-Start aus Empfängerperspektive.

Die abschließende manuelle Akzeptanz darf erst nach diesem vollständigen Lauf
behauptet werden.

## F. Slice 7.5 — Read-only Gesamtprojekt-Audit und Mini-Dokumentations-Gate

### F.1 Eintrittsgate

Slice 7.5 beginnt erst, wenn:

- Slice 6 abgeschlossen und akzeptiert ist;
- Slice 7 vollständig manuell gespielt und akzeptiert ist;
- alle dabei erkannten Release-Blocker behoben und erneut geprüft sind;
- der Branch wieder einen sauberen, committed und pushed Checkpoint besitzt.

Diese Bedingungen sind mit diesem Planungsstand noch nicht erfüllt.

### F.2 Zweck

Slice 7.5 prüft Nexus 01 mit Abstand zur Detailimplementierung als
zusammenhängendes Repository und Release Candidate:

```text
Orientierung
-> Bewertung
-> kleine gezielte Abschlussentscheidungen
-> Dokumentationsvorbereitung
```

Bewertet werden umgesetztes Projektkonzept, Architektur- und
Verantwortungsgrenzen, Repository-Orientierung, aktuelle gegenüber historischen
Dokumenten, kleine belegte Cleanup-Kandidaten und release-facing
Projektbeschreibungen. Dies ist keine erneute Architekturentwicklung.

### F.3 Audit-Scope

Das Audit orientiert sich repository-weit, untersucht aber vertieft nur:

- Nexus-01-Produktionscode und -Tests;
- Packaging und neutralen Carrier;
- deliberate Return Opening;
- Same-process- und Stable-source-Resultatansichten;
- Nexus-01-Planungs- und Statusdokumente;
- direkt zugehörige README-, Quick-Start-, Playing-, Gift- und
  Return-Anleitungen;
- relevante Top-level-Einstiegspunkte.

Historische Experimente, fremde Module und Legacy-Material werden nur vertieft,
wenn sie vom aktuellen Release importiert werden, als aktueller öffentlicher
Einstieg erscheinen, release-facing Verwirrung erzeugen oder eine zentrale
veraltete Anweisung enthalten. Das Audit ist kein repository-weites
Refactoring-Review.

### F.4 Read-only First Gate

Der erste Slice-7.5-Codex-Auftrag ist vollständig read-only. Er darf getrackte
Struktur, Code, Tests, Packaging und Dokumentation lesen, aktuelle und
historische Anleitung vergleichen, konkrete Inkonsistenzen oder Duplikation
belegen, kleine Verbesserungen vorschlagen und release-facing Beschreibungen
entwerfen.

Er darf keine Dateien ändern; keine Git- oder Historienoperation ausführen;
keine Formatter, Generatoren, Paketerzeugung oder schreibenden Befehle starten;
keine Tests oder cache-erzeugenden Imports ausführen; keinen Bericht im
Repository erzeugen; und keine Refactors, Renames, Moves oder
Dependency-Änderungen vornehmen. Der Auditbericht existiert ausschließlich in
der Codex-Antwort.

### F.5 Beleg- und Interpretationsgrenzen

Das Audit trennt ausdrücklich:

```text
im Code und Spielablauf erkennbar
in kanonischer V0.3-Planung ausdrücklich erklärt
nur aus historischen Dokumenten ableitbar
aus dem Repository nicht hinreichend belegbar
```

Jeder Befund nennt einen konkreten Repository-Beleg. Das Audit beschreibt das
tatsächliche Projekt und erfindet keine neue Vision, Funktion, emotionale
Zusage oder künftige Architektur. Klar supersedete historische V0.2-Aussagen
sind nicht allein deshalb Releaseprobleme.

### F.6 Befundkategorien

Jeder Befund erhält genau eine Kategorie:

```text
RELEASE-BLOCKER
KLEINER SICHERER ABSCHLUSSFIX
NACHFOLGEARBEIT NACH DEM RELEASE
```

- **RELEASE-BLOCKER:** belegter Defekt, der Releasepfad, Privacy oder Safety
  verletzen, das Geschenkpaket unbenutzbar machen, materiell falsche oder
  unsichere Anleitung geben oder die finale Akzeptanz verhindern kann.
- **KLEINER SICHERER ABSCHLUSSFIX:** enger, belegter, testbarer Fix in wenigen
  Dateien ohne Architektur- oder Public-Contract-Änderung, der Releaseklarheit
  oder Robustheit wesentlich verbessert.
- **NACHFOLGEARBEIT NACH DEM RELEASE:** nicht releasekritische, strukturelle,
  neue Abstraktionen oder Dokumentationsarchitektur einführende beziehungsweise
  vorwiegend kosmetische Arbeit mit erhöhtem Sprint-Endrisiko.

Bei Unsicherheit gilt `NACHFOLGEARBEIT NACH DEM RELEASE`.

### F.7 Verbindliches Befundformat

```text
Titel:
Kategorie:
Bereich:
Beleg im Repository:
Warum relevant:
Risiko bei Nichtänderung:
Kleinste sinnvolle Maßnahme:
Vermutlich betroffene Dateien:
Empfohlener Zeitpunkt:
```

Vage Empfehlungen wie „Codebasis refactoren“, „Dokumentation verbessern“ oder
„Architektur vereinheitlichen“ gelten ohne konkreten Repository-Befund nicht
als Auditbeobachtung.

### F.8 Outside-perspective Entwürfe

Das read-only Audit schlägt vor, schreibt aber nicht ins Repository:

1. eine GitHub-Kurzbeschreibung mit zwei bis drei Sätzen;
2. eine README-Einleitung mit ungefähr zwei bis vier kurzen Absätzen;
3. eine knappe konzeptionelle Projektbeschreibung.

Die Entwürfe bleiben sachlich und belegt. Sie machen den technischen und
spielerischen Nexus-01-Kern, Atrium, First Spark, Resonance, Return und Revisit,
explizite Interaktion statt Discovery, lokale Privacy-Grenzen, deliberate
Return und spätere Wiederlektüre sowie die Grenze zwischen Geschenkrelease und
künftigen Möglichkeiten sichtbar.

### F.9 Entscheidungsgate

Nach dem Audit erhält jeder Vorschlag gemeinsam genau eine Entscheidung:

```text
akzeptieren
vor Release beheben
nach Release verschieben
bewusst nicht verfolgen
```

Kein Vorschlag autorisiert automatisch eine Änderung. Vor Slice 8 dürfen nur
ausgewählte `RELEASE-BLOCKER` oder `KLEINER SICHERER ABSCHLUSSFIX`-Befunde
umgesetzt werden.

Ein bestätigter `RELEASE-BLOCKER` kann nicht mit `bewusst nicht verfolgen`
abgeschlossen werden. Vor dem Release muss er behoben und erneut geprüft oder
durch konkrete Repository-Belege als nicht release-blockierend nachgewiesen
und formal neu klassifiziert werden. Andernfalls bleibt der Release blockiert;
bloße Uneinigkeit ändert den Blockerstatus nicht.

### F.10 Kleine Änderungspakete

Jedes akzeptierte, eng zusammengehörige Paket erhält einen eigenen schmalen
Codex-Auftrag, strikte Dateigrenzen, angemessene fokussierte Prüfungen,
vollständiges Diff-Review, einen kohärenten Commit und bei player-facing
Änderungen einen kurzen manuellen Replay. Mehrere eng zusammengehörige Befunde
dürfen ein Paket bilden; ein Catch-all-Paket „allgemeines Aufräumen“ ist nicht
zulässig.

### F.11 Mini-Dokumentations-Gate

Nach Auditreview darf eine kleine autorisierte Synchronisierung ausgewählter
aktueller Einstiegsdokumente erfolgen: Haupt-README, Nexus-01-README, Quick
Start, `PLAYING_A_NEXUS.md`, `CURRENT_DIRECTION.md`, Gift-/Return-Anleitungen
und Release-Übergabe.

Sie beantwortet:

```text
Was ist Nexus 01?
Wie starte und spiele ich die Geschenkfassung?
Wie funktionieren Resonance, Return Opening und Result Revisit?
Welche Privacy- und Sicherheitsgrenzen gelten?
Welcher Stand ist aktuell?
Wo liegen die kanonischen technischen Verträge?
```

Die kanonischen technischen Verträge bleiben im Repository. Ein GitHub Wiki
kann bewertet werden, gilt aber standardmäßig als
`NACHFOLGEARBEIT NACH DEM RELEASE`, weil es einen zweiten Pflegeort erzeugt.
Vor Release kommt es nur bei einem belegten release-blockierenden
Orientierungsproblem infrage, das Repository-Dokumentation nicht lösen kann.

### F.12 Abschlussgate

Slice 7.5 ist erst abgeschlossen, wenn das relevante Projekt read-only auditiert
wurde; jeder Befund Beleg und Releasekategorie besitzt; die drei
Beschreibungsvorschläge vorliegen; der Bericht reviewed wurde; erlaubte
Pre-Release-Pakete ausdrücklich ausgewählt wurden; jeder bestätigte
`RELEASE-BLOCKER` behoben und erneut geprüft oder belegbasiert neu klassifiziert
wurde; ausgewählte `KLEINER SICHERER ABSCHLUSSFIX`-Befunde getrennt umgesetzt
und akzeptiert oder bewusst abgelehnt wurden; größere Ideen als Nachfolgearbeit
erfasst sind; autorisierte release-facing Dokumentation synchronisiert ist;
und der Branch wieder einen sauberen, committed und pushed Checkpoint besitzt.

## G. Slice 8 — Release Freeze

Slice 8 verifiziert und friert das bereits akzeptierte Ergebnis ein. Geplante
Orientierungsarbeit und Mini-Dokumentationssynchronisierung gehören in Slice
7.5. Slice 8 führt kein geplantes Feature, keine Architektur, keinen Refactor
und kein neues Dokumentationssystem ein; es korrigiert nur belegte
Releasefehler.

1. Code, aktuelle Dokumentation und Paket auf denselben akzeptierten Checkpoint
   prüfen;
2. finalen kanonischen Testlauf ausführen;
3. finalen Scope- und Sicherheitsdiff prüfen;
4. Releasepaket erzeugen;
5. Paket aus einem leeren temporären Verzeichnis testen;
6. PR vorbereiten;
7. Merge und Release-Tag als getrennte ausdrückliche Entscheidungen behandeln.

## H. Definition of Done

Vor einem PR müssen gelten:

- Slice 6 abgeschlossen und akzeptiert;
- Slice-7-Baseline und vollständiger finaler Spielbogen akzeptiert;
- Slice-7.5-Audit und Entscheidungsgate abgeschlossen;
- alle bestätigten Release-Blocker behoben und erneut geprüft oder belegbasiert
  neu klassifiziert;
- ausgewählte kleine sichere Abschlussfixes umgesetzt und akzeptiert oder
  bewusst abgelehnt;
- autorisierte release-facing Dokumentation synchronisiert;
- Branch an einem sauberen committed Checkpoint;
- kanonische Suite vollständig grün;
- Paket im leeren temporären Verzeichnis erfolgreich geprüft.

Ein bestätigter ungelöster Release-Blocker verhindert PR-Vorbereitung, Merge,
Release-Tag und Release.

PR, Merge und Release-Tag bleiben getrennte ausdrückliche Entscheidungen. Vor
Merge und Tag müssen zusätzlich gelten:

- manueller finaler Play Run akzeptiert;
- PR-Review abgeschlossen;
- Merge ausdrücklich entschieden;
- veröffentlichter Commit eindeutig bestimmt;
- Tagname und Releaseinhalt separat bestätigt.

Bis dahin bleiben PR, Merge und Tag nicht freigegeben.
