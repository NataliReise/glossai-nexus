# Übergabenotiz: Nexus 01 nach Slice 4A

## Zweck

Diese Notiz übergibt den akzeptierten Stand von `/results` und grenzt die spätere
Frage des Wiederlesens vorhandener Resonanzartefakte nach einem Neustart ab.

Slice 4A und die enge Korrektur 4A.1 sind implementiert, geprüft und manuell
akzeptiert. Slice 4A ist korrekt, bleibt bestehen und darf nicht zurückgerollt
werden. Slice 4B und die neu geplante Slice 5 sind nicht implementiert und nicht
zur Umsetzung freigegeben.

Die nach Slice 4A geforderte read-only Inventur zu Slice 4B und Slice 5 ist
inzwischen abgeschlossen. Die daraus folgenden Entscheidungen sind getroffen
und die Planung ist aktualisiert. Operative technische Opening-Infrastruktur ist
vorhanden; das ist ausdrücklich nicht gleichbedeutend mit einer integrierten,
gehärteten und manuell akzeptierten Spielscheibe 5A.

## Repository- und Prüfstand

- Branch: `gift/nexus-01-chamber-archive`
- Slice-4A/4A.1-Implementierungscommit:
  `0da16511d3c068b7afbad7632d36566a0d14de4d`
- Slice-4A-Abnahme-, Status- und Planungscommit:
  `62dc94b0d08a57d8b61127d7f01bfb723981896e`
- Beide Commits wurden auf `origin/gift/nexus-01-chamber-archive` gepusht.
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

Die Inventur fand mehrere quellspezifische read-only Loader, aber keine
bestehende generische Known-source-Ladegrenze. Slice 4B bleibt auf bewusst
bekannte autoritative Quellen nach Neustart begrenzt, vollständig read-only und
ohne Registry, allgemeine Dateisystemsuche, Return Opening, Matching,
Generierung oder Mutation. Slice 4B ist nicht implementiert und nicht zur
Umsetzung freigegeben.

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

Die Inventur bestätigt den gegenwärtigen operativen Produktionspfad in:

```text
modules/nexus_01_nexus_mesomerie/open_resonance_return.py
open_resonance_return_files()
```

Er erzeugt innerhalb des bestehenden Opening-Pfads atomar und ohne
Überschreiben genau eine stabile Markdown-Datei unter:

```text
<private Return Workspace>/results/<ReturnSlot.result_file>
```

## Autoritatives stabiles Produktionsresultat

Entscheidung getroffen: Die bestehende Markdown-Datei mit dem kompakten
Nachhall ist für den Geschenk-Sprint das autoritative stabile lokale
Produktionsresultat. Sie enthält:

- den sichtbaren kompakten Nachhall;
- einen eingebetteten technischen Trace;
- möglicherweise spätere manuelle Ergänzungen.

Im aktuellen Produktionspfad ist der kompakte Nachhall nicht nur eine optionale
spätere Komponente, sondern die vollständige sichtbare stabile Ergebnisform.
Für Resonance Artifact und Nexus Echo werden im Geschenk-Sprint keine neuen
separaten Produktionsdateien eingeführt. Vorhandene entsprechende Renderer und
Begriffe gehören zum Legacy-Bestand und dürfen nicht als aktueller
Produktionsvertrag dargestellt werden.

Ältere Dokumente und Legacy-Module beschreiben Resonance Artifact und Nexus Echo
teilweise noch als Ergebnisform. Der aktuelle Produktionscode und die aktuelle
Richtung verwenden den kompakten Nachhall als vollständiges stabiles Ergebnis.
Diese Legacy-Begriffe werden in einer späteren Dokumentationsbereinigung
synchronisiert; historische, archivierte, V0.1-, Transition- und Legacy-Dateien
bleiben durch diese Aktualisierung unverändert.

## Bewusste Return-Handlung

Die Spielerlebnis-Entscheidung lautet:

```text
Artifact bewusst nach incoming/ kopieren
-> OPEN_RETURN.sh ausdrücklich starten
-> bei genau einem Artifact dieses verwenden
-> bei mehreren Artifacts jede automatische Auswahl verweigern
```

Diese Interaktion gilt als hinreichend bewusst: Das Artifact wird manuell in den
privaten Return Workspace gebracht und das Opening anschließend ausdrücklich
gestartet. Der Launcher führt eine begrenzte Ermittlung ausschließlich innerhalb
des ausdrücklich bekannten `incoming/*.json` durch. Null Kandidaten werden
abgelehnt; genau ein bewusst dort abgelegter Kandidat wird verwendet; mehrere
werden aufgelistet, aber niemals automatisch ausgewählt. Es gibt keine
allgemeine Discovery. Für genau einen bewusst abgelegten Kandidaten ist kein
zusätzlicher Auswahlprompt erforderlich.

Slice 5A soll die bestehende Produktionsinfrastruktur verwenden und keine neue
parallele Opening-Architektur schaffen. Als integrierte, gehärtete und manuell
akzeptierte Spielscheibe bleibt 5A nicht implementiert und nicht zur Umsetzung
freigegeben.

Die Reihenfolge bleibt zwingend:

```text
Return Artifact deliberately opened
-> stable local result already exists

then:

/results
-> read and display that existing stable result
```

Der bestehende öffentliche Opening-Orchestrator ist kein zulässiger Reader für
`/results`. Er kann je nach Zustand Ergebnisdateien erzeugen, Return Artifact und
Return Slot matchen, Generatorlogik aufrufen, den Slotstatus verändern oder
Recovery und Slot-Reparatur durchführen. Der einzige bestehende reine
Dateireader ist derzeit ein privater Helfer innerhalb dieses mutierenden
Opening-Pfads.

