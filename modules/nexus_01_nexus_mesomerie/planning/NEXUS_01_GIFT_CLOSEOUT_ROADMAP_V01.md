# Nexus 01 Geschenkabschluss-Roadmap V0.1

## Dokumentstatus

- Version: 0.1
- Status: Entwurf zur gemeinsamen Annahme
- Ausgangscheckpoint: `193419f`
- Arbeitsbranch: `gift/nexus-01-chamber-archive`
- Zweck: Kontrollierter Abschluss der Geschenkfassung von Nexus 01 auf Basis der bereits abgeschlossenen technischen Slices, des ersten Empfänger-/COMPOSE-Durchlaufs und der begonnenen sprachlichen Redaktion.

## 1. Ziel der Roadmap

Diese Roadmap führt den vorhandenen Zwischenstand zu einer stabilen, verständlichen, atmosphärisch stimmigen und eindeutig identifizierten Geschenkfassung.

Sie beginnt ausdrücklich **nicht** bei null.

Bereits vorhanden sind:

- die abgeschlossenen technischen Hauptslices bis einschließlich Stable-result Revisit;
- die kanonische technische Baseline mit 408/408 Tests am Checkpoint `59c6595`;
- ein erfolgreicher erster Lauf aus Empfängerperspektive bis COMPOSE und `/results`;
- die dokumentierten Befunde GP-01 bis GP-10;
- eine erste umgesetzte redaktionelle Verbesserung am First-Spark-Abschluss;
- ein fokussierter bestandener First-Spark-Test;
- der aktuelle Sprintplan V0.4;
- der Collaboration Workflow V0.1;
- der synchronisierte Living Status;
- ein unabhängiger Planreview und ein gezielter Recheck.

Die Roadmap wiederholt daher weder die abgeschlossenen technischen Slices noch den bereits durchgeführten ersten Empfängerlauf. Sie konsolidiert deren Ergebnisse, schließt offene redaktionelle und dokumentarische Arbeiten ab und ergänzt die noch fehlenden Release-Prüfungen.

## 2. Verbindliche Grenzen

Für alle Roadmap-Phasen gilt:

- keine neue Architektur;
- kein neues allgemeines Command-, Result- oder Persistence-Framework;
- keine automatische Discovery privater Dateien, Tokens, Artefakte oder Resultate;
- keine automatische Übertragung, Reparatur, Regeneration oder Veröffentlichung;
- keine Historienumschreibung aus kosmetischen Gründen;
- keine technische Reorganisation des Repositories ohne belegten Releasebedarf;
- keine stillschweigende Erweiterung des Geschenksprints;
- keine Gleichsetzung eines fokussierten Tests mit einer vollständigen Suite;
- keine Gleichsetzung eines ersten Happy Paths mit finaler Release-Abnahme.

Neue Ideen werden genau einer Kategorie zugeordnet:

```text
notwendige Releasekorrektur
kleine sichere Verbesserung
Nachfolgearbeit nach dem Geschenk
bewusst nicht weiterverfolgen
```

## 3. Phase 0 — Bereits abgeschlossener Vorlauf

**Status:** abgeschlossen

Enthalten:

```text
technische Hauptslices abgeschlossen
-> kanonische Suite 408/408 am technischen Baseline-Checkpoint
-> erster frischer Empfänger-/COMPOSE-Durchlauf
-> GP-01 bis GP-10 dokumentiert
-> First-Spark-Abschlussdarstellung überarbeitet
-> fokussierter First-Spark-Test bestanden
-> Planungs- und Workflowdokumente aktualisiert
-> Fresh-context Review durchgeführt
-> Korrekturpaket eingearbeitet
-> gezielter Recheck abgeschlossen
```

Dieser Vorlauf ist anerkannter Projektbestand und wird nicht erneut als offene Arbeit geplant.

Noch nicht damit belegt sind insbesondere:

- vollständiger ANSWER-Pfad;
- bewusster Return;
- Return Opening;
- Stable-result Revisit im vollständigen Rollenlauf;
- BLOCKED;
- alle verbindlichen Abbruch- und Fehlerpfade;
- vollständige Dokumentationskonsistenz;
- Repository- und Wiki-Abschluss;
- isolierte Prüfung des finalen Geschenkpakets.

