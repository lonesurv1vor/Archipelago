from typing import List

from BaseClasses import Entrance, Item, ItemClassification, LocationProgressType, Tutorial
from worlds.AutoWorld import WebWorld, World

from . import Rules
from . import Items
from . import Locations
from . import Options

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

    item_name_to_id = {name: data.code for name, data in Items.item_table.items() if data.code is not None}
    location_name_to_id = {name: data.id for name, data in Locations.location_table.items() if data.id is not None}

    def fill_slot_data(self) -> dict:
        return self.options.as_dict(*[name for name in self.options_dataclass.type_hints.keys()])

    def generate_early(self):
        return
    
    def create_regions(self):
        from BaseClasses import Region

        # Only one region for now
        menu = Region("Menu", self.player, self.multiworld)
        qud = Region("Qud", self.player, self.multiworld)

        # Level locations
        for level, step in Locations.level_locations(
            self.options.max_level.value,
            self.options.locations_per_level.value):

            loc_name = Locations.level_location_name(level, step)
            loc = Locations.CoQLocation(self.player, loc_name, Locations.location_table[loc_name].id, qud)
            qud.locations += [loc]

        # Quest locations
        for name, data in Locations.location_table.items():
            if data.category != "Quest":
                continue
            loc = Locations.CoQLocation(self.player, name, data.id, qud)
            qud.locations += [loc]


        # Set victory location and place event
        victory_loc = Options.goal_lookup[self.options.goal]
        self.get_location(victory_loc).address = None
        self.get_location(victory_loc).place_locked_item(
            Item("Victory", ItemClassification.progression, None, self.player)
        )

        # Connect Menu to Qud
        conn = Entrance(self.player, "To Qud", menu)
        menu.exits.append(conn)
        conn.connect(qud)

        self.multiworld.regions += [menu, qud]

    def create_items(self):
        item_pool: List[Items.CoQItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Stat ups from level ups
        for level in Rules.levelup_levels(self.options.max_level):
            items = Items.stat_items_on_levelup(level)
            item_pool += [Items.create_item(self, item) for item in items]

        # Fill up with fillers
        while len(item_pool) < total_locations:
            item_pool += [Items.create_item(self, Items.get_filler_item_name(self))]

        self.multiworld.itempool += item_pool

    def set_rules(self):
        Rules.set_rules(self)
