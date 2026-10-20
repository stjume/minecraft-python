"""
Note: these tests are AI GENERATED.

Tests the comparison behaviour (__eq__ / __ne__) of the data models.

The english implementation is the baseline, the german one is only a translation layer on top of it.
Every test therefore runs once per language variant and expects the exact same result from both.
Adding a case here means stating what the comparison *should* do, not what it currently does.

Run with: pytest demo/test_comparisons.py
"""

from datetime import datetime
from enum import Enum
from typing import Protocol

import pytest
from pydantic import BaseModel

import st_minecraft.de.boss_leiste as bl
import st_minecraft.de.daten_modelle as de
import st_minecraft.en.boss_bar as bb
import st_minecraft.en.data_models as en
from st_minecraft.de.entity import EntitySammlung
from st_minecraft.de.material import MaterialSammlung
from st_minecraft.en.data_models import Dimension
from st_minecraft.en.entity import EntityCollection
from st_minecraft.en.material import MaterialCollection

DISPLAY_NAME = "Ein Stein"
"""Display name used wherever the concrete value does not matter"""

ENTITY_ID = "entity-1"
"""Entity id used wherever the concrete value does not matter"""

SENT_AT = datetime(2026, 10, 20, 12, 0, 0)
LATER = datetime(2026, 10, 20, 12, 0, 1)

NOT_COMPARABLE: list[object] = [42, 3.14, [], {}, None]
"""Values that carry no meaning for any data model and may therefore never compare equal to one"""

NOT_COMPARABLE_OR_STRING: list[object] = [*NOT_COMPARABLE, "Stein"]
"""Same as NOT_COMPARABLE, plus a string - only a message gives a string a meaning"""


# --------------------------------------------------------------------------------------------------
# language variants
# --------------------------------------------------------------------------------------------------


class Variant(Protocol):
    """
    One language variant of the library.

    Exposes language-neutral constructors so that a single test can run against both variants.
    """

    name: str
    stone: Enum
    dirt: Enum
    pig: Enum
    cow: Enum

    def item(self, material: Enum, display_name: str | None = DISPLAY_NAME) -> BaseModel: ...

    def field(
        self,
        material: Enum,
        display_name: str | None = DISPLAY_NAME,
        index: int = 0,
        amount: int = 1,
    ) -> BaseModel: ...

    def block(
        self,
        material: Enum | None,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        dimension: Dimension = Dimension.World,
    ) -> BaseModel: ...

    def entity(
        self,
        species: Enum,
        entity_id: str | None = ENTITY_ID,
        name: str | None = None,
        x: float | None = None,
    ) -> BaseModel: ...

    def message(
        self,
        text: str = "hallo",
        sender_name: str = "chris",
        sender_id: int = 1,
        sent_at: datetime = SENT_AT,
    ) -> BaseModel: ...

    def player(self, player_id: int = 1, name: str = "chris", x: float = 0.0) -> BaseModel: ...

    def boss_bar(self, name: str = "leiste", display_text: str = "hallo", value: float = 0.5) -> BaseModel: ...

    def inventory(self, *fields: BaseModel) -> dict[int, BaseModel]: ...


class English:
    """Constructors for the english data models"""

    name = "english"
    stone = MaterialCollection.Stone
    dirt = MaterialCollection.Dirt
    pig = EntityCollection.Pig
    cow = EntityCollection.Cow

    def item(self, material: Enum, display_name: str | None = DISPLAY_NAME) -> BaseModel:
        return en.Item(type=material, display_name=display_name)

    def field(
        self,
        material: Enum,
        display_name: str | None = DISPLAY_NAME,
        index: int = 0,
        amount: int = 1,
    ) -> BaseModel:
        return en.InventoryField(type=material, display_name=display_name, index=index, amount=amount)

    def block(
        self,
        material: Enum | None,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        dimension: Dimension = Dimension.World,
    ) -> BaseModel:
        return en.Material(type=material, x=x, y=y, z=z, dimension=dimension)

    def entity(
        self,
        species: Enum,
        entity_id: str | None = ENTITY_ID,
        name: str | None = None,
        x: float | None = None,
    ) -> BaseModel:
        return en.Entity(type=species, id=entity_id, name=name, x=x)

    def message(
        self,
        text: str = "hallo",
        sender_name: str = "chris",
        sender_id: int = 1,
        sent_at: datetime = SENT_AT,
    ) -> BaseModel:
        return en.Message(text=text, sender_name=sender_name, sender_id=sender_id, time_when_sent=sent_at)

    def player(self, player_id: int = 1, name: str = "chris", x: float = 0.0) -> BaseModel:
        return en.Player(
            id=player_id,
            name=name,
            x=x,
            y=64.0,
            z=0.0,
            dimension=Dimension.World,
            rotation=0,
            looking_at_block=None,
            looking_at_entity=None,
            sneaked=False,
            max_health=20.0,
            health=20.0,
            hunger=20.0,
            saturation=5.0,
            xp_level=0.0,
            xp_progress=0.0,
            holds_item=self.field(self.stone),
        )

    def boss_bar(self, name: str = "leiste", display_text: str = "hallo", value: float = 0.5) -> BaseModel:
        return bb.BossBar(
            name=name,
            display_text=display_text,
            value=value,
            style=bb.BossBarStyle.SOLID,
            color=bb.BossBarColor.BLUE,
        )

    def inventory(self, *fields: BaseModel) -> dict[int, BaseModel]:
        return en.Inventory({field.index: field for field in fields})


