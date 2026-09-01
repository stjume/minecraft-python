"""
This example is really advanced.
It uses a lot of advanced techniques and requires a better understanding from python, loops and datastructures

The idea is as follows: you have to navigate a labyrinth, the normal floor (gras) kills you.
But if you look at a certain block type (blue ice) a safe block (normal ice) spawns below you and keeps you safe
Those safe blocks disappear after a certain amount of time,
but only if you're not standing on it whilst also watching the safe block.

So if you keep watching the safe block you are safe!

There is also a timer structure so that you loose if you cant reach the goal after a certain time.
"""

import time

from pydantic import BaseModel

import st_minecraft.en as mc
import st_minecraft.en.boss_bar as boss_bar
from st_minecraft.en import Material
from st_minecraft.en import MaterialCollection
from st_minecraft.en.utils import get_block_below_player


class BlockRecord(BaseModel):
    """
    Class to store when and how a block at a certain coordinate was changed
    """

    # reason for not using a tuple: we potentially need to update the time_changed after creation of a record
    time_changed: float
    coords: tuple[float, float, float]
    old_type: MaterialCollection
    old_block: Material


def ice_game(p: mc.Player, time_until_disappear: float = 2):
    """
    game where you have to reach a goal whilst constantly looking at a block.
    as long as you look on that block type safe blocks will spawn under you (and disappear after some time)
    if you stand on the wrong block you die.
    """

    bar = boss_bar.create_bar("run", "Run to the finish!")
    remaining = 1.0
    boss_bar_update_interval_seconds = 1

    boss_bar.set_value(bar, remaining)
    boss_bar.set_color(bar, boss_bar.BossBarColor.BLUE)

    last_boss_bar_change = time.time()

    # stores blocks that were changed (mapping coordinates to BlockRecord)
    changed_blocks: dict[tuple, BlockRecord] = {}

    replace_with = MaterialCollection.Ice
    spawner_block = MaterialCollection.Blue_Ice

    # it set to false when player died
    potential_win = True

    # blocks that we don't replace and that don't kill
    safe_blocks = [MaterialCollection.Obsidian, MaterialCollection.Blue_Ice]
    win_block = MaterialCollection.Blue_Ice
    death_block = MaterialCollection.Grass_Block

    # game loop
    while True:
        p = mc.get_player(name=p.name)
        b = get_block_below_player(p)

        # case where we want to spawn a block
        # the player must look at the MaterialCollection.Blue_Ice to spawn a block
        # obsidian is safe and will not be replaced, hence we dont trigger a replace in that case
        if p.looking_at == spawner_block and not b.type in safe_blocks:
            mc.set_block(*b.coords, replace_with)

            # if block is already changed before, only update time
            #  if we add a new record, we replace `replace_with` with `replace_with` and loose the original block type
            if b.coords_int in changed_blocks:
                changed_blocks[b.coords_int].time_changed = time.time()

            # we need to create a new record and register it
            else:
                record = BlockRecord(time_changed=time.time(), coords=b.coords_int, old_type=b.type, old_block=b)
                changed_blocks[b.coords_int] = record

        # case where the player dies
        elif b == death_block:
            potential_win = False
            mc.send_command(f"kill {p.name}")

        # check time since last change for blocks in dict
        # replace blocks with original material if a certain time has passed
        # we need the list() because we will potentially delete from the dict and you never modify the iteration source
        #  during iteration!
        for coords, record in list(changed_blocks.items()):
            now = time.time()

            # if enough time elapsed, change block back
            if now - record.time_changed > time_until_disappear:
                mc.set_block(*record.coords, record.old_type)
                # delte entry from dict
                del changed_blocks[coords]
                continue  # we're done with this block, so let's start the next iteration of the loop

            # we use that dicts store the items in order of how they were added
            # so we can skip all checks as soon as one failed
            # all blocks after this are newer, so we don't need to check them.
            break

        # boss bar maintenance
        now = time.time()
        if now - last_boss_bar_change > boss_bar_update_interval_seconds:
            # update time when we last changed bar
            last_boss_bar_change = time.time()
            # update remaining part
            remaining = remaining - 0.1
            # cant have negative values, so we make sure that we always at least take 0 when remaining gets negative
            bar = boss_bar.set_value(bar, max(remaining, 0))
            # time over
            if remaining <= 0:
                # check if we won
                if not potential_win or b != win_block:
                    mc.show_title("You lose!")
                    mc.send_command(f"kill {p.name}")

                else:
                    mc.show_title("You win!")

                # cleanup
                boss_bar.delete_bar(bar)
                # end function
                return


if __name__ == "__main__":
    mc.connect()

    _s = mc.get_player()

    ice_game(
        _s,
    )
