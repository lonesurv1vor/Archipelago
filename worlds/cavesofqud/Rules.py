from typing import TYPE_CHECKING, Optional
from BaseClasses import CollectionState, Location
from . import Items
from . import Locations
from . import Options
from . import Quests


if TYPE_CHECKING:
    from . import CoQWorld

def set_rules(world: "CoQWorld"):
    victory_loc = world.get_location(Quests.goal_lookup[world.options.goal])
    world.multiworld.completion_condition[world.player] = lambda state: victory_loc in state.locations_checked

    # from Utils import visualize_regions
    # visualize_regions(world.multiworld.get_region("Menu", world.player), "D:/APData/my_world.puml")