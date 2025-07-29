from __future__ import annotations

from typing import TYPE_CHECKING


from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        avoidance_bonus: int = 0,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        dice_count_bonus: int = 0,
        dice_sides_bonus: int = 0,
    ):
        self.equipment_type = equipment_type

        self.avoidance_bonus = avoidance_bonus
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.dice_count_bonus = dice_count_bonus
        self.dice_sides_bonus = dice_sides_bonus


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)
