from typing import TYPE_CHECKING, Optional
from BaseClasses import CollectionState, Location
from . import Items
from . import Locations
from . import Options

import re

if TYPE_CHECKING:
    from . import CoQWorld

def levelup_levels(max_level: int) -> list[int]:
    return [l for l in range(2, max_level + 1)]

def stat_items_total(max_level: int) -> int:
    return sum([len(Items.stat_items_on_levelup(l)) for l in levelup_levels(max_level)])

def stat_items_count(state: CollectionState, player: int) -> int:
    return sum([state.count(item, player) for item in Items.get_items_by_category("Stats").keys()])

def set_rules(world: "CoQWorld"):
    prev_step: Optional[Location] = None
    for name in Locations.main_quests:
        step = world.get_location(name)
        print(step, "---", prev_step)
        step.access_rule = lambda state, p=prev_step: p in state.locations_checked if p != None else True
        prev_step = step

    level_loc_expr = re.compile(r'Level (\d+)')
    for name in Locations.xp_locations(world.options.max_level, world.options.locations_per_level):
        level_match = level_loc_expr.match(name)
        assert(level_match != None)

        level = int(level_match.group(1))
        assert(level)

        step = world.get_location(name)
        step.access_rule = lambda state, level=level:\
            stat_items_count(state, world.player) / stat_items_total(world.options.max_level)\
            >= level / world.options.max_level

    victory_loc = world.get_location(Options.goal_lookup[world.options.goal])
    world.multiworld.completion_condition[world.player] = lambda state: victory_loc in state.locations_checked