## 4. Phase 1 — Vorhandene Befunde konsolidieren

Ziel dieser Phase ist ein belastbarer Überblick über bereits erledigte, teilweise erledigte und noch offene Punkte.

Grundlage sind:

- GP-01 bis GP-10;
- bereits umgesetzte First-Spark-Änderungen;
- frühere technische und manuelle Befunde;
- bekannte Textkandidaten;
- bekannte Dokumentationsdrift;
- bereits angenommene Planungsentscheidungen.

Jeder Befund erhält:

```text
ID
Bereich
Beobachtung
Status
Priorität
Art
kleinste sinnvolle Maßnahme
betroffene Dateien
notwendige Verifikation
```

Zulässige Statuswerte:

```text
ERLEDIGT
TEILWEISE ERLEDIGT
OFFEN
MUSS NOCH VERIFIZIERT WERDEN
SPÄTER
```

Zulässige Prioritäten:

```text
MUSS
SOLLTE
SPÄTER
```

Zulässige Befundarten:

```text
Sprache
Darstellung
Zustandsmismatch
technischer Defekt
Dokumentationsdrift
Repository-Navigation
Wiki-Drift
Paketierungsrisiko
```

Beispiel:

```text
ID: GP-01
Bereich: First Spark
Beobachtung: /unlock war im Abschluss nicht deutlich genug hervorgehoben.
Status: TEILWEISE ERLEDIGT
Maßnahme: Layout bereits verbessert.
Noch erforderlich: erneuter manueller Empfängertest.
```

**Gate:** Alle bereits bekannten Befunde sind eindeutig eingeordnet. Kein bereits erledigter Punkt wird unbemerkt erneut geplant.

## 5. Phase 2 — Gezielte Restinventur

Die Restinventur konzentriert sich auf noch nicht ausreichend geprüfte Bereiche.

### 2A — Noch offene Spielerstrecke

Vertieft zu prüfen:

```text
ANSWER
Return Artifact
bewusste Rückgabe
Return Opening
Stable-result Revisit
BLOCKED
COMPOSE-Abbruch
ANSWER-Abbruch
fehlende Known Source
ungültige Known Source
null Return-Kandidaten
mehrere Return-Kandidaten
wiederholtes Opening
zweiter unabhängiger COMPOSE-Zyklus
```

First Spark, Atrium, COMPOSE und `/results` werden nicht vollständig neu inventarisiert. Dort werden nur:

- offene GP-Befunde geprüft;
- bereits geänderte Stellen verifiziert;
- neu erkennbare Widersprüche erfasst.

### 2B — Dokumentationsinventur

Zu erfassen sind insbesondere:

- Root-README;
- Nexus-01-README;
- Quick Start;
- Linux-Einstieg;
- Playing-a-Nexus-Anleitung;
- Gift Instructions;
- Activation-, Carrier-, Return- und Opening-Anleitungen;
- Konzept- und Architekturdokumente;
- aktuelle und historische Planungsdokumente;
- Statusdokumente;
- Links und Navigationspfade.

Klassifikation:

```text
KANONISCH AKTUELL
HISTORISCH
ARBEITSNOTIZ
DUPLIKAT ODER DRIFT
SPÄTER
```

### 2C — Öffentliches Repository und Wiki

Zu prüfen sind:

- öffentlicher Einstieg in das Repository;
- sichtbare Verzeichnis- und Dokumentstruktur;
- aktuelle und historische Einstiegspunkte;
- tote oder irreführende Links;
- Superseded-Kennzeichnungen;
- lokale oder generierte Nebendateien;
- `.gitignore`;
- vorhandene Wiki-Seiten;
- Wiki-Startseite;
- Wiki-Navigation;
- Widersprüche zwischen Wiki und Repository;
- erkennbare Unfertigkeit in release-relevanten Wiki-Bereichen.

Die Inventur darf Orientierung und öffentliche Präsentation bewerten, autorisiert aber noch keine Verschiebung, Löschung oder strukturelle Reorganisation.

