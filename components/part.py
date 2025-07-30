from __future__ import annotations

from components.equippable import Equippable
from equipment_types import EquipmentType


class Capacitor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.PART, health_bonus=10)


class ArmoredPlating(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.PART, defense_bonus=4)


class Thrusters(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.PART, avoidance_bonus=2)


class Servos(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.PART, dice_count_bonus=1)
