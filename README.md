# sk_minecraft

A Python package for sk_minecraft.

## Installation

```bash
pip install sk_minecraft
```

## Usage

```python
import sk_minecraft
# your code here
``` 

## Feature Parity to [backend](https://github.com/sk-jume/minecraft-python-backend)

Here is a **high-level checklist** for the Minecraft Python Backend API based on your provided protocol. You can use this to track what’s already implemented or still pending:

---

### ✅ **API Command Implementation Checklist**

#### 🔧 **Block Commands**

* [x] `setBlock <x> <y> <z> <blockid>` — Set a block at a specific position
* [x] `getBlock <x> <y> <z>` — Get the block type at a specific position

#### 🧍 **Player Commands**

* [x] `getPlayer <index>` — Get player info (name, coords, rotation)
* [x] `setPlayerPos <playerindex> <x> <y> <z> ?rotation:?`
* [x] `setPlayerStat <type> <playerIndex> <value>`
* [x] `setPlayerVelocity <type> <playerIndex> <value>`

#### 💬 **Chat Commands**

* [x] `postChat <message>` — Post a message in the in-game chat
* [x] `chatCommand <command>` — Run a command via chat (without `/`)

#### 🧱 **Entity Commands**

* [x] `spawnEntity <x> <y> <z> <entityid>` — Spawn an entity at a location
* [ ] `editEntity <target> ?name:String? ?position:x;y;z? ?ai:boolean?`
* [ ] `getEntity <target>`

#### 🎒 **Inventory Commands**

* [x] `addInv <playerIndex> <materialId> <amount> ?name:? ?slot:? !unbreakable!` — Add item to player inventory
* [x] `getInv <playerIndex>` — Get current inventory contents for a player

#### ⚡ **Batching**

* [ ] `batch ;|;<command>;|;<command>` — Run multiple commands in one message

#### 📊 Boss Bar Commands

* [x] spawnBossBar <name> <text> — Spawn a boss bar with a name and display text

* [x] editBossBar <command> <name> ?text:? ?color:? ?value:? ?style:? — Edit an existing boss bar



---

Let me know if you want this as a Markdown file, a checklist app format (like Notion or Trello), or integrated into code comments or a README.


