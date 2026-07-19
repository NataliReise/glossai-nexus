# Nexus 01 Gift Sprint — Arbeitskartenpaket Textredaktion V0.1

## Dokumentstatus

- Version: 0.1
- Status: Nach gezieltem Fresh-context Kartenreview angenommen
- Arbeitsbranch: `gift/nexus-01-chamber-archive`
- Ausgangsstand: `d898d72`
- Review-Korrekturstand: `c956239`
- Übergeordnete Roadmap: `NEXUS_01_GIFT_CLOSEOUT_ROADMAP_V01.md`
- Zweck: Erstes begrenztes Arbeitskartenpaket für die bereits begonnene player-facing Text- und Darstellungsredaktion.

## 1. Scope dieses Kartenpakets

Dieses Paket setzt ausschließlich die bereits begonnene Redaktion im player-facing Hauptpfad fort.

Enthalten sind:

- First-Spark-Abschluss und Verifikation der bereits umgesetzten Darstellung;
- Atrium-Status und Orientierung;
- Resonance PRE_RUN und Hilfe;
- COMPOSE-Einstieg, Auswahl, Review und Abschluss;
- POST_RUN und `/results`;
- sparsame, konsistente Verwendung der bereits akzeptierten Divider-Sprache.

Ausdrücklich nicht enthalten sind:

- ANSWER;
- Return Artifact;
- Return Opening;
- Stable-result Revisit;
- BLOCKED und vollständige Negativpfade;
- Dokumentations-, Repository- oder Wiki-Konsolidierung;
- Paketierung oder Release Candidate;
- neue Commands, neue Zustände, neue Mechanik oder neue Architektur.

## 2. Konsolidierter Stand GP-01 bis GP-10

| ID | Bereich | Befund | Status für dieses Paket | Entscheidung |
|---|---|---|---|---|
| GP-01 | First Spark | `/unlock` benötigt mehr Weißraum und Prominenz. | TEILWEISE ERLEDIGT | Bereits umgesetzte Abschlussdarstellung manuell verifizieren; nur bei bestätigtem Restproblem nacharbeiten. |
| GP-02 | Atrium | Statussprache wirkt zu technisch. | OFFEN | In Karte TR-02 sprachlich prüfen und bei kleinem Risiko präzisieren. |
| GP-03 | Resonance PRE_RUN | „productive“ erscheint doppelt beziehungsweise intern. | OFFEN | In Karte TR-03 bereinigen. |
| GP-04 | Resonance-Hilfe | „originating cycle“ wirkt technisch. | OFFEN | In Karte TR-03 verständlicher formulieren, ohne die technische Bedeutung zu verändern. |
| GP-05 | COMPOSE | Einführung ist zu dicht. | OFFEN | In Karte TR-04 entzerren und priorisieren. |
| GP-06 | COMPOSE-Auswahl | Kreative Auswahl wurde positiv erlebt. | ZU BEWAHREN | Keine inhaltliche Vereinfachung, die Wahlfreiheit oder Atmosphäre schwächt. |
| GP-07 | COMPOSE-Review | Review-Formulierung wirkt technisch. | OFFEN | In Karte TR-04 player-facing präzisieren. |
| GP-08 | POST_RUN | Abschluss wiederholt sich. | OFFEN | In Karte TR-05 straffen. |
| GP-09 | `/results` | Ergebnislabels wirken diagnostisch. | OFFEN | In Karte TR-05 sprachlich enttechnisieren, ohne Ergebnisarten zu vermischen. |
| GP-10 | Gesamtdarstellung | Visuelle Sprache und Divider benötigen Konsistenz. | TEILWEISE ERLEDIGT | First-Spark-Anteil in TR-01 verifizieren; verbleibenden Hauptpfadanteil als querschnittliche Prüfanforderung in TR-02 bis TR-05 berücksichtigen. |

## 3. Unveränderliche Grenzen für alle Karten

