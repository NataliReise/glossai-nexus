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
- Branch-Checkpoint vor der ersten V0.4-Planungssynchronisierung: `a71db33`
- Erster V0.4-Planungscheckpoint: `4904606`
- Upstream: `origin/gift/nexus-01-chamber-archive`
- Letzte kanonische Baseline-Suite am technischen Checkpoint: 43 Testdateien, 408 Tests, 0 Failures, 0 Errors, 0 Skips
- Die großen technischen Slices sind bis einschließlich Stable-result Revisit abgeschlossen.
- Ein erster manueller Empfänger-/COMPOSE-Durchlauf aus einer frischen Carrier-Kopie war erfolgreich.
- Die erste kleine First-Spark-Abschlussdarstellung wurde anschließend gezielt überarbeitet und fokussiert getestet.

Die noch offene Arbeit ist vor allem redaktionell, spielerlebnisbezogen, dokumentarisch, repository-bezogen und release-orientiert. Sie soll nicht durch neue Architektur oder ungeprüfte Funktionsausweitung verdrängt werden.

## B. Ziel der Geschenkfassung

Die Geschenkfassung von Nexus 01 ermöglicht einer Person ohne vorherige Projektkenntnis, ein lokal ausgeführtes kreatives Softwaregeschenk zu öffnen, die persönliche First-Spark-Erfahrung zu durchlaufen, Atrium und Resonance Chamber verständlich zu entdecken, eine eigene Resonanz bewusst zu gestalten und die Möglichkeit ihrer freiwilligen menschlichen Weitergabe zu verstehen.

Die Erfahrung bleibt lokal, nachvollziehbar und sicher. Sie sucht keine privaten Inhalte, überträgt nichts automatisch und führt keine produktive Handlung ohne ausdrückliche Entscheidung aus. Sprache, Terminaldarstellung, Repository-Einstieg, Wiki und Anleitung geben genügend Orientierung, ohne die poetische Entdeckung durch technische Erklärungen zu überdecken.

> Die Geschenkfassung wird nicht durch möglichst viele Funktionen wertvoll, sondern durch eine kleine, in sich geschlossene Erfahrung, deren Technik, Sprache, Atmosphäre und menschliche Bedeutung zuverlässig zusammenwirken.

## C. Wechsel des Arbeitsmodus

Codex war in der vorangegangenen Projektphase ein wichtiges Werkzeug für technische Bestandsaufnahme, klar abgegrenzte Umsetzungsslices und fokussierte Testergänzungen.

Nach Abschluss der großen technischen Umsetzungsslices verlagert sich der Schwerpunkt auf redaktionelle Präzision, manuelle Spielprüfung, kleinteilige Release-Arbeit sowie die sorgfältige Abstimmung zwischen Spielerlebnis, Sprache, Dokumentation, öffentlicher Projektoberfläche und bestehender technischer Struktur.

Das Projekt wechselt deshalb für diese Phase zu einem dokumentgestützten, mehrstufigen Workflow mit:

- ausdrücklicher Planung;
- unabhängiger Gegenprüfung in frischem Kontext;
- einer daraus abgeleiteten Roadmap;
- ausdrücklicher Roadmap-Gegenprüfung;
- kleinen, klar begrenzten Arbeitskarten;
- ausdrücklicher Gegenprüfung umsetzungsbereiter Kartenpakete;
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
- keine Umschreibung veröffentlichter Historie zur kosmetischen Bereinigung;
- nur autorisierte, belegte und überprüfbare Abschlusskorrekturen.

Ein neuer Einfall erweitert den Geschenksprint nicht automatisch. Er wird entweder:

- als notwendige Releasekorrektur belegt;
- als kleine sichere Verbesserung bewusst freigegeben;
- oder für die normale Nexus-Weiterentwicklung bewahrt.

## E. Zwei große Projektstufen

### Stufe 1 — Geschenkfassung abschließen

```text
vollenden
-> vereinfachen
-> dokumentieren
-> öffentlich kuratieren
-> prüfen
-> einfrieren
```

