import json
import copy
from enum import Enum


class MenuState(Enum):
    Main = 0
    Option = 1
    Items = 2
    Equipments = 3


# stop searching and scrolling if there is no result during N times of scrolling
SCROLL_COUNT_LIMIT_UNTIL_FOUND = 5


# lookup to resource typenames to imagemax asset name
lookup_resource_types = {
    MenuState.Option: 'options',
    MenuState.Items: 'items',
    MenuState.Equipments: 'equipments',
}


def get_assetname_by_state(state):
    if state in lookup_resource_types:
        return lookup_resource_types[state]
    else:
        return 'Undefined'


class DataSet:
    def __init__(self):
        self.collectables = {}
        self.equipments = {}
        self.load()

    def load(self):
        with open('../resource_counter/resources_data.json') as f:
            raw = json.load(f)
        for k, entity in raw.items():  # k is id for sheet, v is dict for it
            if '|' in entity['note']:  # dirty parsing
                xp = (entity['note'].split('|'))[-1]
                xp = int(''.join(filter(str.isdigit, xp)))
            else:
                xp = 0
            if entity['type'] == 'item':
                self.collectables[k] = entity.copy()
                self.collectables[k]['xp'] = xp
            # skip equipments for rapid testing
            # elif entity['type'] == 'equip':
            #     self.equipments[k] = entity.copy()
            #     self.equipments[k]['xp'] = xp
            else:
                continue
        # temporary equipments data
        self.equipments['GXP_1'] = {"type": "equip", "asset_name": "GXP_1", "similar_items": None, "note": "장비강화석#0|90xp", 'xp': 90}

    def copy_collectable_items(self):
        return copy.deepcopy(self.collectables)

    def copy_equipments(self):
        return copy.deepcopy(self.equipments.copy())


resource_data = DataSet()