- Keine Änderung an den kanonischen Zustands- oder Ergebnisverträgen.
- Keine Vermischung von Same-process- und Stable-source-Resultaten.
- Keine Vermischung von `/results` und Return Opening.
- Keine Discovery, automatische Auswahl, Übertragung, Reparatur oder Regeneration.
- Keine Änderung an Token-, Artifact-, Routing- oder Packaging-Formaten.
- Keine neue Terminal-UI-Abstraktion oder allgemeines Text-/Divider-Framework.
- Keine Erweiterung des Kartenumfangs auf ANSWER, Return, Revisit oder Dokumentation.
- GP-06 ist eine Schutzanforderung: Die kreative Auswahl bleibt inhaltlich erhalten.
- Der verbleibende Hauptpfadanteil von GP-10 ist eine querschnittliche Prüfanforderung für TR-02 bis TR-05. Er erlaubt ausschließlich die sparsame und kontextgerechte Verwendung der bereits akzeptierten Divider-Palette. Neue Divider-Typen, eine flächige Umgestaltung oder eine eigenständige Divider-Redaktion sind nicht Teil dieses Kartenpakets.
- Ein positiver fokussierter Test ersetzt keine spätere kanonische Vollsuite.

## 4. Akzeptierte Divider-Palette

Die bereits angenommene Palette bleibt die einzige Grundlage:

```text
PERSONAL
︵‿︵‿୨ ☾𓋹☽ ୧‿︵‿︵

THRESHOLD
· · ────── ⟡ · ✦ · ⟡ ────── · ·

SOFT SECTION
· · ────── ꒰ ✦ ꒱ ────── · ·

TECHNICAL SECTION
┈┈┈✧┈┈┈◈┈┈┈✧┈┈┈
```

Regel: Divider nur dort einsetzen, wo sie eine echte semantische Schwelle oder Orientierung tragen. Keine dekorative Häufung.

---

# Arbeitskarte TR-01 — First-Spark-Abschluss verifizieren

## Ausgangslage

Die First-Spark-Abschlussdarstellung wurde bereits überarbeitet und fokussiert getestet. GP-01 und ein Teil von GP-10 sind daher nicht erneut als offene Umsetzung zu behandeln.

## Spielerproblem

Es ist noch nicht manuell aus frischer Empfängerperspektive bestätigt, dass `/unlock` nun ausreichend sichtbar ist und die neue Divider-Struktur im tatsächlichen Terminalfluss ruhig und verständlich wirkt.

## Gewünschtes Ergebnis

Die bestehende Änderung wird aus frischer Empfängerperspektive verifiziert. Nur ein bestätigtes Restproblem führt zu einer minimalen Nacharbeit.

## In Scope

- aktueller First-Spark-Abschluss;
- Sichtbarkeit und Weißraum um `/unlock`;
- Wirkung der PERSONAL-, SOFT-SECTION- und TECHNICAL-SECTION-Divider;
- Terminaldarstellung im realen Ablauf.

## Nicht in Scope

- Neuschreiben des First Spark;
- neue Divider;
- Änderung an Unlock-Logik, Status oder Persistenz;
- neue Tests ohne bestätigten Bedarf.

## Voraussichtlich betroffene Dateien

Primär zur Verifikation:

- `first_spark/first_spark/game_modules/ending.py`
- `first_spark/tests/test_first_spark_flow.py`

Weitere Datei nur, wenn die Verifikation einen konkreten, belegten Bedarf zeigt.

## Tests

- vorhandenen fokussierten First-Spark-Test erneut ausführen, falls eine Änderung erfolgt;
- `git diff --check` für eine Änderung;
- ohne Änderung genügt die dokumentierte manuelle Verifikation.

## Manuelle Prüfung

- frischer First-Spark-Durchlauf;
- Abschluss vollständig lesen, ohne internes Projektwissen;
- prüfen, ob `/unlock` sofort als nächster freiwilliger Schritt erkennbar ist;
- prüfen, ob Divider lesbar, nicht überladen und terminalstabil erscheinen.

## Definition of Done

- entweder bestehende Darstellung ausdrücklich angenommen;
- oder ein eng begrenzter Restfix umgesetzt, fokussiert getestet und manuell angenommen;
- GP-01 und der First-Spark-Anteil von GP-10 danach als `ERLEDIGT` markiert;
- falls ein bestätigter Restbefund nicht innerhalb dieser Karte klein lösbar ist, Status `VERIFIZIERT — RESTBEFUND OFFEN` mit Begründung und ohne falsche Schließung.

