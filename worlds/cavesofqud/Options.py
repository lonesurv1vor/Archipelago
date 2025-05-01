from Options import Choice, Range, PerGameCommonOptions
from dataclasses import dataclass

MAX_MAX_LEVEL = 100

class MaxLevel(Range):
    """
    Determines the maximum level to include in the item and check pool.
    """
    display_name = "Max level"
    range_start = 1
    range_end = MAX_MAX_LEVEL
    default = 30

MAX_LOCATIONS_PER_LEVEL = 10

class LocationsPerLevel(Range):
    """
    Determines the number of locations to check when gaining XP.
    Each level contains the number of locations chosen here,
    distributed across the XP range between current and next level.
    Including the level up itself.
    """
    display_name = "Extra locations per level"
    range_start = 1
    range_end = MAX_LOCATIONS_PER_LEVEL
    default = 4

class Goal(Choice):
    """
    Determines the win condition
    """
    display_name = "Goal"
    option_quest_argyve = 0
    option_quest_more_than_a_willing_spirit = 1
    option_quest_decoding_the_signal = 2
    default = 2

@dataclass
class CoQOptions(PerGameCommonOptions):
    max_level: MaxLevel
    locations_per_level: LocationsPerLevel
    goal: Goal
    # death_link: DeathLink
