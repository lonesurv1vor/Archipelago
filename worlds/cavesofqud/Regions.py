from typing import TYPE_CHECKING, Iterable
from BaseClasses import CollectionState, LocationProgressType, Region

from . import Quests
from . import Locations
from . import Items
from . import Options

if TYPE_CHECKING:
    from . import CoQWorld

def levelup_levels(max_level: int) -> list[int]:
    return [l for l in range(2, max_level + 1)]

def stat_items_total(max_level: int) -> int:
    return sum([len(Items.stat_items_on_levelup(l)) for l in levelup_levels(max_level)])

def stat_items_count(state: CollectionState, player: int) -> int:
    return sum([state.count(item, player) for item in Items.stat_items])

def has_enough_stats_for_level(level: int, state: CollectionState, world: "CoQWorld") -> bool:
    return stat_items_count(state, world.player) / stat_items_total(Quests.max_level(world)) >= (level - 1) / Quests.max_level(world)

def add_level_locations(frm: int, to: int, world: "CoQWorld", region: Region):
    for loc_name in Locations.xp_locations(frm, to, world.options.locations_per_level):
        level_loc = Locations.CoQLocation(world.player, loc_name, world.location_name_to_id[loc_name], region)
        region.locations += [level_loc]

def create_regions(world: "CoQWorld"):
    menu = Region("Menu", world.player, world.multiworld)

    # Instant access to the first levels
    prev_req_level: int = next(iter(Quests.main_quests_table.items()))[1] # Req. level of first quest
    add_level_locations(1, prev_req_level + 1, world, menu)

    world.multiworld.regions += [menu]

    # Main Quest Regions
    prev_region = menu
    for name in Quests.main_quests(world):
        req_level = Quests.main_quests_table[name]
        unlock_item = Quests.quest_unlock_item(name)

        region = Region(name, world.player, world.multiworld)
        quest_loc = Locations.CoQLocation(world.player, name, world.location_name_to_id[name], region)
        quest_loc.progress_type = LocationProgressType.PRIORITY
        region.locations += [quest_loc]

        add_level_locations(prev_req_level + 1, req_level + 1, world, region)

        # Chain them together
        prev_region.connect(region, None , lambda state, unlock_item=unlock_item, prev_region=prev_region, prev_req_level=prev_req_level:
            has_enough_stats_for_level(prev_req_level, state, world) and state.has(unlock_item, world.player))

        world.multiworld.regions += [region]
        prev_region = region
        prev_req_level = req_level

    # Add rest of the XP locations
    add_level_locations(prev_req_level + 1, Quests.max_level(world) + 1, world, prev_region)

    # TMP add all delivery quests randomly
    for q in [k for k in Locations.static_locations if k.type == "delivery"]:
        loc = Locations.CoQLocation(world.player, q.name, world.location_name_to_id[q.name], region)
        region = world.random.choice(list(world.multiworld.regions))
        region.locations += [loc]

    # Side Quest Region TODO
    region = Region("Side Quests", world.player, world.multiworld)
    for q in Quests.side_quests:
        for name in q:
            loc = Locations.CoQLocation(world.player, name, world.location_name_to_id[name], region)
            loc.progress_type = LocationProgressType.EXCLUDED # TODO REMOVE
            region.locations += [loc]
    menu.connect(region) 
    world.multiworld.regions += [region]
