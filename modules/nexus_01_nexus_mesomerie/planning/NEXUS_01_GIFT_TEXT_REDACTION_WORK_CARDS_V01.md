# Nexus 01 Gift Sprint — Arbeitskartenpaket Textredaktion V0.1

## Dokumentstatus

- Version: 0.1
- Status: Entwurf für gezielten Fresh-context Kartenreview
- Arbeitsbranch: `gift/nexus-01-chamber-archive`
- Ausgangsstand: `d898d72`
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
| GP-10 | Gesamtdarstellung | Visuelle Sprache und Divider benötigen Konsistenz. | TEILWEISE ERLEDIGT | Akzeptierte Divider bewahren, sparsam anwenden und im Hauptpfad verifizieren. |

## 3. Unveränderliche Grenzen für alle Karten

- Keine Änderung an den kanonischen Zustands- oder Ergebnisverträgen.
- Keine Vermischung von Same-process- und Stable-source-Resultaten.
- Keine Vermischung von `/results` und Return Opening.
- Keine Discovery, automatische Auswahl, Übertragung, Reparatur oder Regeneration.
- Keine Änderung an Token-, Artifact-, Routing- oder Packaging-Formaten.
- Keine neue Terminal-UI-Abstraktion oder allgemeines Text-/Divider-Framework.
- Keine Erweiterung des Kartenumfangs auf ANSWER, Return, Revisit oder Dokumentation.
- GP-06 ist eine Schutzanforderung: Die kreative Auswahl bleibt inhaltlich erhalten.
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

Weitere Datei nur, wenn der Kartenreview oder die Verifikation einen konkreten, belegten Bedarf zeigt.

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
- GP-01 und der First-Spark-Anteil von GP-10 danach als ERLEDIGT oder weiterhin klar begründet offen markiert.

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
- GP-02.

## Nicht in Scope

- Atrium-Navigation oder Command-Set ändern;
- Statusmodell ändern;
- neue Räume oder Wege;
- allgemeine Dokumentation.

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
- prüfen, ob keine Fähigkeit versprochen wird, die nicht existiert.

## Definition of Done

- GP-02 ist mit minimalen Textänderungen geschlossen oder nachvollziehbar zurückgestellt;
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
- bestehende `/look`, `/help`, `/trace`, `/walkthrough` und `/cancel`-Erklärungen sprachlich, nicht funktional.

## Nicht in Scope

- Commands hinzufügen, entfernen oder umbenennen;
- Cancel-Verhalten ändern;
- Walkthrough-Logik ändern;
- ANSWER-Texte, soweit sie nicht aus gemeinsam genutzter Formulierung zwingend mitbetroffen sind; gemeinsame Texte dürfen nicht unbeabsichtigt verschlechtert werden.

## Voraussichtlich betroffene Dateien

- `atrium/resonance_mode.py`
- `chambers/resonance/terminal_io.py`
- eventuell eng zugehörige Tests dieser Ausgaben.

## Tests

- fokussierte Tests für PRE_RUN/Hilfe und Informationskommandos;
- prüfen, dass Commands unverändert erkannt werden;
- `git diff --check`.

## Manuelle Prüfung

- Resonance neutral betreten;
- Hilfe vor produktiver Handlung aufrufen;
- `/look`, `/trace` und `/walkthrough` stichprobenartig prüfen;
- sicherstellen, dass die Sprache nicht behauptet, es sei bereits etwas erzeugt worden.

## Definition of Done

- GP-03 und GP-04 geschlossen;
- Einstieg ist kürzer und verständlicher;
- Sicherheits- und Command-Information vollständig korrekt;
- keine funktionale Verhaltensänderung.

## Abbruchkriterium

Wenn eine Textänderung unterschiedliche COMPOSE-/ANSWER-Zustände nicht mehr korrekt abbilden kann, Karte stoppen und gemeinsamen Textbestand separat analysieren.

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
- Textdichte, Reihenfolge und Zwischenüberschriften;
- sparsame Verwendung vorhandener Divider;
- player-facing Labels und Review-Sätze.

