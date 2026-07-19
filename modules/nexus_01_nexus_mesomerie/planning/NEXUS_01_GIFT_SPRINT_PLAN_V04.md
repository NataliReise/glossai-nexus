# Nexus 01 Sprintplan — Geschenkfassung V0.4

## Dokumentstatus

- Version: 0.4
- Status: Current
- Datum: 2026-07-19
- Ersetzt: Version 0.3
- Zweck: Kanonischer Abschlussplan für die Geschenkfassung nach Abschluss der großen technischen Umsetzungsslices und Wechsel zu einem dokumentgestützten, mehrstufigen Arbeitsmodus.

## A. Ausgangspunkt

- Branch: `gift/nexus-01-chamber-archive`
- Technischer Baseline-Checkpoint: `59c6595`
- Aktueller Branch-Checkpoint bei Planungsbeginn: `a71db33`
- Upstream: `origin/gift/nexus-01-chamber-archive`
- Letzte kanonische Baseline-Suite am technischen Checkpoint: 43 Testdateien, 408 Tests, 0 Failures, 0 Errors, 0 Skips
- Die großen technischen Slices sind bis einschließlich Stable-result Revisit abgeschlossen.
- Ein erster manueller Empfänger-/COMPOSE-Durchlauf aus einer frischen Carrier-Kopie war erfolgreich.
- Die erste kleine First-Spark-Abschlussdarstellung wurde anschließend gezielt überarbeitet und fokussiert getestet.

Die noch offene Arbeit ist vor allem redaktionell, spielerlebnisbezogen, dokumentarisch und release-orientiert. Sie soll nicht durch neue Architektur oder ungeprüfte Funktionsausweitung verdrängt werden.

## B. Ziel der Geschenkfassung

Die Geschenkfassung von Nexus 01 ermöglicht einer Person ohne vorherige Projektkenntnis, ein lokal ausgeführtes kreatives Softwaregeschenk zu öffnen, die persönliche First-Spark-Erfahrung zu durchlaufen, Atrium und Resonance Chamber verständlich zu entdecken, eine eigene Resonanz bewusst zu gestalten und die Möglichkeit ihrer freiwilligen menschlichen Weitergabe zu verstehen.

Die Erfahrung bleibt lokal, nachvollziehbar und sicher. Sie sucht keine privaten Inhalte, überträgt nichts automatisch und führt keine produktive Handlung ohne ausdrückliche Entscheidung aus. Sprache, Terminaldarstellung und Anleitung geben genügend Orientierung, ohne die poetische Entdeckung durch technische Erklärungen zu überdecken.

> Die Geschenkfassung wird nicht durch möglichst viele Funktionen wertvoll, sondern durch eine kleine, in sich geschlossene Erfahrung, deren Technik, Sprache, Atmosphäre und menschliche Bedeutung zuverlässig zusammenwirken.

## C. Wechsel des Arbeitsmodus

Codex war in der vorangegangenen Projektphase ein wichtiges Werkzeug für technische Bestandsaufnahme, klar abgegrenzte Umsetzungsslices und fokussierte Testergänzungen.

Nach Abschluss der großen technischen Umsetzungsslices verlagert sich der Schwerpunkt auf redaktionelle Präzision, manuelle Spielprüfung, kleinteilige Release-Arbeit sowie die sorgfältige Abstimmung zwischen Spielerlebnis, Sprache, Dokumentation und bestehender technischer Struktur.

Das Projekt wechselt deshalb für diese Phase zu einem dokumentgestützten, mehrstufigen Workflow mit:

- ausdrücklicher Planung;
- unabhängiger Gegenprüfung in frischem Kontext;
- einer daraus abgeleiteten Roadmap;
- kleinen, klar begrenzten Arbeitskarten;
- fokussierter Umsetzung;
- Diff-, Test- und manueller Spielprüfung nach jedem Arbeitsschritt.

Codex wird in dieser Phase nicht als reguläres Umsetzungswerkzeug eingeplant. Ein späterer gezielter Einsatz bleibt nach ausdrücklicher Entscheidung möglich.

Der verbindliche Arbeitsmodus ist in `NEXUS_01_COLLABORATION_WORKFLOW_V01.md` beschrieben.

## D. Verbindliche Abschlussgrenzen

Für den Geschenkabschluss gilt:

