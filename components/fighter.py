from __future__ import annotations

from typing import Optional, TYPE_CHECKING
import random

import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


DEFENSE_ROLL_CHANCE = 0.10


def calculate_if_attack_avoided(avoidance: int) -> bool:
    avoid_chance = ((float(avoidance)/(float(avoidance) + 10.0)) * 0.75)
    if random.random() <= avoid_chance:
        return True
    return False


def calculate_reduction_from_defense(damage: int, defense: int) -> int:
    number_of_defense_rolls = max(0, defense - damage)
    if number_of_defense_rolls == 0:
        return 0
    damage_received: int = damage
    for i in range(number_of_defense_rolls):
        if random.random() <= DEFENSE_ROLL_CHANCE:
            damage_received -= 1
    return damage_received


class Fighter(BaseComponent):
    parent: Actor

    def __init__(
            self, hp: int, base_avoidance: int, base_defense: int,
            base_power: int, base_dice_count: int, base_dice_sides: int):
        self.max_hp = hp
        self._hp = hp
        self.base_avoidance = base_avoidance
        self.base_defense = base_defense
        self.base_power = base_power
        self.base_dice_count = base_dice_count
        self.base_dice_sides = base_dice_sides

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def attack_string(self) -> str:
        return f"{self.dice_count}d{self.dice_sides}+{self.power}"

    @property
    def avoidance(self) -> int:
        return self.base_avoidance + self.avoidance_bonus

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def dice_count(self) -> int:
        return self.base_dice_count + self.dice_count_bonus

    @property
    def dice_sides(self) -> int:
        return self.base_dice_sides + self.dice_sides_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def avoidance_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.avoidance_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def dice_count_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.dice_count_bonus
        else:
            return 0

    @property
    def dice_sides_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.dice_sides_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    def attack(self) -> int:
        total_damage = 0
        for i in range(self.dice_count):
            total_damage += random.randint(1, self.dice_sides)
        total_damage += self.power
        return total_damage

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> Optional[int]:
        """Calculate damage taken, first checking for avoidance."""
        # Check if damage avoided
        if calculate_if_attack_avoided(self.avoidance):
            return None
        reduction = calculate_reduction_from_defense(amount, self.defense)
        damage_taken = max(0, amount - reduction)
        self.hp -= damage_taken
        return damage_taken