class German:
    """Constructors for the german data models"""

    name = "german"
    stone = MaterialSammlung.Stein
    dirt = MaterialSammlung.Erde
    pig = EntitySammlung.Schwein
    cow = EntitySammlung.Kuh

    def item(self, material: Enum, display_name: str | None = DISPLAY_NAME) -> BaseModel:
        return de.Item(typ=material, anzeige_name=display_name)

    def field(
        self,
        material: Enum,
        display_name: str | None = DISPLAY_NAME,
        index: int = 0,
        amount: int = 1,
    ) -> BaseModel:
        return de.InventarFeld(typ=material, anzeige_name=display_name, index=index, anzahl=amount)

    def block(
        self,
        material: Enum | None,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        dimension: Dimension = Dimension.World,
    ) -> BaseModel:
        return de.Material(typ=material, x=x, y=y, z=z, dimension=dimension)

    def entity(
        self,
        species: Enum,
        entity_id: str | None = ENTITY_ID,
        name: str | None = None,
        x: float | None = None,
    ) -> BaseModel:
        return de.Entity(typ=species, id=entity_id, name=name, x=x)

    def message(
        self,
        text: str = "hallo",
        sender_name: str = "chris",
        sender_id: int = 1,
        sent_at: datetime = SENT_AT,
    ) -> BaseModel:
        return de.Nachricht(text=text, absender_name=sender_name, absender_id=sender_id, versandzeit=sent_at)

    def player(self, player_id: int = 1, name: str = "chris", x: float = 0.0) -> BaseModel:
        return de.Spieler(
            id=player_id,
            name=name,
            x=x,
            y=64.0,
            z=0.0,
            dimension=Dimension.World,
            rotation=0,
            schaut_auf_block=None,
            schaut_auf_entity=None,
            sneaked=False,
            max_leben=20.0,
            leben=20.0,
            hunger=20.0,
            sättigung=5.0,
            xp_level=0.0,
            xp_fortschritt=0.0,
            hält_item=self.field(self.stone),
        )

    def boss_bar(self, name: str = "leiste", display_text: str = "hallo", value: float = 0.5) -> BaseModel:
        return bl.BossLeiste(
            name=name,
            anzeige_text=display_text,
            wert=value,
            stil=bl.BossLeisteStil.DURCHGEZOGEN,
            farbe=bl.BossLeisteFarben.BLAU,
        )

    def inventory(self, *fields: BaseModel) -> dict[int, BaseModel]:
        return de.Inventar({field.index: field for field in fields})


ENGLISH = English()
GERMAN = German()


@pytest.fixture(params=[ENGLISH, GERMAN], ids=lambda variant: variant.name)
def lang(request: pytest.FixtureRequest) -> Variant:
    """Makes every test using it run once per language variant"""
    return request.param


# --------------------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------------------


def assert_equal(left: object, right: object) -> None:
    """Asserts that both objects compare equal, in both directions and for both operators"""
    assert left == right, f"{left!r} == {right!r} should be True"
    assert right == left, f"{right!r} == {left!r} should be True (equality must be symmetric)"
    assert not left != right, f"{left!r} != {right!r} should be False"
    assert not right != left, f"{right!r} != {left!r} should be False"