- keine neue Architektur und kein allgemeines Command- oder Result-Framework;
- keine Workspace-, Downloads-, Token-, Artifact- oder Ergebnis-Discovery;
- keine Registry, automatische Kandidatenauswahl oder Dateinamensvermutung;
- Return Opening und `/results` bleiben strikt getrennt;
- Same-process-Resultate und Stable-source-Resultate bleiben getrennte Modelle;
- keine automatische Übertragung, Regeneration, Reparatur oder Überschreibung;
- keine privaten Pfade oder Inhalte im travelling carrier;
- keine unbegründete Vergrößerung des Geschenk-Scope;
- keine Historienumschreibung als kosmetische Aufräummaßnahme;
- nur ausdrücklich autorisierte, belegte und überprüfbare Abschlusskorrekturen.

Ein neuer Einfall erweitert den Geschenksprint nicht automatisch. Er wird entweder:

- als notwendige Releasekorrektur belegt;
- als kleine sichere Verbesserung bewusst freigegeben;
- oder für die normale Nexus-Weiterentwicklung bewahrt.

## E. Zwei große Projektstufen

### Stufe 1 — Geschenkfassung abschließen

Ziel:

```text
vollenden
-> vereinfachen
-> dokumentieren
-> prüfen
-> einfrieren
```

Diese Stufe endet mit einer stabilen, verständlichen, atmosphärisch stimmigen und isoliert geprüften Geschenkfassung.

### Stufe 2 — Normale Nexus-Weiterentwicklung

Ziel:

```text
erforschen
-> erweitern
-> abstrahieren
-> neue Formen erproben
```

Diese Stufe beginnt erst nach Geschenk-Freeze und Nachgeschenk-Retrospektive. Größere Architekturfragen, neue Chambers, Archive-, Constellation-, Launcher- oder Accessibility-Entwicklung gehören grundsätzlich hierhin.

## F. Mehrstufiger Qualitätsworkflow

Jede größere Ebene folgt demselben Muster:

```text
Planung
-> Gegencheck in frischem Kontext
-> Roadmap
-> Gegencheck
-> Arbeitskarten
-> Gegencheck
-> kleine Umsetzung
-> Diff- und Testprüfung
-> manueller Kurztest
-> Annahme oder Nacharbeit
```

Ein Gegencheck entscheidet nichts automatisch. Seine Befunde werden gemeinsam geprüft und einzeln angenommen, verändert, verschoben oder verworfen.

## G. Abschlussroadmap der Geschenkfassung

### Phase 1 — Strategie und Planung synchronisieren

Ergebnisse:

- Sprintplan V0.4;
- Collaboration Workflow V0.1;
- aktualisierter Living Status;
- klare Grenze zwischen Geschenkabschluss und späterer Projektentwicklung;
- neutral dokumentierter Wechsel des Arbeitsmodus.

### Phase 2 — Empfängerperspektive und Bestandsaufnahme

Alle relevanten Oberflächen werden zunächst beobachtet und klassifiziert:

```text
Start und Aktivierung
Atrium
First Spark
Resonance PRE_RUN
COMPOSE
POST_RUN
/results
ANSWER
Return Opening
Stable-result Revisit
BLOCKED und Fehlerpfade
Anleitungen und Verpackung
```

Jeder Befund erhält:

```text
Priorität:
MUSS / SOLLTE / SPÄTER

Art:
Sprache / Darstellung / Zustandsmismatch /
technischer Defekt / Dokumentationsdrift
```

Bereits dokumentierte manuelle Befunde bleiben Teil dieser Inventur.

### Phase 3 — Redaktionelle Release-Roadmap

Aus der Inventur werden begrenzte Arbeitspakete gebildet:

1. Aktivierung und First Spark;
2. Atrium und Orientierung;
3. Resonance PRE_RUN und Hilfe;
4. COMPOSE-Auswahl, Review und Abschluss;
5. POST_RUN und `/results`;
6. ANSWER, Return Opening und Revisit;
7. BLOCKED, Abbruch und Fehlerpfade;
8. Anleitungen, Carrier und Geschenkpaket.

Jeder Befund erhält genau eine Entscheidung:

```text
vor Geschenkübergabe beheben
nur bei geringem Risiko verbessern
nach dem Geschenk weiterverfolgen
bewusst nicht verfolgen
```

### Phase 4 — Arbeitskarten und kleinteilige Umsetzung

Jede Änderung beginnt mit einer Arbeitskarte. Sie beschreibt mindestens:

```text
ID und Titel
Ausgangslage
Spielerproblem
Gewünschtes Ergebnis
In Scope
Nicht in Scope
Betroffene Dateien
Unveränderliche Grenzen
Tests
Manuelle Prüfung
Definition of Done
Abbruchkriterium
```

Eine Karte soll möglichst wenige Dateien betreffen, keine neue Architektur einführen und einen fokussierten Test sowie einen kurzen manuellen Wiederholungslauf ermöglichen.