## Abbruchkriterium

Sobald eine Lösung neue Mechanik, neue Divider-Sprache oder größere First-Spark-Redaktion erfordern würde, Karte stoppen und neu abstimmen.

---

# Arbeitskarte TR-02 — Atrium-Status und Orientierung enttechnisieren

## Ausgangslage

Der erste Empfängerlauf zeigte, dass einzelne Atrium-Statusformulierungen zu technisch wirken. Die vorhandene Funktion und Orientierung sind grundsätzlich tragfähig.

## Spielerproblem

Interne Zustands- oder Implementierungssprache kann die atmosphärische Orientierung stören und den Eindruck erwecken, die spielende Person müsse technische Modelle verstehen.

## Gewünschtes Ergebnis

Status und unmittelbare Resonance-Orientierung sind verständlich, ehrlich und knapp, ohne technische Details zu verstecken, die für eine sichere Entscheidung nötig sind.

## In Scope

- player-facing Atrium-Statuszeilen;
- kurze Orientierung zum verfügbaren Resonance-Weg;
- Begriffe, die unmittelbar im normalen Hauptpfad erscheinen;
- GP-02;
- GP-10 ausschließlich als querschnittliche Prüfung der vorhandenen Divider-Sprache.

## Nicht in Scope

- Atrium-Navigation oder Command-Set ändern;
- Statusmodell ändern;
- neue Räume oder Wege;
- allgemeine Dokumentation;
- eigenständige Divider-Redaktion.

## Voraussichtlich betroffene Dateien

Read-only zuerst prüfen, dann minimal eingrenzen:

- `atrium/resonance_mode.py`
- `atrium/resonance_terminal.py`
- weitere zentrale Atrium-Datei nur bei eindeutigem Textfund.

## Tests

- bestehende fokussierte Atrium-/Resonance-Tests für tatsächlich geänderte Ausgabe;
- gegebenenfalls gezielte Erwartungsanpassung statt breiter Snapshot-Neuschreibung;
- `git diff --check`.

## Manuelle Prüfung

- Atrium nach First Spark betreten;
- Status und Resonance-Orientierung laut beziehungsweise am Stück lesen;
- prüfen, ob der nächste mögliche Schritt erkennbar ist;
- prüfen, ob keine Fähigkeit versprochen wird, die nicht existiert;
- GP-10 querschnittlich prüfen, ohne zusätzliche Divider-Redaktion zu eröffnen.

## Definition of Done

- GP-02 ist mit minimalen Textänderungen geschlossen oder nachvollziehbar zurückgestellt;
- GP-10 für diesen Abschnitt geprüft;
- keine funktionale Änderung;
- vorhandene Wege und Sicherheitsgrenzen bleiben korrekt beschrieben.

## Abbruchkriterium

Wenn die gewünschte Klarheit nur durch neue Statuslogik, Commands oder Navigation erreichbar scheint, Karte stoppen.

---

# Arbeitskarte TR-03 — Resonance PRE_RUN und Hilfe präzisieren

## Ausgangslage

GP-03 und GP-04 betreffen doppelte beziehungsweise technisch klingende Sprache vor dem produktiven Eintritt und in der Hilfe. Die Chamber-Kommandos und Sicherheitsgrenzen sind bereits implementiert.

## Spielerproblem

Begriffe wie „productive“ oder „originating cycle“ können unnötig intern wirken. Wiederholung verdichtet den Einstieg, statt Sicherheit zu schaffen.

## Gewünschtes Ergebnis

PRE_RUN und Hilfe erklären knapp:

- dass noch nichts erzeugt wurde;
- wie eine bewusste COMPOSE-Handlung beginnt;
- welche Informationskommandos verfügbar sind;
- dass `/cancel` sicher beendet, wo es unterstützt wird;
- ohne interne Zyklus- oder Produktivsprache.

## In Scope