Diese Stufe endet mit einer stabilen, verständlichen, atmosphärisch stimmigen, öffentlich glaubwürdigen und isoliert geprüften Geschenkfassung.

### Stufe 2 — Normale Nexus-Weiterentwicklung

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
-> Plan-Gegencheck in frischem Kontext
-> Roadmap
-> Roadmap-Gegencheck
-> Arbeitskarten
-> Kartenpaket-Gegencheck
-> kleine Umsetzung
-> Diff- und Testprüfung
-> manueller Kurztest
-> Annahme, Nacharbeit oder Entscheidung über eine Rücknahme
```

Ein Gegencheck entscheidet nichts automatisch. Seine Befunde werden gemeinsam geprüft und einzeln angenommen, verändert, verschoben oder verworfen.

Eine Entscheidung über eine Rücknahme autorisiert noch keine konkrete Git-Aktion. Die geeignete Wiederherstellungsmethode wird gesondert geprüft und innerhalb der geltenden Freigabegrenze entschieden.

Gegenchecks beziehen sich auf abgeschlossene Planungsebenen oder umsetzungsbereite Kartenpakete. Nicht jede einzelne kleine Wortkorrektur benötigt einen eigenen neuen Chat.

## G. Abschlussroadmap der Geschenkfassung

### Phase 1 — Strategie und Planung synchronisieren

Ergebnisse:

- Sprintplan V0.4;
- Collaboration Workflow V0.1;
- aktualisierter Living Status;
- klare Grenze zwischen Geschenkabschluss und späterer Projektentwicklung;
- neutral dokumentierter Wechsel des Arbeitsmodus;
- angenommene Klarstellungen aus dem ersten Fresh-context Review.

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
Anleitungen, Repository, Wiki und Verpackung
```

Jeder Befund erhält:

```text
Priorität:
MUSS / SOLLTE / SPÄTER

Art:
Sprache / Darstellung / Zustandsmismatch /
technischer Defekt / Dokumentationsdrift /
Repository- oder Wiki-Orientierung / Packaging
```

Bereits dokumentierte manuelle Befunde bleiben Teil dieser Inventur.

### Phase 3 — Redaktionelle und release-bezogene Roadmap

Aus der Inventur werden begrenzte Arbeitspakete gebildet:

1. Aktivierung und First Spark;
2. Atrium und Orientierung;
3. Resonance PRE_RUN und Hilfe;
4. COMPOSE-Auswahl, Review und Abschluss;
5. POST_RUN und `/results`;
6. ANSWER, Return Opening und Revisit;
7. BLOCKED, Abbruch und Fehlerpfade;
8. Anleitungen, Carrier und Geschenkpaket;
9. öffentliche Repository-Kuration;
10. release-relevanter Wiki-Kern.

Jeder Befund erhält genau eine Entscheidung:

```text
vor Geschenkübergabe beheben
nur bei geringem Risiko verbessern
nach dem Geschenk weiterverfolgen
bewusst nicht verfolgen
```

**Roadmap-Gate:** Die vollständige priorisierte Roadmap wird in frischem Kontext geprüft, bevor Kartenpakete als umsetzungsbereit gelten.

### Phase 4 — Arbeitskarten und kleinteilige Umsetzung

Jede Änderung beginnt mit einer Arbeitskarte. Sie beschreibt mindestens:

```text
ID und Titel
Ausgangslage
Spieler- oder Repository-Problem
Gewünschtes Ergebnis
In Scope
Nicht in Scope
Betroffene Dateien
Unveränderliche Grenzen
Tests
Manuelle Prüfung
Definition of Done
Abbruch- oder Rücknahmekriterium
```

Eine Karte soll möglichst wenige Dateien betreffen, keine neue Architektur einführen und einen fokussierten Test sowie einen kurzen manuellen Wiederholungslauf ermöglichen.

**Karten-Gate:** Ein abgeschlossenes umsetzungsbereites Kartenpaket wird vor der ersten Umsetzung in frischem Kontext geprüft.

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
- Verweise zwischen Repository und Wiki.

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

