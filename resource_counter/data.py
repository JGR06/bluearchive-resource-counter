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


# ocr asset and result variable data
ocr_assets = {
    MenuState.Items: {
        'item_count': {
            'asset_name': 'OCR',
            'variable_name': 'ocr_result'
        },
        'item_name_0': {  # line 1
            'asset_name': 'OCR_item_name_0',
            'variable_name': 'ocr_i_name_0'
        },
        'item_name_1': {  # line 2
            'asset_name': 'OCR_item_name_1',
            'variable_name': 'ocr_i_name_1'
        }
    },
    MenuState.Equipments: {
        'item_count': {
            'asset_name': 'OCR_equip',
            'variable_name': 'ocr_e_result'
        },
        'item_name_0': {  # line 1
            'asset_name': '',
            'variable_name': ''
        },
        'item_name_1': {  # line 2
            'asset_name': '',
            'variable_name': ''
        }
    }
}


def get_assetname_by_state(state):
    if state in lookup_resource_types:
        return lookup_resource_types[state]
    else:
        return 'Undefined'


def get_item_type_by_state(state):
    if state == MenuState.Items:
        return 'item'
    elif state == MenuState.Equipments:
        return 'equip'
    else:
        return None


class DataSet:
    def __init__(self):
        self.collectibles = {}
        self.load()

    def load(self):
        with open('../resource_counter/resources_data.json', encoding='UTF8') as f:
            raw = json.load(f)
        for k, entity in raw.items():  # k is id for sheet, v is dict for it
            if '|' in entity['note']:  # dirty parsing
                xp = (entity['note'].split('|'))[-1]
                xp = int(''.join(filter(str.isdigit, xp)))
            else:
                xp = 0
            # skip equipments for rapid testing
            if entity['type'] == 'item':
                self.collectibles[k] = entity.copy()
                self.collectibles[k]['xp'] = xp
            else:
                continue
        # temporary equipments data
        self.collectibles['GXP_1'] = {"type": "equip", "asset_name": "GXP_1", "similar_items": None, "note": "장비강화석#0|90xp", 'xp': 90}

    def copy_collectible_items(self):
        return copy.deepcopy(self.collectibles)


resource_data = DataSet()
