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


def get_assetname_by_state(state):
    if state in lookup_resource_types:
        return lookup_resource_types[state]
    else:
        return 'Undefined'


items_to_asset = {
    'XP1': 'XP_1',  # character xp
    'XP2': 'XP_2',
    'XP3': 'XP_3',
    'XP4': 'XP_4',
}

equipments_to_asset = {
    'GXP1': 'GXP_1',  # gear xp
}