**Gate:** Der tatsächliche Restumfang ist vollständig genug bekannt, um begrenzte Arbeitspakete zu bilden.

## 6. Phase 3 — Priorisierte Abschlussarbeitspakete

Aus Konsolidierung und Restinventur entstehen vier große Arbeitspakete.

### Paket A — Begonnene sprachliche und visuelle Redaktion abschließen

Enthalten:

- offene GP-Befunde;
- erneute First-Spark-Verifikation;
- Atrium-Statussprache;
- Resonance PRE_RUN;
- COMPOSE-Einstieg;
- Auswahl- und Review-Texte;
- POST_RUN;
- `/results`;
- Wiederholungen;
- diagnostisch oder intern klingende Formulierungen;
- konsistente, sparsame Divider-Verwendung.

Nicht enthalten:

- neue Spielmechanik;
- neue Commands;
- neue Zustandsmodelle;
- neues UI-Framework.

### Paket B — Noch nicht vollständig geprüfte Spiel- und Sicherheitsstrecke

Enthalten:

- ANSWER;
- Return Artifact;
- bewusste Rückgabe;
- Return Opening;
- Stable-result Revisit;
- BLOCKED;
- Abbruchpfade;
- Known-source-Fehlerfälle;
- null und mehrere Return-Kandidaten;
- wiederholtes Opening;
- zweiter unabhängiger COMPOSE-Zyklus;
- Nachweis, dass keine Discovery, automatische Auswahl, Reparatur oder Regeneration erfolgt.

### Paket C — Dokumentation und öffentliche Projektoberfläche

Enthalten:

- Dokumenthierarchie;
- aktualisierte Empfängeranleitung;
- Quick Start;
- Gift Instructions;
- Return Guide;
- README-Konsistenz;
- öffentliche Repository-Navigation;
- historische Kennzeichnungen;
- tote Links;
- irreführende Duplikate;
- release-relevante Wiki-Seiten;
- konsistente Privacy- und Sicherheitsbeschreibung;
- öffentliche Identitätsgrenzen.

Repository-Kuration gehört ausdrücklich zum Geschenkabschluss, weil das Repository Teil des öffentlich begehbaren Nexus-Projektraums ist.

Nicht enthalten:

- technische Repository-Neuarchitektur;
- großflächige Importänderungen;
- Testreorganisation;
- Legacy-Bereinigung ohne Releasebedarf;
- Historienumschreibung.

### Paket D — Paketierung, Gesamtprüfung und Freeze

Enthalten:

- definierter Quellcheckpoint;
- eindeutiger Paketname;
- Erstellungsdatum;
- erwartete Hauptbestandteile;
- ausgeschlossene Nebendateien;
- isolierter Prüfort;
- SHA-256-Prüfsumme;
- vollständiger rollengetrennter Testlauf;
- negativer Mindesttest;
- read-only Metadatenprüfung;
- Release-Audit;
- Geschenk-Freeze.

## 7. Phase 4 — Roadmap-Gegenprüfung

Die vollständige Roadmap wird in frischem Kontext geprüft auf:

- versteckte Abhängigkeiten;
- falsche Reihenfolge;
- doppelte Arbeit;
- fehlende Gates;
- zu große Pakete;
- Scope-Erweiterung;
- versehentliche Architekturarbeit;
- unklare Trennung zwischen Geschenk und Nachfolgeentwicklung;
- Widersprüche zu Sprintplan, Workflow und Living Status.

Jeder Reviewbefund wird entschieden als:

```text
übernehmen
präzisieren
verschieben
bewusst nicht übernehmen
```

**Gate:** Erst nach Annahme der Roadmap dürfen Umsetzungskarten erstellt werden.

## 8. Phase 5 — Arbeitskartenpakete

Die Arbeitspakete werden nicht gleichzeitig vollständig in Karten zerlegt.

Vorgesehene Reihenfolge:

### Kartenpaket 1 — Offene Textredaktion

Aus Paket A:

- First Spark;
- Atrium;
- Resonance PRE_RUN;
- COMPOSE;
- POST_RUN;
- `/results`.

### Kartenpaket 2 — Return- und Sicherheitsstrecke

Aus Paket B:

