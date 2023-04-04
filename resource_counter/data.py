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
    return lookup_resource_types.get(state, 'Undefined')


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
            f.close()
        for k, entity in raw.items():  # k is id for sheet, v is dict for it
            if '|' in entity['note']:  # dirty parsing
                xp = (entity['note'].split('|'))[-1]
                xp = int(''.join(filter(str.isdigit, xp)))
            else:
                xp = 0
            self.collectibles[k] = entity.copy()
            self.collectibles[k]['xp'] = xp

    def copy_collectible_items(self):
        return copy.deepcopy(self.collectibles)

    def debug_replace_key_to_name(self, key_dict):
        return dict(map(lambda kv: (self.collectibles.get(kv[0], {'default': 'none'}).get('note', 'Unmanaged'), kv[1]), key_dict.items()))

    def find(self, item_name, school_name):
        nearest_item = None
        nearest_score = 0
        for k, entity in self.collectibles.items():
            if entity['school'] is None or entity['school'] not in school_name:
                continue
            item_type_matched = 0
            for t in entity['item_type'].split(','):
                if t in item_name:
                    item_type_matched += 1
            if entity['grade'] == '상급' and '최상' in item_name:
                item_type_matched += 0  # do nothing
            elif entity['grade'] in item_name:
                item_type_matched += 1
            if item_type_matched > nearest_score:
                nearest_item = k
                nearest_score = item_type_matched
        return nearest_item

    # replace planner site exported userdata if you prepared.
    def save_planner_userdata(self, collectibles, save_as='planner_exported.json'):
        with open('../resource_counter/planner_exported.json', 'r+') as f:
            planner_data = json.load(f)
            # currently 'credit' item is not counting. so keep it
            credit = planner_data['owned_materials']['Credit']
            collectibles['Credit'] = credit
            planner_data['owned_materials'] = collectibles
            f.close()

        with open(f'../resource_counter/{save_as}', 'w') as f:
            json.dump(planner_data, f)
            f.close()


resource_data = DataSet()
