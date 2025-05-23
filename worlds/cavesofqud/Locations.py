import itertools
import json
from typing import Iterable, NamedTuple
from BaseClasses import Location
from . import Options
from . import Quests
import pkgutil

class CoQLocation(Location):
    game: str = "Caves of Qud"

class CoqLocationData(NamedTuple):
    name: str
    type: str
    min_level: int | None = None
    max_level: int | None = None

location_data = pkgutil.get_data(__name__, "data/Locations.json")
static_locations = [CoqLocationData(
    name = loc["name"],
    type = loc["type"],
    min_level = loc["minLevel"] if "minLevel" in loc else 1,
    max_level = loc["maxLevel"] if "maxLevel" in loc else Options.MAX_MAX_LEVEL,
) for loc in json.loads(location_data)]

def xp_locations(frm: int, to: int, per_level: int) -> Iterable[str]:
    assert(frm >= 1)
    assert(to <= Options.MAX_MAX_LEVEL)
    assert(per_level <= Options.MAX_LOCATIONS_PER_LEVEL)

    for level in range(frm, to):
        for step in range(0, per_level):
            # We start at level 1.0, so skip first element
            if level == 1 and step == 0:
                continue
            yield f"Level {level}.{step}"

all_locations: Iterable[str] = itertools.chain(
    Quests.main_quests_table.keys(),
    *Quests.side_quests,
    [i.name for i in static_locations],
    xp_locations(1, Options.MAX_MAX_LEVEL, Options.MAX_LOCATIONS_PER_LEVEL),
)

# Plastic Treem FLoating Glowsphere