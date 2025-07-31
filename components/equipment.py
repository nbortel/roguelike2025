from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, parts: List[Item] = [], max_parts: int = 3):
        self.parts = parts
        self.max_parts = max_parts

    @property
    def avoidance_bonus(self) -> int:
        bonus = 0

        for part in self.parts:
            if part.equippable is not None:
                bonus += part.equippable.avoidance_bonus

        return bonus

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        for part in self.parts:
            if part.equippable is not None:
                bonus += part.equippable.defense_bonus

        return bonus

    @property
    def dice_count_bonus(self) -> int:
        bonus = 0

        for part in self.parts:
            if part.equippable is not None:
                bonus += part.equippable.dice_count_bonus

        return bonus

    @property
    def dice_sides_bonus(self) -> int:
        bonus = 0

        for part in self.parts:
            if part.equippable is not None:
                bonus += part.equippable.dice_sides_bonus

        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0

        for part in self.parts:
            if part.equippable is not None:
                bonus += part.equippable.power_bonus

        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        for part in self.parts:
            if part == item:
                return True
        return False

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip(self, item: Item, add_message: bool) -> None:
        if len(self.parts) >= self.max_parts:
            raise Impossible("No space for more parts. Remove one.")
        if self.item_is_equipped(item):
            raise Impossible("This part is already equipped.")

        self.parts.append(item)

        # Add bonus health if the item conveys it
        if item.equippable.health_bonus > 0:
            self.parent.fighter.max_hp += item.equippable.health_bonus

        if add_message:
            self.equip_message(item.name)

    def unequip(self, item: Item, add_message: bool) -> None:
        if not self.item_is_equipped(item):
            raise Impossible("This part is not equipped. Cannot unequip.")

        if add_message:
            self.unequip_message(item.name)

        # Remove health bonus if item was conveying it
        if item.equippable.health_bonus > 0:
            self.parent.fighter.max_hp -= item.equippable.health_bonus

        self.parts.remove(item)

    def toggle_equip(self, item: Item, add_message: bool = True) -> None:
        if not self.item_is_equipped(item):
            self.equip(item, True)
        else:
            self.unequip(item, True)