- ANSWER;
- Return;
- Opening;
- Revisit;
- BLOCKED;
- Negativpfade.

### Kartenpaket 3 — Dokumentation und öffentliche Oberfläche

Aus Paket C:

- Anleitungen;
- Repository-Kuration;
- Wiki-Releasekern.

### Kartenpaket 4 — Paketierung und Freeze

Aus Paket D:

- Releaseprotokoll;
- Rollenlauf;
- Paketidentität;
- Prüfsumme;
- Audit;
- Freeze.

Jede Karte enthält mindestens:

```text
ID und Titel
Ausgangslage
Problem
gewünschtes Ergebnis
In Scope
Nicht in Scope
betroffene Dateien
unveränderliche Grenzen
Tests
manuelle Prüfung
Definition of Done
Abbruchkriterium
```

Jedes fertige Kartenpaket erhält vor der Umsetzung einen eigenen begrenzten Fresh-context Review.

## 9. Phase 6 — Kleinteilige Umsetzung

Für jede angenommene Karte gilt:

```text
Branch und Synchronisierung prüfen
-> genaue Dateien lesen
-> nur Kartenumfang umsetzen
-> Diff prüfen
-> fokussierte Tests
-> kurzer manueller Test
-> akzeptieren oder nacharbeiten
```

Eine Arbeitspaketfreigabe umfasst die üblichen scope-konformen Datei-, Connector- und Commit-Schritte.

Neue Abstimmung ist erforderlich bei:

- Scope-Erweiterung;
- größeren Löschungen oder Verschiebungen;
- struktureller Reorganisation;
- Branchintegration;
- Änderung veröffentlichter Historie;
- Tags;
- Releases;
- Veröffentlichung;
- unerwartetem Risiko;
- wesentlich anderem Lösungsweg.

## 10. Phase 7 — Dokumentations- und Außenperspektivprüfung

Nach Stabilisierung des Spielerlebnisses werden Dokumentation, Repository und Wiki gemeinsam geprüft.

Zu beantworten ist:

- Findet eine neue Person den richtigen Einstieg?
- Sind README, Quick Start, Gift Instructions und Wiki widerspruchsfrei?
- Ist erkennbar, was aktuell, historisch und experimentell ist?
- Werden nur vorhandene Funktionen versprochen?
- Sind Privacy- und Sicherheitsgrenzen korrekt?
- Sind Rollen, Artefakte und Rückgabe verständlich?
- Sind exakte Startbefehle korrekt?
- Sind Links funktionsfähig?
- Enthalten Dateien oder öffentliche Metadaten private Identitäten oder lokale Rechnerdaten?
- Wirkt das öffentliche Projekt vollständig genug, ohne etwas vorzutäuschen?

Der Wiki-Releasekern umfasst mindestens:

- eine glaubwürdige Home-Seite;
- Projekt- und Nexus-01-Orientierung;
- Spielen und Weitertragen;
- Resonance, Return und Revisit;
- Privacy und lokale Kontrolle;
- aktuellen Projektstatus;
- funktionierende Verweise auf kanonische Repository-Dokumente.

Ein vollständiges Glossar, eine lückenlose Projektgeschichte und eine umfassende langfristige Roadmap sind kein zwingendes Release-Gate, sofern bestehende Seiten nicht irreführend sind.

## 11. Phase 8 — Vollständiger rollengetrennter Geschenkpfad

Eine Person darf alle Rollen simulieren, solange Informations- und Dateigrenzen realistisch getrennt bleiben.

```text
Rolle A: gebende / wartende Seite
-> frisches Geschenkpaket
-> Aktivierung
-> First Spark
-> COMPOSE
-> Einladung und privater Return Workspace

Rolle B: empfangende / antwortende Seite
-> nur bewusst übertragene Einladung
-> ANSWER
-> Return Artifact

Rolle A2: zurückkehrende wartende Seite
-> bewusst zurückgegebenes Artifact
-> Return Opening
-> Stable-result Revisit
```

Verbindliche Bedingungen:

