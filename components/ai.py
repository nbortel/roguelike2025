from __future__ import annotations

import random
from typing import List, Optional, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod
from tcod.map import compute_fov

from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction
from actor_groups import ActorGroups, select_group_from_list

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path an empty list is returned.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an entity blocks movement and cost isn't 0 (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind eachother
                # A higher number means enemies will take longer paths in order
                # to surround
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a
        # new pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position

        # Compute the path to the destination and remove the starting point
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]

    def get_actors_in_fov(self, fov_radius: int = 8) -> List[Actor]:
        actor_list = []
        fov_mask = compute_fov(
                self.entity.parent.tiles["transparent"],
                (self.entity.x, self.entity.y),
                radius=fov_radius,
        )
        iterator = np.nditer(fov_mask, flags=["multi_index"])
        for value in iterator:
            if value:
                x, y = iterator.multi_index
                actor = self.entity.gamemap.get_actor_at_location(x, y)
                if actor and actor is not self.entity:
                    actor_list += [actor]
        return actor_list

    def get_distance_to_target_actor(self, actor: Actor) -> int:
        """Calculate chebyshev distance bewteen self and target."""
        dx, dy = self.entity.x - actor.x, self.entity.y - actor.y
        return max(abs(dx), abs(dy))


class ConfusedEnemy(BaseAI):
    """ A confused enemy will stumble around aimlessly for a given number of
    turns, then revert back to its previous AI. If an actor occupies a tile
    it is randomly moving into, it will attack."""

    def __init__(
            self, entity: Actor,
            previous_ai: Optional[BaseAI], turns_remaining: int
    ):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        """Revert the AI back o the original state if the effect has run its
        course."""
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                    f"The {self.entity.name} is no longer confused."
            )
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice([
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
            ])
            self.turns_remaining -= 1

            """The actor will either try to move or attack in the chosen
            random direction. Its possible the actor will just bump into a
            wall, wasting a turn."""
            return BumpAction(self.entity, direction_x, direction_y).perform()


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target_list = select_group_from_list(
                super().get_actors_in_fov(), ActorGroups.ALLIES)
        closest_target: Actor = None
        if target_list:
            closest_target = target_list[0]
        for target in target_list:
            if (super().get_distance_to_target_actor(target) <
                    super().get_distance_to_target_actor(closest_target)):
                closest_target = target
        if not closest_target:
            return WaitAction(self.entity).perform()

        target = closest_target
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = super().get_distance_to_target_actor(target)

        if distance <= 1:
            return MeleeAction(self.entity, dx, dy).perform()

        self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()


class AlliedFollower(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target_list = select_group_from_list(
                super().get_actors_in_fov(), ActorGroups.ENEMIES)
        closest_target: Actor = None
        if target_list:
            closest_target = target_list[0]
        for target in target_list:
            if (super().get_distance_to_target_actor(target) <
                    super().get_distance_to_target_actor(closest_target)):
                closest_target = target
        if not closest_target:
            target = self.engine.player
        else:
            target = closest_target

        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if distance <= 1:
            if target.group == ActorGroups.ENEMIES:
                return MeleeAction(self.entity, dx, dy).perform()
            return WaitAction(self.entity).perform()
        self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()
