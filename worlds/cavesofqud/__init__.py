from typing import List

from BaseClasses import Entrance, LocationProgressType
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
    location_name_to_id = {name: id for id, name in enumerate(Locations.all_locations, 1)}

    def fill_slot_data(self) -> dict:
        return self.options.as_dict(*[name for name in self.options_dataclass.type_hints.keys()])

    def generate_early(self):
        return
    
    def create_regions(self):
        from BaseClasses import Region

        # Only one region for now
        menu = Region("Menu", self.player, self.multiworld)
        qud = Region("Qud", self.player, self.multiworld)

        # Main Quest locations
        for name in Locations.main_quests:
            loc = Locations.CoQLocation(self.player, name, self.location_name_to_id[name], qud)
            loc.progress_type = LocationProgressType.PRIORITY
            qud.locations += [loc]

        # Side Quest locations
        for q in Locations.side_quests:
            for name in q:
                loc = Locations.CoQLocation(self.player, name, self.location_name_to_id[name], qud)
                qud.locations += [loc]

        # Level locations
        for name in Locations.xp_locations(
            self.options.max_level.value,
            self.options.locations_per_level.value):
            loc = Locations.CoQLocation(self.player, name, self.location_name_to_id[name], qud)
            qud.locations += [loc]

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