- getrennte lokale Bereiche;
- bewusste Kopier- oder Paketierungsschritte;
- keine unbeabsichtigte Wiederverwendung alter Tokens oder Resultate;
- keine Rolle erhält Dateien, die sie im realen Austausch nicht besitzen würde;
- keine Abkürzung über interne Projektverzeichnisse;
- kein gleichzeitiges Redigieren während des Gesamtpfads.

Verbindlicher Negativbogen:

- COMPOSE-Abbruch;
- ANSWER-Abbruch;
- BLOCKED bleibt nichtproduktiv;
- fehlende Known Source;
- ungültige Known Source;
- null Return-Kandidaten;
- mehrere Return-Kandidaten ohne automatische Auswahl;
- wiederholtes Opening ohne Überschreibung;
- zweiter unabhängiger COMPOSE-Zyklus;
- keine Discovery, automatische Reparatur, Regeneration oder Übertragung.

## 12. Phase 9 — Release Candidate und Geschenk-Freeze

Der Release Candidate wird eindeutig dokumentiert:

```text
Quellbranch
Quellcommit
Paketname oder eindeutige Kennzeichnung
Erstellungsdatum
erwartete Hauptbestandteile
ausgeschlossene lokale oder generierte Dateien
isolierter Prüfort
SHA-256-Prüfsumme
vollständiges Prüfergebnis
```

Reihenfolge:

```text
akzeptierter Quellcheckpoint
-> frischer Paketbau
-> Paketinhalt kontrollieren
-> SHA-256 erzeugen
-> isoliert entpacken
-> vollständigen Rollenlauf durchführen
-> Negativbogen prüfen
-> Anleitungen befolgen
-> Repository und Wiki prüfen
-> öffentliche Metadaten read-only prüfen
-> Release-Audit
-> Geschenk-Freeze
```

Nur genau das identifizierte und per Prüfsumme bestätigte Paket, das die isolierte Prüfung bestanden hat, darf übergeben werden.

PR, Merge, Tag, Release oder weitere Veröffentlichung bleiben getrennte Entscheidungen.

## 13. Release-Blocker

Ein Befund ist ein Release-Blocker, wenn er bestätigt mindestens eine dieser Bedingungen erfüllt:

- Der verbindliche Geschenkpfad kann nicht vollständig durchlaufen werden.
- Das Geschenkziel wird wesentlich verfehlt oder irreführend dargestellt.
- Der kanonische technische Vertrag wird verletzt.
- Eine Privacy-, Sicherheits- oder Publikationsgrenze wird verletzt.
- Release-Anleitungen sind materiell falsch oder praktisch nicht ausführbar.
- Das zu übergebende Paket unterscheidet sich vom geprüften Paket.
- Das öffentliche Repository oder Wiki führt Spielende an einer zentralen Stelle wesentlich in die Irre.

Ein kosmetischer Wunsch, eine größere Ordnungsidee oder eine mögliche spätere Architekturverbesserung ist für sich kein Release-Blocker.

## 14. Zentrale Abhängigkeiten

```text
bekannte Befunde konsolidiert
-> gezielte Restinventur

Restinventur abgeschlossen
-> priorisierte Arbeitspakete

Roadmap akzeptiert
-> Arbeitskarten

Kartenpaket geprüft
-> Umsetzung

Spielerlebnis stabil
-> endgültige Anleitungen

Repository-Dokumentation stabil
-> Wiki-Synchronisierung

alle akzeptierten Änderungen abgeschlossen
-> vollständiger Rollenlauf

vollständiger Rollenlauf bestanden
-> Release Candidate

genau identifizierter Candidate isoliert geprüft
-> Geschenk-Freeze
```

## 15. Unmittelbarer nächster Schritt

Der nächste Schritt ist nicht eine neue Vollinventur, sondern:

```text
GP-01 bis GP-10 konsolidieren
-> bereits erledigte First-Spark-Arbeit korrekt markieren
-> offene Textredaktion bestimmen
-> noch ungeprüfte Spielstrecke inventarisieren
-> Dokumentation, Repository und Wiki erfassen
-> daraus die vier Arbeitspakete A bis D endgültig priorisieren
```

Danach folgt der Fresh-context Review dieser Roadmap. Erst anschließend werden die ersten Umsetzungskarten für die bereits begonnene sprachliche Redaktion erstellt.