### Phase 5 — Dokumentationsinventur und Zielbild

Alle öffentlich oder release-nah sichtbaren Dokumente werden eingeordnet als:

```text
KANONISCH AKTUELL
HISTORISCH
ARBEITSNOTIZ
DUPLIKAT ODER DRIFT
SPÄTER
```

Zu prüfen sind insbesondere:

- Root-README;
- Nexus-01-README;
- Quick Start und Linux-Einstieg;
- Playing-a-Nexus-Anleitung;
- Gift Instructions;
- Aktivierungs-, Carrier-, Return- und Opening-Anleitungen;
- Architektur- und Konzeptdokumente;
- aktuelle Planungs-, Vertrags- und Statusdokumente;
- alte Versionsstände, Experimente und interne Arbeitsnotizen;
- Verweise zwischen Dokumenten.

Ziel ist eine eindeutige Dokumenthierarchie:

```text
README
-> Projektüberblick und Einstieg

Nexus-01-README
-> Modulüberblick und Startwege

Quick Start
-> kürzester technisch sicherer Start

Playing a Nexus
-> spielerische Grundidee

Gift Instructions
-> Empfängeranleitung

Return Guide
-> Weitergabe, Antwort, Opening und Revisit

Concept Documents
-> Vision, Architektur, Privacy, Resonance, Archive

Planning / Status
-> Entwicklungsstand, nicht primärer Spieleinstieg
```

Information soll möglichst einen klaren Hauptort besitzen. Andere Dokumente verweisen dorthin, statt dieselbe Erklärung in driftenden Varianten zu wiederholen.

### Phase 6 — Repository-Aufräumung

Sicher und sinnvoll vor dem Geschenk sind:

- veraltete aktuelle Hinweise korrigieren;
- überholte Dokumente klar als superseded oder historisch markieren;
- tote Links reparieren;
- doppelte Einstiegshinweise reduzieren;
- Dateinamen, Navigation und release-nahe Verweise prüfen;
- lokale oder generierte Dateien aus dem Repository fernhalten;
- `.gitignore` gegen reale Nebendateien prüfen;
- irreführende Platzhalter oder veraltete öffentliche Einstiegspunkte beurteilen.

Nur mit eigener Arbeitskarte und Gegenprüfung zulässig sind:

- Dateien verschieben, umbenennen, zusammenführen oder löschen;
- Importpfade oder Verzeichnisstruktur ändern;
- Legacy-Code entfernen;
- Teststruktur reorganisieren;
- Commit-Historie verändern.

> Wir räumen die sichtbare Gegenwart des Repositorys auf, nicht rückwirkend seine Entstehungsgeschichte.

### Phase 7 — Wiki-Synchronisierung

Das Wiki wird erst nach der Repository-Dokumentation aktualisiert. Es fasst zusammen und verweist auf maßgebliche Repository-Dokumente; es wird keine zweite unkontrollierte Quelle versionskritischer Wahrheit.

Vorgesehenes Zielbild:

```text
Home
├── Was ist Nexus?
├── Nexus 01 – Nexus-Mesomerie
├── Spielen und Weitertragen
├── First Spark
├── Resonance, Return und Revisit
├── Privacy und lokale Kontrolle
├── Begriffe und Glossar
├── Projektgeschichte
└── Entwicklung und Roadmap
```

Exakte Startbefehle, versionskritische Installationsanweisungen, Release-Verträge, Formate und Teststatus bleiben primär im Repository.

### Phase 8 — Dokumentations- und Außenperspektiv-Gegencheck

Ein frischer Kontext prüft insbesondere:

- Findet eine neue Person den richtigen Einstieg?
- Widersprechen sich README, Anleitung und Wiki?
- Ist erkennbar, was aktuell, historisch und experimentell ist?
- Werden nur tatsächlich vorhandene Funktionen versprochen?
- Sind Privacy- und Sicherheitsgrenzen korrekt beschrieben?
- Tauchen private Identitäten oder lokale Rechnerdaten auf?
- Ist die Geschenkfassung von der späteren Projektvision unterscheidbar?
- Gibt es tote, zirkuläre oder irreführende Verweise?
- Ist die öffentliche Projektidentität konsistent?

### Phase 9 — Vollständiger Geschenkpfad

Der verbindliche Gesamtbogen lautet:

```text
frisches Geschenkpaket
-> Aktivierung
-> First Spark
-> COMPOSE
-> bewusste Weitergabe
-> ANSWER
-> bewusstes Return Opening
-> Stable-result Revisit
```

Zusätzlich zu prüfen:

