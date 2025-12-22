> [!CAUTION]
> This library is in early development. We currently only permit private use. Any sort of commertial use is prohibited. This might change with future versions, when a final license is chosen.

## st_minecraft

(Eine deutsche Version dieser README ist in der Datei [README_DE.md](README_DE.md) verfügbar. Beachten Sie, dass die englische Version die _Hauptversion_ ist. Die deutsche Version _könnte_ veraltet sein.)

Library for interacting with a Minecraft server through Python programs.
This is the frontend part, which requires the use of our [Server Plugin](https://github.com/sk-jume/minecraft-python-backend) on the server side.

The library is designed to teach children the Python programming language playfully through interactions with Minecraft.
It is *not* intended for production use!

We provide an english and a german version of the library.

### Available Interactions
- Set and read blocks
- Query and move players
- Send and receive chat messages and execute commands
- Spawn and edit entities (mobs, items, etc.)
- Manage player inventory
- Work with boss bars

If you're completely new to Python and programming: don't worry. Just follow the steps below and copy the example. You should see first results in a few minutes.

### What You Need

- A Minecraft Java Edition server with the appropriate server plugin running.
  More information can be found in the documentation of the [Server Plugin](https://github.com/sk-jume/minecraft-python-backend).
  If the server has been set up for you, you need the IP and port.
- Python 3.10 or newer on your computer. If not yet installed: download and install from `https://www.python.org/downloads/`.
    - Make sure to add Python to "PATH" during installation.
- We also recommend using [PyCharm](https://www.jetbrains.com/pycharm/download), the free version without subscription is completely sufficient!

### Installation with pip

Open your terminal (macOS/Linux) or command prompt/PowerShell (Windows) and install the package:

#### Windows
```bash
py -m pip install st_minecraft
```

#### Linux / MacOS
```bash
python3 -m pip install st_minecraft
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
  - First call `connect(HOST, PORT)`. Check IP/port and whether the server is running.
- Timeout/No response from server
  - The server may not be reachable or the backend is not running. Also check IP and port.
- I don't know the coordinates (x, y, z)
  - Stand at the desired location in the game and press F3 (Java Edition) to see your position. Alternatively, start with small test coordinates near the spawn.

---

## Feature Coverage for [Backend](https://github.com/sk-jume/minecraft-python-backend)

Here is a rough checklist of backend commands and what is implemented in this library:

### API Commands Checklist

#### Block Commands

* [x] `setBlock <x> <y> <z> <blockid>` — Sets a block at a specific position
* [x] `getBlock <x> <y> <z>` — Reads the block type at a position

#### Player Commands

* [x] `getPlayer <index>` — Retrieve player data (name, coordinates, rotation)
* [x] `setPlayerPos <playerindex> <x> <y> <z> ?rotation:?`
* [x] `setPlayerStat <type> <playerIndex> <value>`
* [x] `setPlayerVelocity <type> <playerIndex> <value>`

#### Chat Commands

* [x] `postChat <message>` — Send message to in-game chat
* [x] `chatCommand <command>` — Execute command via chat (without `/`)

#### Entity Commands

* [x] `spawnEntity <x> <y> <z> <entityid>` — Spawn entity at position
* [x] `editEntity <target> ?name:String? ?position:x;y;z? ?ai:boolean?`
* [x] `getEntity <target>`

#### Inventory Commands

* [x] `addInv <playerIndex> <materialId> <amount> ?name:? ?slot:? !unbreakable!` — Place item in player inventory
* [x] `getInv <playerIndex>` — Retrieve current inventory contents of a player

#### ⚡ Batching

* [ ] `batch ;|;<command>;|;<command>` — Multiple commands in one message

#### Boss Bar Commands

* [x] `spawnBossBar <name> <text>` — Create boss bar with name and text
* [x] `editBossBar <command> <name> ?text:? ?color:? ?value:? ?style:?` — Edit existing boss bar

(Parts of this README were generated with the help of AI and then manually checked for correctness).