def assert_not_equal(left: object, right: object) -> None:
    """Asserts that both objects do not compare equal, in both directions and for both operators"""
    assert not left == right, f"{left!r} == {right!r} should be False"
    assert not right == left, f"{right!r} == {left!r} should be False (equality must be symmetric)"
    assert left != right, f"{left!r} != {right!r} should be True"
    assert right != left, f"{right!r} != {left!r} should be True"


# --------------------------------------------------------------------------------------------------
# Item
# --------------------------------------------------------------------------------------------------


class TestItem:
    """An item is identified by its material and its display name"""

    def test_same_material_and_display_name(self, lang: Variant) -> None:
        assert_equal(lang.item(lang.stone), lang.item(lang.stone))

    def test_different_material(self, lang: Variant) -> None:
        assert_not_equal(lang.item(lang.stone), lang.item(lang.dirt))

    def test_different_display_name(self, lang: Variant) -> None:
        assert_not_equal(lang.item(lang.stone), lang.item(lang.stone, display_name="Etwas anderes"))

    def test_matching_material_member(self, lang: Variant) -> None:
        assert_equal(lang.item(lang.stone), lang.stone)

    def test_other_material_member(self, lang: Variant) -> None:
        assert_not_equal(lang.item(lang.stone), lang.dirt)

    @pytest.mark.parametrize("other", NOT_COMPARABLE_OR_STRING)
    def test_not_comparable_values(self, lang: Variant, other: object) -> None:
        assert_not_equal(lang.item(lang.stone), other)


# --------------------------------------------------------------------------------------------------
# InventoryField
# --------------------------------------------------------------------------------------------------


class TestInventoryField:
    """
    An inventory field is an item plus the position and the stack size it has in the inventory.

    Compared against another field all of that matters.
    Compared against a plain item only the item part matters, because an item carries no position.
    """

    def test_all_fields_identical(self, lang: Variant) -> None:
        assert_equal(lang.field(lang.stone, index=3, amount=12), lang.field(lang.stone, index=3, amount=12))

    def test_different_index(self, lang: Variant) -> None:
        assert_not_equal(lang.field(lang.stone, index=3), lang.field(lang.stone, index=4))

    def test_different_amount(self, lang: Variant) -> None:
        assert_not_equal(lang.field(lang.stone, amount=1), lang.field(lang.stone, amount=12))

    def test_different_material(self, lang: Variant) -> None:
        assert_not_equal(lang.field(lang.stone), lang.field(lang.dirt))

    def test_different_display_name(self, lang: Variant) -> None:
        assert_not_equal(lang.field(lang.stone), lang.field(lang.stone, display_name="Etwas anderes"))

    def test_item_with_same_material_and_display_name(self, lang: Variant) -> None:
        """Index and amount are ignored here, an item simply does not have them"""
        assert_equal(lang.field(lang.stone, index=7, amount=64), lang.item(lang.stone))

    def test_item_with_different_material(self, lang: Variant) -> None:
        assert_not_equal(lang.field(lang.stone), lang.item(lang.dirt))

    def test_matching_material_member(self, lang: Variant) -> None:
        assert_equal(lang.field(lang.stone), lang.stone)

    def test_other_material_member(self, lang: Variant) -> None:
        assert_not_equal(lang.field(lang.stone), lang.dirt)

    @pytest.mark.parametrize("other", NOT_COMPARABLE_OR_STRING)
    def test_not_comparable_values(self, lang: Variant, other: object) -> None:
        assert_not_equal(lang.field(lang.stone), other)


# --------------------------------------------------------------------------------------------------
# Inventory
# --------------------------------------------------------------------------------------------------


class TestInventoryContains:
    """The `in` operator on an inventory asks whether any field matches the given item"""

    def test_contains_matching_item(self, lang: Variant) -> None:
        inventory = lang.inventory(lang.field(lang.stone, index=3, amount=12))

        assert lang.item(lang.stone) in inventory

    def test_contains_matching_material_member(self, lang: Variant) -> None:
        inventory = lang.inventory(lang.field(lang.stone, index=3, amount=12))

        assert lang.stone in inventory

    def test_does_not_contain_other_item(self, lang: Variant) -> None:
        inventory = lang.inventory(lang.field(lang.stone))

        assert lang.item(lang.dirt) not in inventory

    def test_does_not_contain_other_material_member(self, lang: Variant) -> None:
        inventory = lang.inventory(lang.field(lang.stone))

        assert lang.dirt not in inventory

    def test_empty_inventory_contains_nothing(self, lang: Variant) -> None:
        assert lang.item(lang.stone) not in lang.inventory()

    def test_contains_taken_index(self, lang: Variant) -> None:
        """An index asks the inventory the same thing any other dict would be asked"""
        inventory = lang.inventory(lang.field(lang.stone, index=5))

        assert 5 in inventory

    def test_does_not_contain_free_index(self, lang: Variant) -> None:
        inventory = lang.inventory(lang.field(lang.stone, index=5))

        assert 7 not in inventory


