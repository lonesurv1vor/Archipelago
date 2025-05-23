from typing import List

from BaseClasses import Entrance, LocationProgressType
from worlds.AutoWorld import WebWorld, World

from . import Rules
from . import Items
from . import Locations
from . import Options
from . import Quests
from . import Regions

class CoQWeb(WebWorld):
    theme = "jungle"
    bug_report_page = "https://github.com/lonesurv1vor/CavesOfQudArchipelagoRandomizer/issues"

class CoQWorld(World):
    """
    Live and drink
    """
    game = "Caves of Qud"
    web = CoQWeb()
    options_dataclass = Options.CoQOptions
    options: Options.CoQOptions # type: ignore
    topology_present = False
    required_client_version = (0, 6, 0)
    required_server_version = (0, 6, 0)

    item_name_to_id = {item: id for id, item in enumerate(Items.all_items, 1)}
    location_name_to_id = {name: id for id, name in enumerate(Locations.all_locations, 1)}

    def fill_slot_data(self) -> dict:
        return self.options.as_dict(*[name for name in self.options_dataclass.type_hints.keys()])

    def generate_early(self):
        return
    
    def create_regions(self):
        Regions.create_regions(self)

    def create_items(self):
        item_pool: List[Items.CoQItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Main quest unlock items
        for quest in Quests.main_quests(self):
            item_name = Quests.quest_unlock_item(quest)
            item_pool += [Items.CoQItem(item_name, Items.ItemClassification.progression, self.item_name_to_id[item_name], self.player)]

        # Stat ups from level ups
        for level in Regions.levelup_levels(Quests.max_level(self)):
            item_pool += Items.create_stat_items_on_levelup(self, level)

        # Fill up with fillers
        while len(item_pool) < total_locations:
            item_pool += [Items.create_filler_item(self)]

        self.multiworld.itempool += item_pool

    def set_rules(self):

        Rules.set_rules(self)
