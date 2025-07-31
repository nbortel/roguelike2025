from actor_groups import ActorGroups
from components.ai import AlliedFollower, HostileEnemy
from components import consumable, part
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    group=ActorGroups.ALLIES,
    equipment=Equipment(),
    fighter=Fighter(
        hp=30, base_avoidance=2, base_defense=1, base_power=2,
        base_dice_count=1, base_dice_sides=3),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)
"""ACTORS"""
allied_dummy = Actor(
    char="d",
    color=(255, 255, 255),
    name="Friendly Dummy",
    group=ActorGroups.ALLIES,
    ai_cls=AlliedFollower,
    equipment=Equipment(),
    fighter=Fighter(
        hp=15, base_avoidance=0, base_defense=1, base_power=2,
        base_dice_count=1, base_dice_sides=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0)
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_avoidance=1, base_defense=0, base_power=1,
                    base_dice_count=1, base_dice_sides=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_avoidance=1, base_defense=1, base_power=4,
                    base_dice_count=1, base_dice_sides=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)
"""CONSUMABLE ITEMS"""
scrambler = Item(
    char="~",
    color=(207, 63, 255),
    name="Scrambler",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

# TODO: Reflavor
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

# TODO: Reflavor
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

# TODO: Reflavor
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5)
)
"""PART ITEMS"""
capacitor = Item(
    char="*", color=(150, 0, 150), name="Capacitor",
    equippable=part.Capacitor()
)
armored_plating = Item(
    char="*", color=(150, 0, 150), name="Armored Plating",
    equippable=part.ArmoredPlating()
)
thrusters = Item(
    char="*", color=(150, 0, 150), name="Thrusters",
    equippable=part.Thrusters()
)
servos = Item(
    char="*", color=(150, 0, 150), name="Servos",
    equippable=part.Servos()
)
