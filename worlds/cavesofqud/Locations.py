import itertools
from typing import Iterable
from BaseClasses import Location
from . import Options


class CoQLocation(Location):
    game: str = "Caves of Qud"

main_quests: list[str] = [
    "Fetch Argyve a Knickknack - Find a Knickknack",
    "Fetch Argyve a Knickknack - Return to Argyve",

    "Fetch Argyve Another Knickknack - Find Another Knickknack",
    "Fetch Argyve Another Knickknack - Return to Argyve",
    "Weirdwire Conduit... Eureka! - Find 200 Feet of Wire",
    "Weirdwire Conduit... Eureka! - Return to Argyve",

    "A Canticle for Barathrum - Travel to Grit Gate",
    "A Canticle for Barathrum - Locate the Barathrumite Enclave" ,
    "A Canticle for Barathrum - Speak with the Barathrumites",

    "More Than a Willing Spirit - Travel to Golgotha",
    "More Than a Willing Spirit - Find a Dysfunctional Waydroid",
    "More Than a Willing Spirit - Repair the Waydroid",
    "More Than a Willing Spirit - Return to Grit Gate",
    "Decoding the Signal - Get Q Girl's Instructions onto the Data Disk",
    "Decoding the Signal - Locate the Mechanimist Compound at Bethesda Susa",
    "Decoding the Signal - Decode the Signal",
    "Decoding the Signal - Return to Grit Gate",
]

side_quests: list[list[str]] = [[
        "What's Eating the Watervine? - Travel to Red Rock",
        "What's Eating the Watervine? - Find the Vermin",
        "What's Eating the Watervine? - Get a Corpse",
        "What's Eating the Watervine? - Return with the Corpse",
    ],[
        "O Glorious Shekhinah! - Make a Pilgrimage to the Six Day Stilt",
    ],[
        "Raising Indrix - Find Mamon Souldrinker",
        "Raising Indrix - Recover the Amaranthine Prism"
    ]
]

def _split_levels(max_level: int, per_level: int) -> Iterable[tuple[int, int]]:
    if(max_level > 1):
        for l in range(1, max_level):
            for s in range(0, per_level):
                # We start at level 1.0, so skip first element
                if l == 1 and s == 0:
                    continue
                yield (l, s)
        # We end at level maxlevel.0, so include last element
        yield (max_level, 0)

def xp_locations(max_level: int, max_locations_per_level: int) -> Iterable[str]:
    yield from [f"Level {level}.{step}" for (level, step) in _split_levels(max_level, max_locations_per_level)]

all_locations: Iterable[str] = itertools.chain(
    main_quests,
    *side_quests,
    xp_locations(Options.MAX_MAX_LEVEL, Options.MAX_LOCATIONS_PER_LEVEL),
)

# Early game?

# Deliver 5 bear jerky
# Deliver 5 croc jerky
# Deliver 5 crab jerky
# Deliver 5 boar jerky
# Deliver 5 goat jerky

# mid game

# Deliver 1 congealed blaze
# Deliver 1 congealed hulk honey
# Deliver 1 congealed love
# Deliver 1 congealed rubbergum
# Deliver 1 congealed salve
# Deliver 1 congealed shade oil

# Find x lead slugs / shotgun shells / boomrose arrow / carbide arrow/ steel arrow / HE Missile
# Find injectors
# Find liquids
# Find artifacts: metal folding chair, plastic tree
# glowsphere, floating glowsphere

# Kill crocodiles, snapjaws, baboons