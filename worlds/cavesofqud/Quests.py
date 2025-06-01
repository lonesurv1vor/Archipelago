from collections import deque
import itertools
from typing import TYPE_CHECKING, Dict, Iterable, NamedTuple
from BaseClasses import Location

from . import Options

if TYPE_CHECKING:
    from . import CoQWorld

# This defines the general progress through levels and main quest steps
# (Level required, main quest name)
# The values are oriented on the quests in game level recommendation from Quests.xml
# This is a dict but the entries must be made in correct order. And it requires python 3.7 to retain the order.
main_quests_table: Dict[str, int] = {
    "Fetch Argyve a Knickknack~Find a Knickknack": 3,
    "Fetch Argyve a Knickknack~Return to Argyve": 3,

    "Fetch Argyve Another Knickknack~Find Another Knickknack": 5,
    "Fetch Argyve Another Knickknack~Return to Argyve": 5,
    
    "Weirdwire Conduit... Eureka!~Find 200 Feet of Wire": 7,
    "Weirdwire Conduit... Eureka!~Return to Argyve": 7,
    
    "A Canticle for Barathrum~Travel to Grit Gate": 10,
    # Not controllable through conversation, skipped for now
    # "A Canticle for Barathrum~Locate the Barathrumite Enclave":10,
    "A Canticle for Barathrum~Speak with the Barathrumites": 10,
    
    "More Than a Willing Spirit~Travel to Golgotha": 12,
    "More Than a Willing Spirit~Find a Dysfunctional Waydroid": 15,
    "More Than a Willing Spirit~Repair the Waydroid": 15,
    "More Than a Willing Spirit~Return to Grit Gate": 15,
    
    "Decoding the Signal~Get Q Girl's Instructions onto the Data Disk": 18,
    "Decoding the Signal~Locate the Mechanimist Compound at Bethesda Susa": 20,
    "Decoding the Signal~Decode the Signal": 22,
    "Decoding the Signal~Return to Grit Gate": 22,
}

goal_lookup = {
    Options.Goal.option_quest_argyve: "Fetch Argyve a Knickknack~Return to Argyve",
    Options.Goal.option_quest_more_than_a_willing_spirit: "More Than a Willing Spirit~Return to Grit Gate",
    Options.Goal.option_quest_decoding_the_signal: "Decoding the Signal~Return to Grit Gate",
}

def main_quests(world: "CoQWorld") -> Iterable[str]:
    for name in main_quests_table.keys():
        yield name
        if name == goal_lookup[world.options.goal]:
            break

def quest_unlock_item(name: str) -> str:
    return "Unlock: " + name

# Max level is last required quest level + some extra
# TODO
def max_level(world: "CoQWorld") -> int:
    return main_quests_table[goal_lookup[world.options.goal]] + world.options.extra_location_levels

# These all stand by themselves, no logic other than the level requirement per step. There
# are no unlocks for these, so no deadlock possible.
side_quests_table: Dict[str, int] = {
    "What's Eating the Watervine?~Travel to Red Rock": 1,
    "What's Eating the Watervine?~Find the Vermin": 3,
    "What's Eating the Watervine?~Get a Corpse": 3,
    "What's Eating the Watervine?~Return with the Corpse": 5,
    "O Glorious Shekhinah!~Make a Pilgrimage to the Six Day Stilt": 3,
    "Raising Indrix~Find Mamon Souldrinker": 15,
    "Raising Indrix~Recover the Amaranthine Prism": 15
}

def side_quests(world: "CoQWorld") -> Iterable[str]:
    for name, level in side_quests_table.items():
        if level <= max_level(world):
            yield name
