import json
import copy
from enum import Enum


class MenuState(Enum):
    Main = 0
    Option = 1
    Items = 2
    Equipments = 3


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


# NOTE: BlueArchive sets letterbox to screen when ratio is not matched.
# therefore below is not working well except 16:9 resolutions
# TODO: fix when ratio is not 16:9
class ScaledSizeContainer:
    # (w, h) or (x, y, w, h)
    constant_sizes_by_ui = {
        MenuState.Items: {
            'cell': (168, 150),
            'cell_consider_line': (0, 60),
            'table_roi': (1026, 224, 842, 690)
        },
        MenuState.Equipments: {
            'cell': (168, 150),
            'cell_consider_line': (0, 60),
            'table_roi': (1031, 228, 1031 + 831, 228 + 765)
        }
    }

    def __init__(self):
        self.design_resolution = (1920, 1080)
        self.screen_resolution = (1920, 1080)  # TODO: get window size from imax
        self.resizing_factor = (1.0, 1.0)

    # size: window size tuple
    def set_resolution(self, size):
        self.screen_resolution = size
        self.resizing_factor = (self.screen_resolution[0] / self.design_resolution[0], self.screen_resolution[1] / self.design_resolution[1])

    def get_size(self, current_ui, key):
        ui = self.constant_sizes_by_ui.get(current_ui, None)
        target = ui.get(key, None) if ui else None
        if target is None:
            return None
        resized = []
        for i in range(0, len(target)):
            resized.append(target[i] * self.resizing_factor[i % 2])  # sizes are always [w, h] or [x, y, w, h]
        return tuple(int(i) for i in resized)  # screen points should be integer

    def get_scale_factor(self):
        return self.resizing_factor


scaled_sizes = ScaledSizeContainer()


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
