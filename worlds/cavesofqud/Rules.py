from typing import TYPE_CHECKING
from BaseClasses import CollectionState
from . import Items

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
    level_loc_expr = re.compile(r'Level (\d+)')
    for loc in world.get_locations():
        level_match = level_loc_expr.match(loc.name)
        if level_match == None:
            continue

        level = int(level_match.group(1))
        if level:
            loc.access_rule = lambda state, level=level:\
                stat_items_count(state, world.player) / stat_items_total(world.options.max_level)\
                >= level / world.options.max_level