Damit ist Option C belegt:

```text
Vor einer Slice-5B-Integration ist eine schmale Trennung
zwischen „bestehendes Ergebnis lesen“ und „Return öffnen“ erforderlich.
```

5B darf nur die bereits bestehende autoritative Markdown-Datei über einen
explizit bekannten Pfad read-only lesen. Es darf Opening-Orchestrierung,
Return-Artifact-Parsing als Voraussetzung für Revisit, Slot-Matching, Generator,
Slot-Update, Regeneration, Reparatur, Kandidatensuche oder Kandidatenauswahl
weder importieren noch aufrufen. Slice 5B bleibt nicht implementiert und nicht
zur Umsetzung freigegeben.

## Verbindliche `/results`-Allowlist für 5B

Eine spätere Anzeige darf niemals die ganze Markdown-Datei ungefiltert ausgeben.
Die erste Allowlist lautet:

```text
[private local]
gespeicherter kompakter Nachhall

[local path]
exakter bewusst bekannter Resultatpfad
Verfügbarkeit dieses Pfades
```

Ausdrücklich nicht anzeigen:

- technischer Trace;
- `artifact_identity` und `slot_identity`;
- Route-, Package-, Slot- oder Origin-IDs;
- deterministischer Seed oder Seed-Ableitung;
- Composition Plan;
- Generatorinternas;
- Profil- oder Source-IDs;
- Slotstatus und Slotnotizen;
- generische Objektrepräsentationen;
- unklassifizierte manuelle Anhänge.

Manuelle Notizen sind eine interessante mögliche spätere persönliche
Erweiterung, gehören aber nicht zur ersten 5B-Allowlist. Sie dürfen erst nach
einer eigenen Datenschutz-, Format- und Spielerlebnisentscheidung sichtbar
werden. Vorher werden sie weder automatisch erkannt noch automatisch
dargestellt.

## Bestehende Idempotenz- und No-overwrite-Grenzen

Folgende Produktionsgrenzen bleiben wertvoll und müssen erhalten werden:

- bestehende Ergebnisdateien werden unverändert gelesen;
- ein geöffneter Slot ohne Ergebnisdatei wird hart abgelehnt;
- es findet keine Regeneration statt;
- atomare Erzeugung verhindert Überschreiben;
- Symlinks und unsichere Zielpfade werden abgelehnt;
- manuelle Ergänzungen einer vorhandenen Ergebnisdatei bleiben erhalten;
- nach fehlgeschlagenem Slot-Update kann die vorhandene Ergebnisdatei später
  ohne Regeneration zur Slot-Reparatur verwendet werden.

`/results` darf diese Recovery- oder Reparaturlogik niemals aufrufen.

## Priorisierter 5A-Härtungsbefund

Doppelte identische Return-Slot-Identitäten werden im allgemeinen
Produktionspfad möglicherweise erst nach der Ergebnisdateierzeugung beim
Slot-Update eindeutig abgelehnt. Dadurch kann entstehen:

```text
Ergebnisdatei existiert
-> Slot-Update scheitert wegen Mehrdeutigkeit
-> partieller Zustand
```

Verbindliche spätere Sicherheitsanforderung: Die Eindeutigkeit der maßgeblichen
Slot-Identität muss vor jeder Generierung oder Dateierzeugung vollständig geprüft
werden. Diese Härtung ist nicht implementiert, nicht freigegeben, muss vor oder
innerhalb der 5A-Integration separat umgesetzt und getestet werden und darf nicht
mit 5B vermischt werden.

## Offene Architekturfrage: bewusste Pfadübergabe

Die wichtigste verbleibende Frage lautet:

```text
Wie gelangt der exakte autoritative stabile Resultatpfad
nach einem Prozessneustart bewusst zur Resonance Chamber?
```

Belegte Ausgangslage:

- während des Openings existiert der Pfad als `LocalResonanceResult.path`;
- die CLI gibt ihn aus;
- er kann aus bewusst bekanntem Workspace plus `slot.result_file` bestimmt
  werden;
- die Resonance Chamber erhält oder persistiert ihn derzeit nicht;
- Registry, automatische Suche, Ergebnisdatenbank und Schattenkopie sind
  ausgeschlossen.

Die technische Lösung wird noch nicht vorweggenommen. Als nächster separater
read-only Schritt wird die kleinste vorhandene Übergabenaht untersucht:
Konstruktion und Eintritt der Resonance Chamber nach Neustart, vorhandene
explizite Pfadparameter, Launcher- oder Aktivierungskontext, bestehende
Controller-Eingaben, bewusst bekannte Workspace-Pfade und paketrelative oder
lokale Source-Übergaben. Eine spätere Lösung muss bewusst, lokal, explizit, ohne
Registry, ohne Discovery, ohne zweite Persistenzschicht und ohne Kopplung an
Opening arbeiten.

## Nächster sicherer Schritt

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

Dies ist eine vorsichtige Planungsreihenfolge und keine
Implementierungsfreigabe. Slice 4A bleibt unverändert und abgeschlossen. Slice
4B, 5A und 5B bleiben nicht implementiert und nicht zur Umsetzung freigegeben.
Die Pfadübergabe-Inventur ist der unmittelbar nächste technische Schritt. Jede
Umsetzung benötigt eine neue ausdrückliche Autorisierung.