## Nicht in Scope

- Choice Catalog oder Kompatibilitätsregeln ändern;
- Anzahl oder Inhalt der kreativen Optionen neu gestalten, außer ein einzelnes Label ist nachweislich unverständlich;
- Datenmodell oder Tokenbau ändern;
- neue Bestätigungsschritte oder Commands;
- ANSWER.

## Voraussichtlich betroffene Dateien

Read-only zuerst eingrenzen:

- `chambers/resonance/terminal_io.py`
- `chambers/resonance/choices.py`
- `chambers/resonance/compose.py` nur, falls dort tatsächlich player-facing Text liegt;
- `atrium/resonance_mode.py` für rahmende COMPOSE-Ausgaben;
- passende fokussierte Tests.

## Tests

- bestehende COMPOSE-Flow- und Terminaltests;
- Auswahlreihenfolge und Rückgabewerte unverändert;
- keine internen IDs in player-facing Ausgabe;
- `git diff --check`.

## Manuelle Prüfung

- vollständiger COMPOSE-Durchlauf;
- prüfen, ob vor der ersten Wahl schnell verständlich ist, was geschieht;
- prüfen, ob jede Wahl genug Raum erhält;
- prüfen, ob Review verständlich ist, ohne technisch zu klingen;
- prüfen, ob GP-06 weiterhin klar erfüllt ist.

## Definition of Done

- GP-05 und GP-07 geschlossen;
- GP-06 nach manueller Prüfung weiterhin positiv bestätigt;
- Auswahlmechanik und Ergebnis unverändert;
- Textfluss ist kürzer, nicht ärmer.

## Abbruchkriterium

Wenn die Redaktion Änderungen an Katalog, Auswahlmechanik, Token oder Chamber-Grammatik verlangt, Karte stoppen.

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
- Same-process- und Stable-source-Bezeichnungen verständlich darstellen, ohne sie fachlich zu vermischen.

## Nicht in Scope

- Resultmodell ändern;
- Return Opening in `/results` integrieren;
- automatische Dateisuche oder Auswahl;
- Speicherorte, Formate oder Artefakte ändern;
- ANSWER-/Return-Abschluss.

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
- prüfen, ob Wiederholungen reduziert wurden, ohne Privacy-Aussagen zu verlieren.

## Definition of Done

- GP-08 und GP-09 geschlossen;
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

Vor Umsetzung:

1. gezielter Fresh-context Review dieses vollständigen Kartenpakets;
2. gemeinsame Entscheidung über Reviewbefunde;
3. ausdrückliche Annahme des umsetzungsreifen Kartenpakets.

Für jede Karte danach:

```text
Branch und Synchronisierung prüfen
-> genaue Fundstellen read-only bestätigen
-> kleinste Textänderung umsetzen
-> Diff prüfen
-> fokussierte Tests
-> kurzer manueller Test
-> acceptance or revision
```

## 6. Reviewauftrag für dieses Kartenpaket

Der Kartenreview soll ausschließlich prüfen:

- Sind GP-01 bis GP-10 korrekt und ohne Doppelarbeit zugeordnet?
- Ist bereits Erledigtes als Verifikation statt Neuimplementierung behandelt?
- Sind die fünf Karten klein und voneinander ausreichend getrennt?
- Sind betroffene Dateien nur als zu bestätigende Kandidaten benannt, wo die Fundstelle noch nicht abschließend belegt ist?
- Schützen die Karten GP-06 sowie alle technischen und Privacy-Grenzen?
- Greift eine Karte unzulässig auf ANSWER, Return, Revisit, Dokumentation oder Paketierung über?
- Sind Tests, manuelle Prüfung, Definition of Done und Abbruchkriterien konkret genug?

Der Review autorisiert keine Umsetzung.
