# Übergabenotiz: Nexus 01 nach Slice 4A

## Zweck

Diese Notiz übergibt den akzeptierten Stand von `/results` und grenzt die spätere
Frage des Wiederlesens vorhandener Resonanzartefakte nach einem Neustart ab.

Slice 4A und die enge Korrektur 4A.1 sind implementiert, geprüft und manuell
akzeptiert. Slice 4A ist korrekt, bleibt bestehen und darf nicht zurückgerollt
werden. Slice 4B und die neu geplante Slice 5 sind nicht implementiert und nicht
zur Umsetzung freigegeben.

## Repository- und Prüfstand

- Branch: `gift/nexus-01-chamber-archive`
- Ausgangs-HEAD: `b04c3918d61ce28b6e25e766188030a9a2770647`
- Arbeitsbaum: uncommitted
- Index: leer
- Letzter kanonischer Lauf aus der 4A.1-Implementierungs- und Abnahmesequenz:
  363 Tests, 0 Fehler, 0 Errors, 0 übersprungen
- Fokussiert: ANSWER 21 und COMPOSE 22 Tests, jeweils erfolgreich
- Packaging-Regression: 11 Tests, erfolgreich
- `git diff --check`: erfolgreich

Diese Prüfungen wurden vor dieser Dokumentationsübergabe ausgeführt; die
Dokumentationsaufgabe hat sie nicht erneut ausgeführt.

## Akzeptierter Slice-4A-Vertrag

`/results` gehört ausschließlich zu den abgeschlossenen corrected COMPOSE- und
ANSWER-Post-run-Flächen. Während eines produktiven Zyklus ist der Befehl nicht
verfügbar; bare `results` bleibt unbekannt.

Der `ClassifiedResonanceController` hält genau einen process-lokalen Anker für
das jüngste erfolgreiche corrected Resonance-Ergebnis seiner aktuellen Sitzung:

- `CompletedComposeResult`
- `CompletedAnswerResult`

Ein späterer erfolgreicher COMPOSE-Zyklus ersetzt nur diese Sitzungsansicht.
Frühere Einladungen, private Return Workspaces und Return Artifacts bleiben als
separate externe Ausgaben bestehen. Sie werden nicht gelöscht, überschrieben,
invalidiert, verborgen oder gesucht. Abbruch, Validierungsfehler,
Publikationsfehler und Writer-Fehler ersetzen das letzte erfolgreiche Ergebnis
nicht.

Es gibt keine Ergebnisliste, Auswahlfläche, persistente Historie, Registry oder
Dateisystemsuche. `/results` rendert einmal und kehrt zum vorhandenen Post-run-
Prompt zurück. Die Ansicht ist read-only und startet weder Opening noch Matching,
Generator, Nachhall, Übertragung, Publikation oder Mutation.

## Erlaubte Ergebnisdarstellung

Die Ausgabe verwendet drei Klassen:

```text
[private local]
[public-safe]
[local path]
```

COMPOSE darf nur die gespeicherten Werte des originating contribution und die
beiden bekannten Ausgabepfade zeigen.

ANSWER darf nur das carried contribution, die Response-Auswahlen, das Return
Word, ein optionales carried public-safe Label oder eine ruhige Abwesenheitsmeldung
und den bekannten Return-Artifact-Pfad zeigen.

Token-, Route-, Return-Slot-, Package- und Aktivierungsinternas sowie generische
Objektdarstellungen sind nicht player-facing.

## Bekannte, später fehlende Pfade

Die gespeicherten In-memory-Werte bleiben sichtbar. Geprüft wird ausschließlich
der exakte bekannte Pfad. Fehlt die Ausgabe dort, meldet die Ansicht ruhig, dass
sie am bekannten Ort nicht mehr verfügbar ist, und erklärt ausdrücklich, dass
keine Dateisystemsuche ausgeführt wurde.

Es wird kein Ersatz gesucht, nichts regeneriert und kein Ergebniszustand
zerstört.

## Akzeptierte Slice-4A.1-Korrektur

ANSWER fragt nun nach:

```text
Parent directory for the Return Artifact (blank to cancel):
```

Akzeptiert werden nur vorhandene externe Verzeichnisse außerhalb des travelling
Nexus carrier. Dateien und nicht vorhandene Ziele werden ruhig abgelehnt.

Der Dateiname wird automatisch und neutral erzeugt:

```text
n01-return-artifact-<24 lowercase hexadecimal characters>.json
```

