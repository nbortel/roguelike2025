from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine


class Camera:
    """
    An object which holds the sub-console the game world is rendered to and
    related functionality.
    """

    parent: Engine

    def __init__(
            self,
            position: Tuple[int, int] = (0, 0),
            width: int = 60, height: int = 40
    ):
        self.width = width
        self.height = height
        self._position = position
        self.console = tcod.console.Console(
                width=width, height=height, order='F')

    @property
    def gamemap(self) -> Optional[GameMap]:
        return self.parent.game_map

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    @position.setter
    def position(self, new_position: Tuple[int, int]):
        new_x = new_position[0]
        new_y = new_position[1]
        if new_x < 0:
            new_x = 0
        elif new_x + self.width >= self.gamemap.width:
            new_x = self.gamemap.width - self.width
        if new_y < 0:
            new_y = 0
        elif new_y + self.height >= self.gamemap.height:
            new_y = self.gamemap.height - self.height

        self._position = (new_x, new_y)

    def render(self):
        """Renders a subset of the game map defined by position, width, and
        to the Camera's console."""
        # Ranges for the subset of gamemap we want to capture
        slice_x = (self.position[0], self.position[0] + self.width)
        slice_y = (self.position[1], self.position[1] + self.height)

        # Copy the subset of the gamemap arrays indicated by slices
        visible = self.gamemap.visible[slice_x[0]:slice_x[1],
                                       slice_y[0]:slice_y[1]].copy()
        explored = self.gamemap.explored[slice_x[0]:slice_x[1],
                                         slice_y[0]:slice_y[1]].copy()
        tiles = self.gamemap.tiles[slice_x[0]:slice_x[1],
                                   slice_y[0]:slice_y[1]].copy()

        self.console.rgb[0:self.width, 0:self.height] = np.select(
                condlist=[visible, explored],
                choicelist=[tiles["light"], tiles["dark"]],
                default=tile_types.SHROUD
        )

        entities_sorted_for_rendering = sorted(
            self.gamemap.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            entity_adjust_x = entity.x - self.position[0]
            entity_adjust_y = entity.y - self.position[1]
            # Skip entities that are outside the camera
            if (entity_adjust_x < 0 or entity_adjust_y < 0
                    or entity_adjust_x > self.width - 1
                    or entity_adjust_y > self.height - 1):
                continue
            # Only print entities that are in the FOV
            if visible[entity_adjust_x, entity_adjust_y]:
                self.console.print(
                    x=entity_adjust_x, y=entity_adjust_y,
                    string=entity.char, fg=entity.color
                )