### Phase 6 — Öffentliche Repository-Kuration

Das Repository ist nicht nur Codeablage, sondern Teil des öffentlich begehbaren Nexus-Projektraums und kann von Spielenden besucht werden.

Release-relevante Kuration umfasst:

- aktuelle Hinweise und klare Einstiegswege;
- Kennzeichnung überholter oder historischer Dokumente;
- Reparatur toter oder irreführender Links;
- Reduktion doppelter Einstiegshinweise;
- Prüfung von Dateinamen, Navigation und release-nahen Verweisen;
- Fernhalten lokaler oder generierter Nebendateien;
- `.gitignore`-Prüfung gegen reale Nebendateien;
- Korrektur irreführender öffentlicher Platzhalter;
- kleine dokumentarische Verschiebungen oder Umbenennungen nur mit eigener Karte und nach belegtem Orientierungsnutzen.

Grundsätzlich nach dem Geschenk erfolgen:

- großflächige Code- oder Verzeichnisreorganisation;
- Importpfadänderungen aus Ordnungserwägungen;
- Testarchitektur-Reorganisation;
- pauschale Legacy-Entfernung;
- große Datei- oder Modulzusammenführungen;
- Umschreibung veröffentlichter Commit-Historie.

Eine technische Strukturänderung darf nur dann in den Geschenkabschluss gelangen, wenn ein bestätigter Release-Blocker anders nicht sicher und kleiner behoben werden kann.

> Wir kuratieren die sichtbare Gegenwart des Repositorys und verändern seine veröffentlichte Vergangenheit nicht aus kosmetischen Gründen.

### Phase 7 — Wiki-Synchronisierung

Das Wiki wird erst nach der Repository-Dokumentation aktualisiert. Es fasst zusammen und verweist auf maßgebliche Repository-Dokumente; es wird keine zweite unkontrollierte Quelle versionskritischer Wahrheit.

Verbindlicher Wiki-Releasekern:

- glaubwürdige und aktuelle Home-Seite;
- verständlicher Projekt- und Nexus-01-Einstieg;
- Spielen und Weitertragen;
- Resonance, Return und Revisit;
- Privacy und lokale Kontrolle;
- aktueller Entwicklungsstand oder klarer Roadmap-Verweis;
- funktionierende Links zu kanonischen Repository-Dokumenten.

Langfristiges Wiki-Zielbild:

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

Glossar, vollständige Projektgeschichte, detaillierte Architekturseiten und langfristige Roadmap müssen vor der Geschenkübergabe nicht vollständig neu aufgebaut werden. Bereits vorhandene öffentliche Seiten dürfen jedoch nicht widersprüchlich, sichtbar veraltet oder irreführend bleiben.

Exakte Startbefehle, versionskritische Installationsanweisungen, Release-Verträge, Formate und Teststatus bleiben primär im Repository.

### Phase 8 — Dokumentations-, Metadaten- und Außenperspektiv-Gegencheck

Ein frischer Kontext prüft insbesondere:

- Findet eine neue Person den richtigen Einstieg?
- Widersprechen sich README, Anleitung und Wiki?
- Ist erkennbar, was aktuell, historisch und experimentell ist?
- Werden nur tatsächlich vorhandene Funktionen versprochen?
- Sind Privacy- und Sicherheitsgrenzen korrekt beschrieben?
- Tauchen private Identitäten oder lokale Rechnerdaten auf?
- Ist die Geschenkfassung von der späteren Projektvision unterscheidbar?
- Gibt es tote, zirkuläre oder irreführende Verweise?
- Sind Autor-, Committer-, E-Mail-, Committext- und gegebenenfalls Tag-Metadaten für die Veröffentlichung zulässig?

Ein problematischer Metadatenbefund führt zu einer gesonderten Entscheidung und autorisiert keine automatische Historienumschreibung.

### Phase 9 — Manueller vollständiger Geschenkpfad

#### Testrollen und Dateigrenzen

Eine Person darf alle Rollen kontrolliert simulieren, solange die realen Informations- und Dateigrenzen erhalten bleiben:

