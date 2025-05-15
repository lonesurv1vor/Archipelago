from typing import Dict, NamedTuple, Optional
from BaseClasses import Location
from . import Options


class CoQLocation(Location):
    game: str = "Caves of Qud"

class CoQLocationData(NamedTuple):
    category: str
    id: Optional[int] = None

def level_locations(max_level: int, per_level: int) -> list[tuple[int, int]]:
    locs = []
    if(max_level > 1):
        for l in range(1, max_level):
            for s in range(0, per_level):
                locs.append((l, s))
        # We start at level 1.0, so remove first element
        locs = locs[1:]
        # We end at level maxlevel.0, so add last element
        locs.append((max_level, 0))
    return locs

def level_location_name(level: int, step: int) -> str:
    return f"Level {level}.{step}"
            
location_table: Dict[str, CoQLocationData] = {
    # Quests
    "Quest: Fetch Argyve a Knickknack":                  CoQLocationData("Quest", 1),
    "Quest: Fetch Argyve Another Knickknack":            CoQLocationData("Quest", 2),
    "Quest: Weirdwire Conduit... Eureka!":               CoQLocationData("Quest", 3),
    "Quest: A Canticle for Barathrum":                   CoQLocationData("Quest", 4),
    "Quest: More Than a Willing Spirit":                 CoQLocationData("Quest", 5),
    "Quest: Decoding the Signal":                        CoQLocationData("Quest", 6),

    "Quest: O Glorious Shekhinah!":                      CoQLocationData("Quest", 7),
    "Quest: What's Eating the Watervine?":               CoQLocationData("Quest", 8),
    "Quest: Raising Indrix":                             CoQLocationData("Quest", 9),

    # XP Gain / Level up
    **{level_location_name(l,s): CoQLocationData("XP",  1000 + l*10 + s) for (l,s) in level_locations(Options.MAX_MAX_LEVEL, Options.MAX_LOCATIONS_PER_LEVEL)},
}
