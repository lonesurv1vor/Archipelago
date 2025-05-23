from typing import TYPE_CHECKING
from Options import Choice, Range, PerGameCommonOptions
from dataclasses import dataclass
from . import Quests

MAX_MAX_LEVEL = 50
MAX_LOCATIONS_PER_LEVEL = 10

class LocationsPerLevel(Range):
    """
    Determines the number of locations to check when gaining XP.
    Each level contains the number of locations chosen here,
    distributed across the XP range between current and next level.
    Including the level up itself.
    """
    display_name = "Extra locations per level"
    range_start = 4
    range_end = MAX_LOCATIONS_PER_LEVEL
    default = 5

class Goal(Choice):
    """
    Determines the win condition
    """
    display_name = "Goal"
    option_quest_argyve = 0
    option_quest_more_than_a_willing_spirit = 1
    option_quest_decoding_the_signal = 2
    default = 2

class TrapPercentage(Range):
    """
    Determines the percentage of filler items that are replaced by
    traps.
    """
    display_name = "Percentage of filler items replaced with traps"
    range_start = 0
    range_end = 100
    default = 50

@dataclass
class CoQOptions(PerGameCommonOptions):
    locations_per_level: LocationsPerLevel
    goal: Goal
    trap_percentage: TrapPercentage
    # death_link: DeathLink 