```text
Rolle A: schenkende / wartende Seite
-> frisches Geschenkpaket
-> COMPOSE
-> travelling invitation
-> privater Return Workspace verbleibt auf dieser Seite

Rolle B: empfangende / antwortende Seite
-> erhält nur die bewusst übertragene Einladung
-> ANSWER
-> erzeugt Return Artifact

Rolle A2: zurückkehrende wartende Seite
-> erhält das Artifact bewusst zurück
-> legt es im bekannten incoming-Bereich ab
-> Return Opening
-> Stable-result Revisit
```

Voraussetzungen:

- frisches, eindeutig identifiziertes Geschenkpaket;
- getrennte lokale Bereiche für die simulierten Rollen;
- bewusste Kopier- oder Paketierungsschritte;
- keine unbeabsichtigte Wiederverwendung alter Tokens, Artifacts oder Ergebnisse;
- keine Rolle liest Dateien, die ihr im realen Austausch nicht zur Verfügung stünden;
- der private Return Workspace bleibt auf der wartenden Seite.

#### Verbindlicher Gesamtbogen

```text
identifiziertes frisches Geschenkpaket
-> Aktivierung
-> First Spark
-> COMPOSE
-> bewusste rollengetrennte Weitergabe
-> ANSWER
-> bewusstes Return Opening
-> Stable-result Revisit
```

#### Verbindlicher Mindestumfang der Negativprüfung

- COMPOSE-Abbruch beziehungsweise `/cancel`;
- ANSWER-Abbruch beziehungsweise `/cancel`;
- BLOCKED ohne produktive Aktion;
- fehlende Known Source;
- ungültige Known Source;
- null Return-Kandidaten;
- mehrere Return-Kandidaten ohne automatische Auswahl;
- wiederholtes Opening ohne Überschreibung;
- zweiter unabhängiger COMPOSE-Zyklus;
- keine Discovery, automatische Reparatur, Regeneration oder Übertragung.

Während dieses vollständigen Laufs wird nicht nebenbei redigiert. Neue Befunde werden notiert und anschließend als eigene Karten behandelt.

### Phase 10 — Paketidentität, Release-Audit und Geschenk-Freeze

Für jeden finalen Release Candidate werden mindestens festgehalten:

```text
Quellbranch
Quellcommit
Paketname oder eindeutige Kennzeichnung
Erstellungsdatum
erwartete Hauptbestandteile
ausgeschlossene lokale oder generierte Nebendateien
isolierter Prüfort
SHA-256-Prüfsumme
Ergebnis der vollständigen Abnahme
```

Genau das anhand von Commit, Dateiname und Prüfsumme identifizierte Paket, das isoliert geprüft wurde, ist zur Übergabe freigabefähig.

Ein frischer Kontext erhält Ziel, Plan, Grenzen, relevanten Stand, Testergebnisse, Metadatenprüfung und manuelle Abnahmen. Befunde werden klassifiziert als:

```text
RELEASE-BLOCKER
KLEINER SICHERER ABSCHLUSSFIX
NACHFOLGEARBEIT NACH DEM GESCHENK
```

Ein bestätigter Befund ist ein Release-Blocker, wenn er mindestens eine dieser Bedingungen erfüllt:

- der verbindliche Geschenkpfad kann nicht vollständig durchlaufen werden;
- das definierte Geschenkziel wird wesentlich verfehlt oder irreführend dargestellt;
- der kanonische technische Vertrag wird verletzt;
- eine Privacy-, Sicherheits- oder Publikationsgrenze wird verletzt;
- Empfänger erhalten eine materiell falsche oder nicht ausführbare Anleitung;
- das zur Übergabe vorgesehene Paket unterscheidet sich ungeprüft vom akzeptierten Paket.

Danach folgen:

- nur autorisierte Abschlusskorrekturen;
- fokussierte und vollständige Tests;
- neuer Paketbau;
- isolierte Paketprüfung;
- letzter rollengetrennter Empfängerperspektiv-Lauf;
- dokumentierter Release-Checkpoint;
- separate Entscheidung über PR, Merge, Tag oder Veröffentlichung.

