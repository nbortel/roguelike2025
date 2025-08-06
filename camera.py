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

    def __init__(
            self, engine: Engine,
            position: Tuple[int, int] = (0, 0),
            width: int = 60, height: int = 40
    ):
        self.engine = engine
        self.width = width
        self.height = height
        self._position = position
        self.console = tcod.console.Console(
                width=width, height=height, order='F')

    @property
    def gamemap(self) -> Optional[GameMap]:
        return self.engine.game_map

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

    def render(self, dx: int = 0, dy: int = 0):
        """Renders a subset of the game map defined by position, width, and
        to the Camera's console. Additionally render entities within the
        camera area."""
        if dx == 0 and dy == 0:  # update the entire viewport if no delta
            # Ranges for the subset of gamemap we want to capture
            slice_x = (self.position[0], self.position[0] + self.width)
            slice_y = (self.position[1], self.position[1] + self.height)

            self.console.rgb[0:self.width, 0:self.height] = np.select(
                    condlist=[
                        self.gamemap.visible[
                            slice_x[0]:slice_x[1], slice_y[0]:slice_y[1]],
                        self.gamemap.explored[
                            slice_x[0]:slice_x[1], slice_y[0]:slice_y[1]],
                    ],
                    choicelist=[
                        self.gamemap.tiles[
                            slice_x[0]:slice_x[1],
                            slice_y[0]:slice_y[1]]["light"],
                        self.gamemap.tiles[
                            slice_x[0]:slice_x[1],
                            slice_y[0]:slice_y[1]]["dark"],
                    ],
                    default=tile_types.SHROUD
            )
        else:
            if dx > 0:  # TODO: Finish this!
                self.console.rgb = np.delete(self.console.rgb, range(0, dx), axis=1)
                pass
            elif dx < 0:
                pass
            if dy > 0:
                pass
            elif dy < 0:
                pass

        entities_sorted_for_rendering = sorted(
            self.gamemap.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            entity_camera_x = entity.x - self.position[0]
            entity_camera_y = entity.y - self.position[1]
            # Skip entities that are outside the camera
            if (entity_camera_x < 0 or entity_camera_y < 0
                    or entity_camera_x > self.width - 1
                    or entity_camera_y > self.height - 1):
                continue
            # Only print entities that are in the FOV
            if self.gamemap.visible[entity.x, entity.y]:
                self.console.print(
                    x=entity_camera_x, y=entity_camera_y,
                    string=entity.char, fg=entity.color
                )