- GP-03;
- GP-04;
- PRE_RUN-Übergang zur Chamber;
- unmittelbar zugehörige `/help`-Texte;
- bestehende `/look`, `/help`, `/trace`, `/walkthrough` und `/cancel`-Erklärungen sprachlich, nicht funktional;
- GP-10 ausschließlich als querschnittliche Prüfung der vorhandenen Divider-Sprache.

## Nicht in Scope

- Commands hinzufügen, entfernen oder umbenennen;
- Cancel-Verhalten ändern;
- Walkthrough-Logik ändern;
- eigenständige ANSWER-Redaktion;
- eigenständige Divider-Redaktion.

Eine gemeinsam von COMPOSE und ANSWER genutzte Fundstelle darf nur geändert werden, wenn die Änderung für ANSWER semantisch neutral bleibt. Die vorhandene ANSWER-Ausgabe wird in diesem Zusammenhang ausschließlich regressiv auf unbeabsichtigte Verschlechterungen geprüft. Das erfordert keinen vollständigen ANSWER-Durchlauf.

## Voraussichtlich betroffene Dateien

- `atrium/resonance_mode.py`
- `chambers/resonance/terminal_io.py`
- eventuell eng zugehörige Tests dieser Ausgaben.

## Tests

- fokussierte Tests für PRE_RUN/Hilfe und Informationskommandos;
- prüfen, dass Commands unverändert erkannt werden;
- bei gemeinsam genutzter Fundstelle regressiv prüfen, dass ANSWER semantisch unverändert bleibt;
- `git diff --check`.

## Manuelle Prüfung

- Resonance neutral betreten;
- Hilfe vor produktiver Handlung aufrufen;
- `/look`, `/trace` und `/walkthrough` stichprobenartig prüfen;
- sicherstellen, dass die Sprache nicht behauptet, es sei bereits etwas erzeugt worden;
- GP-10 querschnittlich prüfen, ohne zusätzliche Divider-Redaktion zu eröffnen.

## Definition of Done

- GP-03 und GP-04 geschlossen;
- GP-10 für diesen Abschnitt geprüft;
- Einstieg ist kürzer und verständlicher;
- Sicherheits- und Command-Information vollständig korrekt;
- keine funktionale Verhaltensänderung;
- keine eigenständige ANSWER-Redaktion.

## Abbruchkriterium

Karte stoppen, sobald eine sinnvolle COMPOSE-Verbesserung eine eigenständige ANSWER-Formulierung, Verzweigung oder Zustandsunterscheidung erfordern würde oder ein gemeinsamer Textbestand unterschiedliche COMPOSE-/ANSWER-Zustände nicht korrekt abbilden kann.

---

# Arbeitskarte TR-04 — COMPOSE-Einstieg, Auswahl und Review entzerren

## Ausgangslage

Der COMPOSE-Pfad wurde erfolgreich durchlaufen. GP-05 und GP-07 betreffen Dichte und technische Review-Sprache. GP-06 schützt ausdrücklich die positiv erlebte kreative Auswahl.

## Spielerproblem

Zu viel Erklärung vor der ersten Wahl und technisch klingende Review-Texte können die kreative Handlung bremsen. Gleichzeitig darf die sichere, bewusste Entscheidung nicht verunklart werden.

## Gewünschtes Ergebnis

COMPOSE führt in ruhigen, klar getrennten Schritten durch:

- kurze Einladung;
- Bild;
- Duft;
- Bewegung;
- Wunschwort;
- verständliche Zusammenfassung beziehungsweise Bestätigung;

wobei die bestehende Wahlvielfalt und poetische Offenheit erhalten bleiben.

## In Scope

- GP-05;
- GP-06 als Schutzanforderung;
- GP-07;
- Textdichte, Zwischenüberschriften sowie Reihenfolge und Gliederung der player-facing Erklärungselemente innerhalb der bestehenden Schritte;
- sparsame Verwendung vorhandener Divider;
- player-facing Labels und Review-Sätze;
- GP-10 ausschließlich als querschnittliche Prüfung der vorhandenen Divider-Sprache.

