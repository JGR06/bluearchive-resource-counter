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


items_to_asset = {
    'XP_1': 'XP_1',  # character xp
    'XP_2': 'XP_2',
    'XP_3': 'XP_3',
    'XP_4': 'XP_4',
    '100': 'nebra0',
    '101': 'nebra1',
    '102': 'nebra2',
    '103': 'nebra3',
    '110': 'phaistos0',
    '111': 'phaistos1',
    '112': 'phaistos2',
    '113': 'phaistos3',
    '120': 'wolfsegg0',
    '121': 'wolfsegg1',
    '122': 'wolfsegg2',
    '123': 'wolfsegg3',
    '130': 'nimrud0',
    '131': 'nimrud1',
    '132': 'nimrud2',
    '133': 'nimrud3',
    '140': 'mandragora0',
    '141': 'mandragora1',
    '142': 'mandragora2',
    '143': 'mandragora3',
    '150': 'rohonc0',
    '151': 'rohonc1',
    '152': 'rohonc2',
    '153': 'rohonc3',
    '160': 'aether0',
    '161': 'aether1',
    '162': 'aether2',
    '163': 'aether3',
    '170': 'antikythera0',
    '171': 'antikythera1',
    '172': 'antikythera2',
    '173': 'antikythera3',
    '180': 'voynich0',
    '181': 'voynich1',
    '182': 'voynich2',
    '183': 'voynich3',
    '190': 'haniwa0',
    '191': 'haniwa1',
    '192': 'haniwa2',
    '193': 'haniwa3',
    '200': 'totem0',
    '201': 'totem1',
    '202': 'totem2',
    '203': 'totem3',
    '210': 'baghdad0',
    '211': 'baghdad1',
    '212': 'baghdad2',
    '213': 'baghdad3',
    '240': 'colgante0',
    '241': 'colgante1',
    '242': 'colgante2',
    '243': 'colgante3',
    '290': 'mystery0',
    '291': 'mystery1',
    '292': 'mystery2',
    '293': 'mystery3',
}

equipments_to_asset = {
    'GXP1': 'GXP_1',  # gear xp
}
