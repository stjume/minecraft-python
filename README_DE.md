# st_minecraft

Bibliothek zum Interagieren mit einem Minecraft Server durch Python Programme.
Es handelt sich hier um den Frontend Part, welcher die Nutzung unseres [Server Plugins](https://github.com/sk-jume/minecraft-python-backend) auf Serverseite voraussetzt.

Die Bibliothek ist konzipiert, um Kindern spielerisch durch Interaktionen mit Minecraft die Programmiersprache python beizubringen.
Sie ist *nicht* für den produktiv-betrieb gedacht!

Wir bieten eine englische und eine deutsche Version der Bibliothek an.

### Schnelles Start

```python
import st_minecraft.de as mc

mc.verbinden("localhost")

while True:
  spieler = mc.hole_spieler()
  mc.setze_block(spieler.x, spieler.y - 1, spieler.z, mc.MaterialSammlung.Stein)
```

Wenn du noch ganz neu in Python und Programmierung bist: keine Sorge.
Folge einfach den Schritten unten und kopiere das Beispiel.
In wenigen Minuten solltest du erste Ergebnisse sehen.


### Verfügbare Interaktionen
- Mit Spielern interagieren
  - Informationen über Spieler abrufen (Position, Statistiken, Inventar)
  - Spielerposition ändern (inkl. Dimension und Rotation)
  - Spielerstatistiken ändern (XP, Gesundheit, Hunger)
  - Items geben
- Mit Blöcken interagieren
  - Blöcke setzen
  - Blöcke auslesen
- Chat-Nachrichten senden und empfangen sowie Befehle ausführen
- Entities (Mobs, Items, etc.) spawnen und bearbeiten
- Bossleisten erstellen und bearbeiten
- Titel anzeigen

## Installation

### Was du brauchst

- Einen Minecraft‑Java‑Edition‑Server, auf dem das passende Server Plugin läuft.
  Mehr dazu findest du in der Dokumentation des [Server Plugins](https://github.com/sk-jume/minecraft-python-backend).
  Wenn der Server für dich aufgesetzt wurde brauchst du die IP und Port.
- Python 3.10 oder neuer auf deinem Computer. Falls noch nicht installiert: von `https://www.python.org/downloads/` herunterladen und installieren.
    - Achte darauf Python zum "PATH" während dem Install hinzuzufügen.
- Wir empfehlen darüber hinaus [PyCharm](https://www.jetbrains.com/pycharm/download) zu benutzten, die kostenfreie Version ohne Abo reicht völlig aus!

### Installation mit pip

#### (Optional) Verwendung einer virtuellen Umgebung
Wir empfehlen die Verwendung einer [venv](https://docs.python.org/3/library/venv.html):
Windows:
```
py -m venv venv
venv\Scripts\Activate.ps1
```

Linux/MacOS:
```
python3 -m venv venv
venv/bin/activate
```

#### Installation der Bibliothek

> [!CAUTION]
> Wir werden dieses Paket in naher Zukunft über pypi veröffentlichen. Bis dahin musst du eine lokale Installation durchführen.

Lade dieses Repository herunter.

Öffne dein Terminal (macOS/Linux) oder die Eingabeaufforderung/PowerShell (Windows) und navigiere zu dem Ordner, in den du es heruntergeladen hast.

Installiere es mit:
#### Windows
```bash
py -m pip install .
```

#### Linux / MacOS
```bash
python3 -m pip install .
```

### Quickstart (kopieren & einfügen)

Beispiele, wie du die Library benutzt findest du in [demo/](demo/).


### So ist die Bibliothek aufgebaut

Die Funktionsnamen sind auf Deutsch und Englisch verfügbar und einsteigerfreundlich:

#### Deutsche Beispiele
- Blöcke: `setze_block(...)`, `hole_block(...)`
- Spieler: `hole_spieler(...)`, `spieler_position_setzen(...)`, `spieler_leben_setzen(...)`, `spieler_hunger_setzen(...)`, `spieler_xp_level_setzen(...)`, `spieler_geschwindigkeit_setzen(...)`
- Chat & Befehle: `sende_an_chat(...)`, `sende_befehl(...)`
- Entities: `erzeuge_entity(...)`, `entity_name_setzen(...)`, `entity_position_setzen(...)`, `entity_ai_setzen(...)`
- Inventar: `gebe_item(...)`, `hole_inventar(...)`

Block‑ und Entity‑Typen kommen aus den deutschen Enums `MaterialSammlung` und `EntitySammlung` (z. B. `MaterialSammlung.Melone`, `EntitySammlung.Schaf`).

#### Englische Beispiele
- Blocks: `set_block(...)`, `get_block(...)`
- Players: `get_player(...)`, `set_player_position(...)`, `set_player_health(...)`, `set_player_hunger(...)`, `set_player_xp_level(...)`, `set_player_velocity(...)`
- Chat & Commands: `send_to_chat(...)`, `send_command(...)`
- Entities: `spawn_entity(...)`, `set_entity_name(...)`, `set_entity_position(...)`, `set_entity_ai(...)`
- Inventory: `give_item(...)`, `get_inventory(...)`

Block and entity types come from the English enums `MaterialCollection` and `EntityCollection` (e.g., `MaterialCollection.Melon`, `EntityCollection.Sheep`).

### Fehlerbehebung

- RuntimeError: "No connection to server. Please connect first."
  - Rufe zuerst `verbinden(HOST)` auf. Prüfe die IP des Servers und ob der Server läuft.
- Timeout/Keine Antwort vom Server
  - Der Server ist ggf. nicht erreichbar oder das Backend läuft nicht. Prüfe zusätzlich IP und Port.
- Ich kenne die Koordinaten (x, y, z) nicht
  - Stelle dich im Spiel an die gewünschte Stelle und drücke F3, um deine Position zu sehen. Alternativ mit kleinen Testkoordinaten in der Nähe des Spawns beginnen.


#### AI Disclaimer
- Teile des README und des Codes sind mit KI übersetzt.
- Alle inhalte wurden von Menschen vor Veröffentlichung überprüft.
- Die Logik selber wurde von Hand geschrieben.