# --------------------------------------------------------------------------------------------------
# Material
# --------------------------------------------------------------------------------------------------


class TestMaterial:
    """
    A block is identified by its material, its position and its dimension.

    Positions are compared as whole blocks, because a block occupies a whole coordinate.
    """

    def test_same_material_position_and_dimension(self, lang: Variant) -> None:
        assert_equal(lang.block(lang.stone, x=1.0, y=2.0, z=3.0), lang.block(lang.stone, x=1.0, y=2.0, z=3.0))

    def test_same_block_hit_at_different_fractions(self, lang: Variant) -> None:
        """Both positions floor to the same block, so they describe the same block"""
        assert_equal(lang.block(lang.stone, x=1.0, y=2.0, z=3.0), lang.block(lang.stone, x=1.7, y=2.2, z=3.9))

    def test_different_position(self, lang: Variant) -> None:
        assert_not_equal(lang.block(lang.stone, x=1.0), lang.block(lang.stone, x=9.0))

    def test_different_material(self, lang: Variant) -> None:
        assert_not_equal(lang.block(lang.stone), lang.block(lang.dirt))

    def test_different_dimension(self, lang: Variant) -> None:
        assert_not_equal(
            lang.block(lang.stone, dimension=Dimension.World),
            lang.block(lang.stone, dimension=Dimension.Nether),
        )

    def test_matching_material_member(self, lang: Variant) -> None:
        assert_equal(lang.block(lang.stone), lang.stone)

    def test_other_material_member(self, lang: Variant) -> None:
        assert_not_equal(lang.block(lang.stone), lang.dirt)

    def test_unknown_material_at_same_position(self, lang: Variant) -> None:
        """An unknown material is still a block at a position"""
        assert_equal(lang.block(None, x=1.0), lang.block(None, x=1.0))

    def test_unknown_material_at_different_position(self, lang: Variant) -> None:
        assert_not_equal(lang.block(None, x=1.0), lang.block(None, x=5.0))

    def test_unknown_material_against_known_one(self, lang: Variant) -> None:
        assert_not_equal(lang.block(None, x=1.0), lang.block(lang.stone, x=1.0))

    @pytest.mark.parametrize("other", NOT_COMPARABLE_OR_STRING)
    def test_not_comparable_values(self, lang: Variant, other: object) -> None:
        assert_not_equal(lang.block(lang.stone), other)


# --------------------------------------------------------------------------------------------------
# Entity
# --------------------------------------------------------------------------------------------------


class TestEntity:
    """
    An entity is identified by its id, which the server guarantees to be unique.

    Without an id there is nothing to identify it by, so it is not considered equal to anything.
    """

    def test_same_id(self, lang: Variant) -> None:
        assert_equal(lang.entity(lang.pig), lang.entity(lang.pig))

    def test_different_id(self, lang: Variant) -> None:
        assert_not_equal(lang.entity(lang.pig, entity_id="a"), lang.entity(lang.pig, entity_id="b"))

    def test_same_id_but_renamed(self, lang: Variant) -> None:
        """The id identifies the entity, a renamed entity is still the same entity"""
        assert_equal(lang.entity(lang.pig, name="Rosa"), lang.entity(lang.pig, name="Berta"))

    def test_matching_species_member(self, lang: Variant) -> None:
        assert_equal(lang.entity(lang.pig), lang.pig)

    def test_other_species_member(self, lang: Variant) -> None:
        assert_not_equal(lang.entity(lang.pig), lang.cow)

    def test_without_id_and_otherwise_identical(self, lang: Variant) -> None:
        """Without an id neither entity can be identified, so they must not claim to be the same"""
        assert_not_equal(lang.entity(lang.pig, entity_id=None), lang.entity(lang.pig, entity_id=None))

    def test_without_id_but_different_species(self, lang: Variant) -> None:
        """A pig is never a cow, no matter how little else is known about either"""
        assert_not_equal(lang.entity(lang.pig, entity_id=None), lang.entity(lang.cow, entity_id=None))

    def test_without_id_but_different_position(self, lang: Variant) -> None:
        """Two unidentified pigs standing apart are two different pigs"""
        assert_not_equal(
            lang.entity(lang.pig, entity_id=None, x=1.0),
            lang.entity(lang.pig, entity_id=None, x=9.0),
        )

    @pytest.mark.parametrize("other", NOT_COMPARABLE_OR_STRING)
    def test_not_comparable_values(self, lang: Variant, other: object) -> None:
        assert_not_equal(lang.entity(lang.pig), other)


