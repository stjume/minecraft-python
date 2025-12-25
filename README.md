> [!CAUTION]
> This library is in early development. We currently only permit private use. Any sort of commercial use is prohibited. This might change with future versions, when a final license is chosen.

# st_minecraft

(Eine deutsche Version dieser README ist in der Datei [README_DE.md](README_DE.md) verfügbar. Beachten Sie, dass die englische Version die _Hauptversion_ ist. Die deutsche Version _könnte_ veraltet sein.)

Library for interacting with a Minecraft server through Python programs.
This is the frontend part, which requires the use of our [Server Plugin](https://github.com/sk-jume/minecraft-python-backend) on the server side.

The library is designed to teach children the Python programming language playfully through interactions with Minecraft.
It is *not* intended for production use!

We provide an english and a german version of the library.

### Quick Example

```python
import st_minecraft.en as mc
from st_minecraft.en.material import MaterialCollection

mc.connect("localhost")

while True:
  player = mc.get_player()
  mc.set_block(player.x, player.y - 1, player.z, MaterialCollection.Diamond_Block)
```


```python
import st_minecraft.de as mc

mc.verbinden("localhost")

while True:
  spieler = mc.hole_spieler()
  mc.setze_block(spieler.x, spieler.y - 1, spieler.z, mc.MaterialSammlung.Stein)
```

If you're completely new to Python and programming: don't worry.
Just follow the steps below and copy the example.
You should see first results in a few minutes.


### Available Interactions
- Interact with players
  - fetch information about player (position, stats, inventory)
  - modify player position (incl. dimension and rotation)
  - modify player stats (xp, health, hunger)
  - give items
- Interact with Blocks
  - Set Blocks
  - Fetch Blocks
- Send and receive chat messages and execute commands
- Spawn and edit entities (mobs, items, etc.)
- Create and edit boss bars
- Display titles

## How to install
### What You Need

- A Minecraft Java Edition server with the appropriate server plugin running.
  More information can be found in the documentation of the [Server Plugin](https://github.com/sk-jume/minecraft-python-backend).
  If the server has been set up for you, you need the IP and port.
- Python 3.10 or newer on your computer. If not yet installed: download and install from `https://www.python.org/downloads/`.
    - Make sure to add Python to "PATH" during installation.
- We also recommend using [PyCharm](https://www.jetbrains.com/pycharm/download), the free version without subscription is completely sufficient!

### Installation with pip

#### (Optional) Using a virtual eenvironment
We recommend to us a [venv](https://docs.python.org/3/library/venv.html):
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

#### Installing the library

> [!CAUTION]
> We will publish this package via pypi in the near future. For now you need to do a local install.

Download this repository.

Open your terminal (macOS/Linux) or command prompt/PowerShell (Windows) navigate to the folder you downloaded it to.

Install it using:
#### Windows
```bash
py -m pip install .
```

#### Linux / MacOS
```bash
python3 -m pip install .
```

### Quickstart (copy & paste)

Examples of how to use the library can be found in [demo/](demo/).


### How the Library is Structured

The function names are available in german and english and kept beginner-friendly:

#### English examples
- Blocks: `set_block(...)`, `get_block(...)`
- Players: `get_player(...)`, `set_player_position(...)`, `set_player_health(...)`, `set_player_hunger(...)`, `set_player_xp_level(...)`, `set_player_velocity(...)`
- Chat & Commands: `send_to_chat(...)`, `send_command(...)`
- Entities: `spawn_entity(...)`, `set_entity_name(...)`, `set_entity_position(...)`, `set_entity_ai(...)`
- Inventory: `give_item(...)`, `get_inventory(...)`

Block and entity types come from the English enums `MaterialCollection` and `EntityCollection` (e.g., `MaterialCollection.Melon`, `EntityCollection.Sheep`).

#### German examples
- Blocks: `setze_block(...)`, `hole_block(...)`
- Players: `hole_spieler(...)`, `spieler_position_setzen(...)`, `spieler_leben_setzen(...)`, `spieler_hunger_setzen(...)`, `spieler_xp_level_setzen(...)`, `spieler_geschwindigkeit_setzen(...)`
- Chat & Commands: `sende_an_chat(...)`, `sende_befehl(...)`
- Entities: `erzeuge_entity(...)`, `entity_name_setzen(...)`, `entity_position_setzen(...)`, `entity_ai_setzen(...)`
- Inventory: `gebe_item(...)`, `hole_inventar(...)`

Block and entity types come from the German enums `MaterialSammlung` and `EntitySammlung` (e.g., `MaterialSammlung.Melone`, `EntitySammlung.Schaf`).

### Troubleshooting

- RuntimeError: "No connection to server. Please connect first."
  - First call `connect(HOST)`. Check the servers IP and whether the server is running.
- Timeout/No response from server
  - The server may not be reachable or the backend is not running. Also check IP and port.
- I don't know my coordinates (x, y, z)
  - Stand at the desired location in the game and press F3 to see your position. Alternatively, start with small test coordinates near the spawn.

#### AI Disclaimer
- Parts of the README and code have been translated using AI.
- All content has been reviewed by humans before publication.
- The logic itself was written by hand.
