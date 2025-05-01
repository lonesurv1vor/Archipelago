from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification

class CoQItem(Item):
    game: str = "Caves of Qud"

class CoQItemData(NamedTuple):
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    weight: int = 1

item_table: Dict[str, CoQItemData] = {
    "Hit Points":                         CoQItemData("Stats", 1, ItemClassification.useful),
    "Attribute Points":                   CoQItemData("Stats", 2, ItemClassification.useful),
    "Attribute Bonus":                    CoQItemData("Stats", 3, ItemClassification.useful),
    "Mutation Points":                    CoQItemData("Stats", 4, ItemClassification.useful),
    "Skill Points":                       CoQItemData("Stats", 5, ItemClassification.useful),
    "Rapid Mutation Advancement":         CoQItemData("Stats", 6, ItemClassification.useful),

    "10 Drams of Fresh Water":            CoQItemData("Filler", 1000, ItemClassification.filler, 3),
    "Item: 50 Lead Slug":                 CoQItemData("Filler", 1001, ItemClassification.filler, 4),
    "Item: 50 Shotgun Shell":             CoQItemData("Filler", 1002, ItemClassification.filler, 4),
    "Item: 20 Wooden Arrow":              CoQItemData("Filler", 1003, ItemClassification.filler, 4),
    "Item: 20 Steel Arrow":               CoQItemData("Filler", 1004, ItemClassification.filler, 4),
    "Item: HeatGrenade2":                 CoQItemData("Filler", 1005, ItemClassification.filler, 4),
    "Item: HEGrenade2":                   CoQItemData("Filler", 1006, ItemClassification.filler, 4),
    "Item: EMPGrenade2":                  CoQItemData("Filler", 1007, ItemClassification.filler, 4),
    "Item: AcidGasGrenade2":              CoQItemData("Filler", 1008, ItemClassification.filler, 4),
    "Item: Laser Rifle":                  CoQItemData("Filler", 1009, ItemClassification.filler, 1),
    "Item: Gaslight Dagger":              CoQItemData("Filler", 1010, ItemClassification.filler, 2),
    "Item: Chem Cell":                    CoQItemData("Filler", 1011, ItemClassification.filler, 3),
    "Item: Solar Cell":                   CoQItemData("Filler", 1012, ItemClassification.filler, 2),
    "Item: Nuclear Cell":                 CoQItemData("Filler", 1013, ItemClassification.filler, 1),

    "Spawn Creature Trap":                CoQItemData("Filler", 1014, ItemClassification.trap, 25),
    "Bomb Trap":                          CoQItemData("Filler", 1015, ItemClassification.trap, 10),
    "Double Bomb Trap":                   CoQItemData("Filler", 1016, ItemClassification.trap, 5),
}

def stat_items_on_levelup(level: int) -> list[str]:
    items = ["Hit Points", "Mutation Points", "Skill Points"]
    if (level + 3) % 6 == 0:
        items.append("Attribute Points")
    if (level + 6) % 6 == 0:
        items.append("Attribute Bonus")
    if (level + 5) % 10 == 0:
        items.append("Rapid Mutation Advancement")

    return items


def get_items_by_category(category: str) -> Dict[str, CoQItemData]:
    item_dict: Dict[str, CoQItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)
    return item_dict