- zweiter unabhängiger COMPOSE-Zyklus;
- BLOCKED;
- Abbruch an maßgeblichen Grenzen;
- fehlende und ungültige Known Source;
- mehrere Return-Kandidaten ohne automatische Auswahl;
- genau ein erfolgreiches Opening;
- wiederholtes unverändertes Opening;
- Same-process-Vorrang vor Stable Source;
- keine Discovery, Regeneration oder Überschreibung;
- Carrier-Start aus Empfängerperspektive;
- tatsächliche Nutzbarkeit der veröffentlichten Anleitungen.

Während dieses vollständigen Laufs wird nicht nebenbei redigiert. Neue Befunde werden notiert und anschließend als eigene Karten behandelt.

### Phase 10 — Release-Audit und Geschenk-Freeze

Ein frischer Kontext erhält Ziel, Plan, Grenzen, relevanten Stand, Testergebnisse und manuelle Abnahmen. Befunde werden klassifiziert als:

```text
RELEASE-BLOCKER
KLEINER SICHERER ABSCHLUSSFIX
NACHFOLGEARBEIT NACH DEM GESCHENK
```

Danach folgen:

- nur autorisierte Abschlusskorrekturen;
- fokussierte und vollständige Tests;
- neuer Paketbau;
- isolierte Paketprüfung;
- letzter Empfängerperspektiv-Lauf;
- dokumentierter Release-Checkpoint;
- separate Entscheidung über PR, Merge, Tag oder Veröffentlichung.

## H. Git-, Connector- und Identitätsregeln

Vor jeder Änderung wird der Branch geprüft. Verbindlicher Arbeitsbranch ist derzeit:

```text
gift/nexus-01-chamber-archive
```

Lokaler Checkout und Remote-Branch werden nicht parallel divergent bearbeitet. Es wird zuerst synchronisiert und anschließend nur an einem Ort weitergearbeitet.

Ohne ausdrückliche Freigabe erfolgen keine Branch-, Merge-, Rebase-, Reset-, Push-, PR-, Tag- oder Release-Aktionen.

Öffentliche Projektidentität:

```text
Natali / Natali Reise
info@glossai.de
```

Die technische Connector-Identität `eulisiller` ist für Connector-Commits zulässig. Private Berufsidentitäten und deren Kombination mit dem Familiennamen dürfen in öffentlichen Projektdateien, Commits, Issues, Wiki-Seiten oder Release-Texten nicht verwendet werden.

## I. Definition of Done für den Geschenksprint

Der Geschenksprint ist erst abgeschlossen, wenn:

- die Geschenkfassung aus frischer Empfängerperspektive startbar ist;
- der vollständige Geschenkpfad erfolgreich manuell durchlaufen wurde;
- relevante Abbruch-, BLOCKED- und Sicherheitsfälle geprüft sind;
- keine bestätigten Release-Blocker offen sind;
- alle release-nahen Anleitungen dem tatsächlichen Verhalten entsprechen;
- Repository-Einstieg, Dokumenthierarchie und Wiki konsistent sind;
- keine private Identität oder lokale Maschineninformation veröffentlicht wird;
- das finale Paket neu gebaut und isoliert geprüft wurde;
- der akzeptierte Stand sauber dokumentiert und eingefroren ist.

## J. Übergang zur normalen Weiterentwicklung

Nach dem Geschenk-Freeze folgt eine eigene Nachgeschenk-Retrospektive. Sie dokumentiert:

- bewährte Spielerlebnisse und Architekturgrenzen;
- erkannte Unklarheiten und technische Schulden;
- bewusst vertagte Ideen;
- nur für den Geschenktermin entstandene Sonderlösungen;
- mögliche nächste Entwicklungsstränge.

Erst danach entsteht eine neue allgemeine Projektroadmap, beispielsweise `NEXUS_PROJECT_ROADMAP_V01.md`. Die Geschenkfassung bleibt als eigener historischer Meilenstein erhalten und wird nicht stillschweigend zur beweglichen Dauerbaustelle erklärt.

## K. Unmittelbare nächste Schritte

1. Planungsdokumente vollständig synchronisieren.
2. Den neuen Plan in einem frischen Kontext gegenprüfen.
3. Befunde gemeinsam entscheiden und gegebenenfalls eine korrigierte Planversion erstellen.
4. Eine konkrete Geschenkabschluss-Roadmap aus den vorhandenen manuellen Befunden und der Dokumentationsinventur ableiten.
5. Die ersten kleinen Arbeitskarten erstellen.
6. Erst danach weitere player-facing oder dokumentarische Änderungen umsetzen.
