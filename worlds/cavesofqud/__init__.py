from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import CoQItem, CoQItemData, get_items_by_category, item_table, stat_items_on_levelup
from .Locations import CoQLocation, CoQLocationData, level_location_name, level_locations, location_table
from .Options import CoQOptions

class CoQWeb(WebWorld):
    theme = "jungle"
    bug_report_page = "https://github.com/lonesurv1vor/CavesOfQud_AP/issues"

class CoQWorld(World):
    """
    Live and drink
    """
    game = "Caves of Qud"
    web = CoQWeb()
    options_dataclass = CoQOptions
    options: CoQOptions
    topology_present = False
    required_client_version = (0, 6, 0)
    required_server_version = (0, 6, 0)

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.id for name, data in location_table.items() if data.id is not None}

    def fill_slot_data(self) -> dict:
        return self.options.as_dict(*[name for name in self.options_dataclass.type_hints.keys()])

    def generate_early(self):
        return

    def create_items(self):
        item_pool: List[CoQItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Stat ups from level ups
        for level in range(1, self.options.max_level):
            items = stat_items_on_levelup(level)
            item_pool += [self.create_item(item) for item in items]

        # Fill up with fillers
        while len(item_pool) < total_locations:
            item_pool += [self.create_item(self.get_filler_item_name())]

        self.multiworld.itempool += item_pool

    def create_item(self, name: str) -> CoQItem:
        data = item_table[name]
        return CoQItem(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        fillers = get_items_by_category("Filler")
        weights = [data.weight for data in fillers.values()]
        return self.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def set_rules(self):
        # Win condition, TODO
        self.multiworld.completion_condition[self.player] = lambda state: True

    def create_regions(self):
        from BaseClasses import Region

        # Only one region for now
        region = Region("Menu", self.player, self.multiworld)

        # Quest locations
        for name, data in location_table.items():
            if data.category != "Quest":
                continue
            loc = CoQLocation(self.player, name, data.id, region)
            region.locations.append(loc)

        # Level Gain locations
        for (level, step) in level_locations(self.options.max_level, self.options.locations_per_level):
                name = level_location_name(level, step)
                loc = CoQLocation(self.player, name, location_table[name].id, region)
                region.locations.append(loc)

        self.multiworld.regions.append(region)