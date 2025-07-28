from __future__ import annotations

from enum import auto, Enum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Actor


class ActorGroups(Enum):
    ALLIES = auto()
    ENEMIES = auto()


def select_group_from_list(
        actors: List[Actor], group: ActorGroups) -> List[Actor]:
    sublist = []
    for actor in actors:
        if actor.group == group:
            sublist += [actor]
    return sublist