## H. Arbeitsfreigaben, Git, Connector und Identität

Vor jeder Änderung wird der Branch geprüft. Verbindlicher Arbeitsbranch ist derzeit:

```text
gift/nexus-01-chamber-archive
```

Lokaler Checkout und Remote-Branch werden nicht parallel divergent bearbeitet. Es wird zuerst synchronisiert und anschließend nur an einem Ort weitergearbeitet.

Eine ausdrückliche Freigabe gilt für ein klar beschriebenes Arbeitspaket. Sie umfasst die üblichen scope-konformen Lese-, Datei-, Connector-, Commit-, Diff- und normalen Synchronisierungsschritte auf dem benannten Arbeitsbranch. Nicht jeder technische Teilschritt benötigt eine neue Einzelbestätigung.

Read-only Prüfungen innerhalb eines vereinbarten Review-Auftrags benötigen ebenfalls keine Einzelbestätigung für jeden Lesezugriff.

Erneute Abstimmung ist erforderlich, wenn:

- der vereinbarte Scope wesentlich erweitert werden müsste;
- Dateien gelöscht, umfangreich verschoben oder strukturell reorganisiert würden;
- Architektur, Imports, Packaging, Sicherheitsgrenzen oder Testorganisation wesentlich betroffen wären;
- ein anderer Branch oder `main` schreibend betroffen wäre;
- Merge, Rebase, Reset, Force, Amend veröffentlichter Arbeit oder Historienumschreibung vorgeschlagen werden;
- Pull Request, Tag, Release oder Veröffentlichung erfolgen sollen;
- ein unerwartetes Risiko einen wesentlich anderen Lösungsweg erfordert.

Ein normaler Fast-forward-Abgleich nach einem freigegebenen Connector-Arbeitspaket gehört zu diesem Paket, muss aber transparent bleiben und darf keine Divergenz oder Konflikte verdecken.

Öffentliche Projektidentität:

```text
Natali / Natali Reise
info@glossai.de
```

Die technische Connector-Identität `eulisiller` ist für Connector-Commits zulässig. Private Berufsidentitäten und deren Kombination mit dem Familiennamen dürfen in öffentlichen Projektdateien, Commits, Commit-Metadaten, Issues, Wiki-Seiten, Tags oder Release-Texten nicht verwendet werden.

## I. Definition of Done für den Geschenksprint

Der Geschenksprint ist erst abgeschlossen, wenn:

- die Geschenkfassung aus frischer Empfängerperspektive startbar ist;
- der vollständige rollengetrennte Geschenkpfad erfolgreich manuell durchlaufen wurde;
- der verbindliche Mindestumfang der Abbruch-, BLOCKED- und Sicherheitsfälle geprüft ist;
- keine bestätigten Release-Blocker offen sind;
- alle release-nahen Anleitungen dem tatsächlichen Verhalten entsprechen;
- Repository-Einstieg, Dokumenthierarchie und release-relevanter Wiki-Kern konsistent sind;
- öffentliche Dateien und relevante Git-Metadaten keine private Identität oder lokale Maschineninformation offenlegen;
- das finale Paket anhand von Branch, Commit, Dateiname und SHA-256 eindeutig identifiziert ist;
- genau dieses Paket neu gebaut und isoliert geprüft wurde;
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

1. Das angenommene Klarstellungspaket in Sprintplan, Workflow und Living Status synchronisieren.
2. Die korrigierten Punkte in einem gezielten frischen Kontext gegenprüfen.
3. Nur verbleibende Widersprüche gemeinsam entscheiden.
4. Eine konkrete Geschenkabschluss-Roadmap aus den vorhandenen manuellen Befunden, der Dokumentationsinventur und der öffentlichen Repository-/Wiki-Perspektive ableiten.
5. Die Roadmap in frischem Kontext prüfen.
6. Erste kleine Arbeitskarten erstellen und als Paket gegenprüfen.
7. Erst danach weitere player-facing, dokumentarische oder repository-bezogene Änderungen umsetzen.