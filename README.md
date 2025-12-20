## sk_minecraft

Bibliothek zum Interagieren mit einem Minecraft Server durch Python Programme.
Es handelt sich hier um den Frontend Part, welcher die Nutzung unseres [Server Plugins](https://github.com/sk-jume/minecraft-python-backend) auf Serverseite voraussetzt.

Die Bibliothek ist konzipiert, um Kindern spielerisch durch Interaktionen mit Minecraft die Programmiersprache python beizubringen.
Sie ist *nicht* für den prduktiv-betrieb gedacht!

### Verfügbare Interaktionen
- Blöcke setzen und auslesen
- Spieler abfragen und bewegen
- Chat‑Nachrichten senden, empfangen und Befehle ausführen
- Entities (Mobs, Items, etc.) spawnen und bearbeiten
- Spieler‑Inventar verwalten
- Mit Bossleisten arbeiten

Wenn du noch ganz neu in Python und Programmierung bist: keine Sorge. Folge einfach den Schritten unten und kopiere das Beispiel. In wenigen Minuten solltest du erste Ergebnisse sehen.

### Was du brauchst

- Einen Minecraft‑Java‑Edition‑Server, auf dem das passende Server Plugin läuft.
Mehr dazu findest du in der Dokumentation des [Server Plugins](https://github.com/sk-jume/minecraft-python-backend).
Wenn der Server für dich aufgesetzt wurde brauchst du die IP und Port.
- Python 3.9 oder neuer auf deinem Computer. Falls noch nicht installiert: von `https://www.python.org/downloads/` herunterladen und installieren.
    - Achte darauf Python zum "PATH" während dem Install hinzuzufügen.
- Wir empfehlen darüber hinaus [Pycharm](https://www.jetbrains.com/pycharm/download) zu benutzten, die kostenfreie Version ohne Abo reicht völlig aus!

### Installation mit pip

Öffne dein Terminal (macOS/Linux) oder die Eingabeaufforderung/PowerShell (Windows) und installiere das Paket:

#### Windows
```bash
py -m pip install st_minecraft
```

#### Linux / MacOS
```bash
python3 -m pip install st_minecraft
```

### Quickstart (kopieren & einfügen)

Beispiele, wie du die Library benutzt findest du in [demo/](demo/).


### So ist die Bibliothek aufgebaut

Die Funktionsnamen sind auf Deutsch gehalten und einsteigerfreundlich:
- Blöcke: `setze_block(...)`, `hole_block(...)`
- Spieler: `hole_spieler(...)`, `spieler_position_setzen(...)`, `spieler_leben_setzen(...)`, `spieler_hunger_setzen(...)`, `spieler_xp_level_setzen(...)`, `spieler_geschwindigkeit_setzen(...)`
- Chat & Befehle: `sende_an_chat(...)`, `sende_befehl(...)`
- Entities: `erzeuge_entity(...)`, `entity_name_setzen(...)`, `entity_position_setzen(...)`, `entity_ai_setzen(...)`
- Inventar: `gebe_item(...)`, `hole_inventar(...)`

Block‑ und Entity‑Typen kommen aus den deutschen Enums `MaterialSammlung` und `EntitySammlung` (z. B. `MaterialSammlung.Melone`, `EntitySammlung.Schaf`).

### Fehlerbehebung

- RuntimeError: „Keine Verbindung zum Server. Bitte zuerst verbinden.“
  - Rufe zuerst `verbinden(HOST, PORT)` auf. Prüfe IP/Port und ob der Server läuft.
- Timeout/Keine Antwort vom Server
  - Der Server ist ggf. nicht erreichbar oder das Backend läuft nicht. Prüfe zusätzlich IP und Port.
- Ich kenne die Koordinaten (x, y, z) nicht
  - Stelle dich im Spiel an die gewünschte Stelle und drücke F3 (Java Edition), um deine Position zu sehen. Alternativ mit kleinen Testkoordinaten in der Nähe des Spawns beginnen.

---

## Funktionsabdeckung zum [Backend](https://github.com/sk-jume/minecraft-python-backend)

Hier ist eine grobe Checkliste der Backend‑Befehle und was davon in dieser Bibliothek umgesetzt ist:

### Checkliste der API‑Befehle

#### Block‑Befehle

* [x] `setBlock <x> <y> <z> <blockid>` — Setzt einen Block an einer bestimmten Position
* [x] `getBlock <x> <y> <z>` — Liest den Block‑Typ an einer Position aus

#### Spieler‑Befehle

* [x] `getPlayer <index>` — Spielerdaten abrufen (Name, Koordinaten, Rotation)
* [x] `setPlayerPos <playerindex> <x> <y> <z> ?rotation:?`
* [x] `setPlayerStat <type> <playerIndex> <value>`
* [x] `setPlayerVelocity <type> <playerIndex> <value>`

#### Chat‑Befehle

* [x] `postChat <message>` — Nachricht in den In‑Game‑Chat senden
* [x] `chatCommand <command>` — Befehl per Chat ausführen (ohne `/`)

#### Entity‑Befehle

* [x] `spawnEntity <x> <y> <z> <entityid>` — Entity an Position spawnen
* [x] `editEntity <target> ?name:String? ?position:x;y;z? ?ai:boolean?`
* [x] `getEntity <target>`

#### Inventar‑Befehle

* [x] `addInv <playerIndex> <materialId> <amount> ?name:? ?slot:? !unbreakable!` — Item ins Spieler‑Inventar legen
* [x] `getInv <playerIndex>` — Aktuellen Inventarinhalt eines Spielers abrufen

#### ⚡ Batching

* [ ] `batch ;|;<command>;|;<command>` — Mehrere Befehle in einer Nachricht

#### Bossleisten‑Befehle

* [x] `spawnBossBar <name> <text>` — Bossleiste mit Namen und Text erstellen
* [x] `editBossBar <command> <name> ?text:? ?color:? ?value:? ?style:?` — Existierende Bossleiste bearbeiten

(Teile dieser Readme wurden mit Hilfe von AI generiert und danach manuell auf Richtigkeit überprüft).