Die ID basiert auf sicherem Zufall entsprechend `secrets.token_hex(12)`. Sie
enthält weder Zeitstempel noch Wish/Return Word, Namen, Token-/Route-ID,
Pfadbestandteile, Benutzernamen oder persönliche Inhalte. Bis zu acht Kandidaten
werden versucht. Kollisionen überschreiben nichts; nach Ausschöpfung wird nichts
erstellt. Der atomare bestehende Writer bleibt die letzte No-overwrite-Grenze.

Der Zyklus gilt erst nach erfolgreichem Schreiben als abgeschlossen. Erst dann
wird der exakte Pfad in `CompletedAnswerResult` gehalten und durch `/results`
angezeigt. Ein späterer Writer-Fehler lässt ein früheres erfolgreiches
Sitzungsergebnis unverändert.

## Manuelle Abnahme

### COMPOSE

Eine frische integrierte Nexus-Kopie bestätigte:

- kein `/results` während des produktiven Zyklus;
- je erfolgreichem COMPOSE eine Einladung und ein privater Return Workspace;
- Anzeige der erlaubten Werte und beider exakter bekannter Pfade;
- ein expliziter zweiter COMPOSE wird zur jüngsten Sitzungsansicht;
- beide externen Ausgabepaare bestehen gleichzeitig;
- ein abgebrochener dritter COMPOSE bewahrt das zweite erfolgreiche Ergebnis;
- keine frühere Ausgabe wird entfernt oder überschrieben;
- keine internen IDs werden angezeigt.

### ANSWER

Eine frische integrierte Nexus-Kopie mit bewusst gewähltem gültigem Token V2
bestätigte:

- echten ANSWER-Modus und das carried originating contribution;
- genau ein automatisch benanntes Return Artifact im gewählten externen
  Elternverzeichnis;
- den neutralen 24-Hex-Dateinamen;
- abgeschlossene Wiederkehr ohne automatischen zweiten ANSWER;
- die erlaubten carried/response/return-Werte und den exakten bekannten Pfad;
- eine ruhige Meldung, wenn kein public-safe Summary vorhanden ist;
- keine Token-, Route-, Return-Slot-, Package- oder Objektinternas;
- nach manuellem Verschieben weiterhin sichtbare In-memory-Werte;
- den bekannten Pfad als nicht mehr verfügbar und die ausdrückliche No-search-
  Meldung;
- keine Neugenerierung.

Der frühere Full-file-path-Prompt deutete ein vorhandenes Verzeichnis als
vollständigen Dateipfad. Der Writer lehnte dies sicher und ohne Überschreiben ab.
Das war eine Bedienlücke, kein Sicherheitsfehler; 4A.1 löste sie vor der finalen
Abnahme.

Keine privaten Testwerte, lokalen absoluten Pfade oder zufälligen realen IDs sind
in dieser Notiz festgehalten.

## Persistenzgrenze

```text
Slice 4A
same-process COMPOSE/ANSWER result view

Slice 4B
known-source read-only rereading after restart

Slice 5A
manual Return Opening and stable local result creation

Slice 5B
read-only revisit of that already created stable local result
```

Slice 4A überlebt keinen Prozessneustart. Es entdeckt keine alten Ordner, scannt
weder Downloads noch das Dateisystem, errät keine Namen, sammelt keine Tokens,
baut keine Datenbank, History, Cloud-Synchronisierung oder Registry und liest
keine Dateien zur Rekonstruktion der Same-process-Ansicht erneut ein.

Slice 4B untersucht in einer getrennten read-only Inventur, wie eine absichtlich
bekannte autoritative Quelle nach Neustart sicher und ohne Discovery erneut
gelesen werden kann. 4B führt kein Return Opening aus, validiert kein Return
Artifact gegen einen Return Slot und erzeugt kein stabiles lokales Ergebnis.

## Geplante Ergebnisstufen

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

Das durch ANSWER erzeugte Return Artifact ist zunächst ein Transportobjekt und
nicht das finale lokale Ergebnis. Das stabile lokale Ergebnis entsteht erst
durch ein erfolgreiches absichtliches Return Opening gegen den strukturell
passenden Return Slot.

