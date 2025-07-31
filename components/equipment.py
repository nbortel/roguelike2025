from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(
            self, weapon: Optional[Item] = None, armor: Optional[Item] = None,
            part: Optional[Item] = None):
        self.weapon = weapon
        self.armor = armor
        self.part = part

    @property
    def avoidance_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.avoidance_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.avoidance_bonus

        if self.part is not None and self.part.equippable is not None:
            bonus += self.part.equippable.avoidance_bonus

        return bonus

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.defense_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.defense_bonus

        if self.part is not None and self.part.equippable is not None:
            bonus += self.part.equippable.defense_bonus

        return bonus

    @property
    def dice_count_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.dice_count_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.dice_count_bonus

        if self.part is not None and self.part.equippable is not None:
            bonus += self.part.equippable.dice_count_bonus

        return bonus

    @property
    def dice_sides_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.dice_sides_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.dice_sides_bonus

        if self.part is not None and self.part.equippable is not None:
            bonus += self.part.equippable.dice_sides_bonus

        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.power_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.defense_bonus

        if self.part is not None and self.part.equippable is not None:
            bonus += self.part.equippable.power_bonus

        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.weapon == item or self.armor == item or self.part == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        # Add bonus health if the item conveys it
        if item.equippable.health_bonus > 0:
            self.parent.fighter.max_hp += item.equippable.health_bonus

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        # Remove health bonus if item was conveying it
        if current_item.equippable.health_bonus > 0:
            self.parent.fighter.max_hp -= current_item.equippable.health_bonus

        setattr(self, slot, None)

    def toggle_equip(
            self, equippable_item: Item, add_message: bool = True) -> None:
        if (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
        ):
            slot = "weapon"
        elif equippable_item.equippable.equipment_type == EquipmentType.PART:
            slot = "part"
        else:
            slot = "armor"

        if getattr(self, slot) == equippable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)