Die mechanische Schrittfolge `image -> scent -> movement -> wish_word -> review` sowie Auswahlreihenfolge, Rückgabewerte und Zustandsübergänge bleiben unverändert.

## Nicht in Scope

- Choice Catalog oder Kompatibilitätsregeln ändern;
- Anzahl oder Inhalt der kreativen Optionen neu gestalten, außer ein einzelnes Label ist nachweislich unverständlich;
- Datenmodell oder Tokenbau ändern;
- neue Bestätigungsschritte oder Commands;
- ANSWER;
- eigenständige Divider-Redaktion.

## Voraussichtlich betroffene Dateien

Read-only zuerst eingrenzen:

- `chambers/resonance/terminal_io.py`
- `chambers/resonance/choices.py`
- `chambers/resonance/compose.py` nur, falls dort tatsächlich player-facing Text liegt;
- `atrium/resonance_mode.py` für rahmende COMPOSE-Ausgaben;
- passende fokussierte Tests.

## Tests

- bestehende COMPOSE-Flow- und Terminaltests;
- mechanische Schritt- und Auswahlreihenfolge sowie Rückgabewerte unverändert;
- keine internen IDs in player-facing Ausgabe;
- `git diff --check`.

## Manuelle Prüfung

- vollständiger COMPOSE-Durchlauf;
- prüfen, ob vor der ersten Wahl schnell verständlich ist, was geschieht;
- prüfen, ob jede Wahl genug Raum erhält;
- prüfen, ob Review verständlich ist, ohne technisch zu klingen;
- prüfen, ob GP-06 weiterhin klar erfüllt ist;
- GP-10 querschnittlich prüfen, ohne zusätzliche Divider-Redaktion zu eröffnen.

## Definition of Done

- GP-05 und GP-07 geschlossen;
- GP-06 nach manueller Prüfung weiterhin positiv bestätigt;
- GP-10 für diesen Abschnitt geprüft;
- Auswahlmechanik, Schrittfolge und Ergebnis unverändert;
- Textfluss ist kürzer, nicht ärmer.

## Abbruchkriterium

Wenn die Redaktion Änderungen an Katalog, Auswahlmechanik, mechanischer Schrittfolge, Token oder Chamber-Grammatik verlangt, Karte stoppen.

---

# Arbeitskarte TR-05 — POST_RUN und `/results` straffen

## Ausgangslage

Der erste COMPOSE-Lauf endete technisch erfolgreich. GP-08 betrifft wiederholte Abschlussaussagen; GP-09 diagnostisch klingende Ergebnislabels.

## Spielerproblem

Mehrfache Hinweise auf Abschluss, Lokalität oder Nichtübertragung können den Nachklang überfrachten. Diagnostische Labels lassen ein kreatives Ergebnis wie einen Systembericht erscheinen.

## Gewünschtes Ergebnis

Nach COMPOSE ist klar und ruhig erkennbar:

- die Handlung ist abgeschlossen;
- welche lokalen Ausgaben entstanden sind;
- was freiwillig weitergegeben werden kann;
- was privat bleibt;
- was `/results` zeigt und was es ausdrücklich nicht zeigt.

## In Scope

- GP-08;
- GP-09;
- POST_RUN-Ausgaben des COMPOSE-Hauptpfads;
- `/results`-Überschriften und player-facing Labels;
- Wiederholungen reduzieren;
- Same-process- und Stable-source-Bezeichnungen verständlich darstellen, ohne sie fachlich zu vermischen;
- GP-10 ausschließlich als querschnittliche Prüfung der vorhandenen Divider-Sprache.

## Nicht in Scope

- Resultmodell ändern;
- Return Opening in `/results` integrieren;
- automatische Dateisuche oder Auswahl;
- Speicherorte, Formate oder Artefakte ändern;
- ANSWER-/Return-Abschluss;
- eigenständige Divider-Redaktion.

## Voraussichtlich betroffene Dateien

Read-only zuerst lokalisieren:

- `atrium/resonance_mode.py`
- zentrale `/results`-Darstellung im Atrium;
- gegebenenfalls zugehöriger Result-Renderer;
- passende fokussierte Tests.