# --------------------------------------------------------------------------------------------------
# Message
# --------------------------------------------------------------------------------------------------


class TestMessage:
    """
    A message is identified by its text, its sender and the time it was sent.

    The sender name is skipped on purpose, it is just another identifier for the same sender id.
    """

    def test_same_text_sender_and_time(self, lang: Variant) -> None:
        assert_equal(lang.message(), lang.message())

    def test_different_sender_name_only(self, lang: Variant) -> None:
        assert_equal(lang.message(sender_name="chris"), lang.message(sender_name="adrian"))

    def test_different_text(self, lang: Variant) -> None:
        assert_not_equal(lang.message(text="hallo"), lang.message(text="tschuess"))

    def test_different_sender_id(self, lang: Variant) -> None:
        assert_not_equal(lang.message(sender_id=1), lang.message(sender_id=2))

    def test_different_time(self, lang: Variant) -> None:
        assert_not_equal(lang.message(sent_at=SENT_AT), lang.message(sent_at=LATER))

    def test_matching_text_as_string(self, lang: Variant) -> None:
        """Comparing against a string asks whether the message says exactly that"""
        assert_equal(lang.message(text="hallo"), "hallo")

    def test_other_text_as_string(self, lang: Variant) -> None:
        assert_not_equal(lang.message(text="hallo"), "tschuess")

    @pytest.mark.parametrize("other", NOT_COMPARABLE)
    def test_not_comparable_values(self, lang: Variant, other: object) -> None:
        assert_not_equal(lang.message(), other)


# --------------------------------------------------------------------------------------------------
# Player
# --------------------------------------------------------------------------------------------------


class TestPlayer:
    """
    A player is compared field by field, except against a string, which asks for the name.

    Whether a player should rather be identified by its id is still open.
    """

    def test_same_fields(self, lang: Variant) -> None:
        assert_equal(lang.player(), lang.player())

    def test_different_id(self, lang: Variant) -> None:
        assert_not_equal(lang.player(player_id=1), lang.player(player_id=2))

    def test_different_name(self, lang: Variant) -> None:
        assert_not_equal(lang.player(name="chris"), lang.player(name="adrian"))

    def test_different_position(self, lang: Variant) -> None:
        """The same player having moved is a different snapshot of that player"""
        assert_not_equal(lang.player(x=0.0), lang.player(x=10.0))

    def test_matching_name_as_string(self, lang: Variant) -> None:
        """Comparing against a string asks whether the player goes by that name"""
        assert_equal(lang.player(name="chris"), "chris")

    def test_other_name_as_string(self, lang: Variant) -> None:
        assert_not_equal(lang.player(name="chris"), "adrian")

    @pytest.mark.parametrize("other", NOT_COMPARABLE)
    def test_not_comparable_values(self, lang: Variant, other: object) -> None:
        assert_not_equal(lang.player(), other)


# --------------------------------------------------------------------------------------------------
# BossBar
# --------------------------------------------------------------------------------------------------


class TestBossBar:
    """A boss bar is compared field by field, it has no comparison of its own"""

    def test_same_fields(self, lang: Variant) -> None:
        assert_equal(lang.boss_bar(), lang.boss_bar())

    def test_different_name(self, lang: Variant) -> None:
        assert_not_equal(lang.boss_bar(name="erste"), lang.boss_bar(name="zweite"))

    def test_different_value(self, lang: Variant) -> None:
        assert_not_equal(lang.boss_bar(value=0.5), lang.boss_bar(value=0.9))

    @pytest.mark.parametrize("other", NOT_COMPARABLE_OR_STRING)
    def test_not_comparable_values(self, lang: Variant, other: object) -> None:
        assert_not_equal(lang.boss_bar(), other)