Slice 5A plant dieses manuelle Return Opening und die genau einmalige stabile
lokale Ergebniserzeugung. Slice 5B plant danach ausschließlich das read-only
Wiederanzeigen dieses bereits erzeugten stabilen Ergebnisses von einer bewusst
bekannten autoritativen Quelle. 5B wendet die in 4B untersuchte Known-source-
Grenze auf das besondere 5A-Ergebnis an oder erweitert sie nur mit ausdrücklicher
Begründung; es darf keine zweite unabhängige Persistenz- oder Ladearchitektur
schaffen.

Die Reihenfolge bleibt zwingend:

```text
Return Artifact deliberately opened
-> stable local result already exists

then:

/results
-> read and display that existing stable result
```

`/results` betrachtet ausschließlich. Es öffnet kein Return Artifact, validiert
oder verändert keinen Return Slot, erzeugt oder regeneriert weder Resonance
Artifact noch Nexus Echo oder Nachhall, erzeugt kein stabiles lokales Ergebnis,
überschreibt nichts, sucht nicht im Dateisystem und ruft Opening weder direkt
noch indirekt auf.

Die genaue Beziehung zwischen Resonance Artifact, Nexus Echo und Nachhall sowie
ihre konkreten Dateien und Pfade muss erst inventarisiert werden. Ein Nachhall
darf bei der späteren Anzeige nur erscheinen, wenn er bereits zum gespeicherten
Ergebnis gehört; die Anzeige erzeugt ihn niemals.

## Offene Slice-4B-Fragen

Eine separate read-only Inventur muss klären:

- welche bereits vorhandenen, autoritativen Quellen bewusst ausgewählt und
  sicher wieder gelesen werden können;
- welche Quelle je Ergebnisklasse maßgeblich ist;
- welche Auswahlhandlung ausdrücklich player-owned bleibt;
- welche Privacy-Klassen beim Wiederlesen gelten;
- wie fehlende oder verschobene bekannte Quellen ohne Discovery behandelt
  werden;
- ob Slice 4B überhaupt in die Geschenkfassung gehört.

Slice 4B soll keine Suche, Registry, automatische Token-Auswahl, Opening-
Erzeugung, Nachhall-Erzeugung oder Multi-result-Historie vorwegnehmen.

## Offene Slice-5-Fragen

Eine eigene read-only Inventur muss vor jeder Umsetzung klären:

1. Welche bestehende Opening-Funktion erzeugt das stabile Ergebnis?
2. Was tun `OPEN_RETURN.sh`, `incoming/` und `results/` bereits genau?
3. Welche Dateien enthalten Resonance Artifact, Nexus Echo und Nachhall?
4. Ist Nachhall gespeichertes Geschwister, optionale Komponente oder spätere Stufe?
5. Welcher exakte Pfad wird nach erfolgreichem Opening zurückgegeben oder gespeichert?
6. Wie wird dieser Pfad der Resonance Chamber ausdrücklich bekannt gemacht?
7. Wie wird nach Neustart ohne Dateisystemsuche oder allgemeine Registry gelesen?
8. Welche typisierte Ergebnisgruppe und Rendering-Allowlist werden benötigt?
9. Wie bleibt garantiert, dass `/results` Opening und Regeneration nie aufruft?
10. Wo liegt die bestehende Idempotenzgrenze wiederholten Openings?
11. Wie werden mehrere Artifacts ohne automatische Auswahl behandelt?
12. Welche Recovery-Zustände bestehen bereits und welche sind nur geplant?

Vor dieser Inventur werden weder eine genaue Dateistruktur noch ein endgültiger
Name für eine mögliche typisierte Ergebnisgruppe vorgeschrieben. Ausgeschlossen
sind eine allgemeine Registry, automatische Suche oder Auswahl, automatische
Rückkehr, Übertragung, Cloud-Synchronisierung, Publikation oder Opening,
Archivintegration, erneute ANSWER-Erzeugung, Regeneration oder Überschreiben und
eine neue Persistenzarchitektur ohne vorherige Inventur.

## Nächster sicherer Schritt

1. Diesen Dokumentationsdiff prüfen.
2. Vor einem Commit bei Bedarf die kanonische Suite erneut ausführen.
3. Ausdrückliche Freigabe für Stage, Commit und Push einholen.
4. Slice 4A sauber schließen.
5. Erst danach eine getrennte read-only Slice-4B-Inventur durchführen.
6. Danach eine getrennte read-only Slice-5-Inventur durchführen.
7. Erst nach den Inventuren über eine Umsetzung entscheiden.

Slice 4B und Slice 5 sind nicht zur Implementierung freigegeben. Jede Umsetzung
benötigt eine neue ausdrückliche Autorisierung.
