from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from camera import Camera
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

        self.camera = Camera(self)
        self.camera.parent = self

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI

    def update_fov(self) -> None:
        """Recompute the visble area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        # self.game_map.render(console)
        camera_position_x = min(
                self.game_map.width - self.camera.width,
                max(0, self.player.x - int(self.camera.width / 2))
        )
        camera_position_y = min(
                self.game_map.height - self.camera.height,
                max(0, self.player.y - int(self.camera.height / 2))
        )
        self.camera.position = (camera_position_x, camera_position_y)
        self.camera.render()
        self.camera.console.blit(console)

        render_functions.render_debug_info(
                x=60, y=0, console=console, engine=self)

        self.message_log.render(
                console=console, x=21, y=42, width=50, height=8
        )

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_duneon_level(
                console=console,
                dungeon_level=self.game_world.current_floor,
                location=(0, 47),
        )

        render_functions.render_names_at_location(
                console=console, x=21, y=41, engine=self)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