## Tests

- fokussierte POST_RUN- und `/results`-Tests;
- Same-process-Vorrang bleibt unverändert;
- Stable-source-Resultat bleibt getrennt;
- keine Return-Opening-Funktion in `/results`;
- `git diff --check`.

## Manuelle Prüfung

- COMPOSE abschließen;
- Abschlussausgabe vollständig lesen;
- `/results` im selben Prozess aufrufen;
- prüfen, ob Ergebnisarten verständlich, aber nicht diagnostisch benannt sind;
- prüfen, ob Wiederholungen reduziert wurden, ohne Privacy-Aussagen zu verlieren;
- GP-10 querschnittlich prüfen, ohne zusätzliche Divider-Redaktion zu eröffnen.

## Definition of Done

- GP-08 und GP-09 geschlossen;
- GP-10 für diesen Abschnitt geprüft;
- POST_RUN wirkt ruhig und eindeutig;
- `/results` bleibt technisch ehrlich und funktional unverändert;
- keine Vermischung mit Return Opening oder Stable-result Revisit.

## Abbruchkriterium

Wenn verständliche Labels nur durch Änderung der Resulttypen oder ihrer Prioritätslogik möglich erscheinen, Karte stoppen.

---

## 5. Reihenfolge und Gates

Vorgesehene Reihenfolge:

```text
TR-01 First-Spark-Verifikation
-> TR-02 Atrium
-> TR-03 PRE_RUN und Hilfe
-> TR-04 COMPOSE
-> TR-05 POST_RUN und /results
```

TR-02 bis TR-05 dürfen bei eindeutig getrennten Dateien redaktionell vorbereitet werden, werden aber einzeln umgesetzt, geprüft und angenommen.

Der gezielte Fresh-context Review wurde durchgeführt, seine vier kleinen Klarstellungen wurden gemeinsam angenommen und in diese Fassung eingearbeitet. Das Kartenpaket ist damit für den Einzelkartenzyklus angenommen.

Vor jeder Änderung werden die exakten Produktionsfundstellen sowie die vorhandenen betroffenen Testdateien und Testfälle read-only benannt und im Arbeitsprotokoll der Karte festgehalten. Erst danach wird der tatsächliche Änderungsumfang innerhalb der bereits angenommenen Karte festgelegt. Diese Benennung dient der Scope-Kontrolle und erfordert keine zusätzliche strategische Freigabe, solange keine neue Datei, Funktion oder technische Grenze hinzukommt.

Für jede Karte:

```text
Branch und Synchronisierung prüfen
-> exakte Produktions- und Testfundstellen read-only benennen
-> tatsächlichen Umfang innerhalb der Karte festlegen
-> kleinste Textänderung umsetzen
-> Diff prüfen
-> fokussierte Tests
-> kurzer manueller Test
-> acceptance or revision
```

## 6. Reviewabschluss

Der gezielte Fresh-context Kartenreview bestätigte:

- keine Karten-Blocker;
- fünf tragfähige, ausreichend kleine Karten;
- korrekte Behandlung der bereits umgesetzten First-Spark-Arbeit als Verifikation;
- Schutz von GP-06;
- keine neue Scope- oder Architekturöffnung;
- Umsetzungsreife nach den eingearbeiteten Klarstellungen.

Die vier geschlossenen Klarstellungen betreffen:

1. querschnittliche Restzuordnung von GP-10 zu TR-02 bis TR-05;
2. eindeutige Trennung zwischen textlicher Gliederung und mechanischer Schrittfolge in TR-04;
3. semantisch neutrale Behandlung gemeinsam genutzter COMPOSE-/ANSWER-Fundstellen in TR-03;
4. Benennung exakter Produktions- und Testfundstellen vor jeder Änderung.

Zusätzlich gilt für TR-01 der präzise Status `VERIFIZIERT — RESTBEFUND OFFEN`, falls ein bestätigtes Problem nicht innerhalb der Karte klein lösbar ist.

Der Reviewabschluss autorisiert die kleinteilige Umsetzung ab TR-01 innerhalb der festgelegten Karten- und Freigabegrenzen.