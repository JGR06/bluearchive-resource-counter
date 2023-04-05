import copy
import sys
import time
from datetime import date
import json
import importlib.util
# TODO: fix dirty import
file_path = '../resource_counter/util.py'
module_name = 'util'

spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.modules[module_name] = module

import util
util.import_specific_module('lua_helper.py', 'lua_helper')
util.import_specific_module('data.py', 'data')
util.import_specific_module('settings.py', 'settings')
import lua_helper
import data
import settings
import imax


class ResourceCounter:
    def __init__(self):
        self.scroll_count_while_not_found = 0
        self.current_state = data.MenuState.Main
        self.collectibles = data.resource_data.copy_collectible_items()
        self.skip_until_scroll = []
        self.result = {'Xp': 0, 'GearXp': 0}
        self.misrecognitions = {}
        self.roi_table = []
        self.current_clicked_positions = []
        data.scaled_sizes.set_resolution(lua_helper.get_window_size())
        imax.print("ResourceCounter initialized")

    def is_finished(self):
        return len(self.collectibles.keys()) == 0

    def save(self):
        with open(f'{util.root_path}/output.json', 'w') as f:
            json.dump(self.result, f)
        f.close()

        today = date.today()
        data.resource_data.save_planner_userdata(self.result, f"result_data_{today.strftime('%y%m%d')}.json")

        data.resource_data.save_result_diff(self.result, settings.RESULT_DIFF_WARNING_THRESHOLD, f"result_diff_{today.strftime('%y%m%d')}.json")

        # debug outputs
        if settings.DEBUG_SAVE_MISRECOGNITIONS:
            with open(f'{util.root_path}/misrecognitions.json', 'w') as f:
                json.dump(self.misrecognitions, f)
            f.close()

        if settings.DEBUG_SAVE_NAME_REPLACED_RESULT:
            with open(f'{util.root_path}/debug_output.json', 'w', encoding='UTF-8') as f:
                json.dump(data.resource_data.debug_replace_key_to_name(self.result), f, ensure_ascii=False)
            f.close()

    def run(self):
        while not self.is_finished():
            self.update_state()
        self.save()

    def remaining_items_count(self, state):
        key = data.get_item_type_by_state(state)
        return sum(1 for e in self.collectibles.values() if e['type'] == key)  # I want method like LINQ...

    # state switch
    def update_state(self):
        if self.current_state == data.MenuState.Main:  # enter to options
            lua_helper.find_and_click(data.get_assetname_by_state(data.MenuState.Option))
            time.sleep(1)
            self.current_state = data.MenuState.Option

        elif self.current_state == data.MenuState.Option:  # enter to items or equipments
            if self.remaining_items_count(data.MenuState.Items) > 0:
                self.scroll_count_while_not_found = 0
                lua_helper.find_and_click(data.get_assetname_by_state(data.MenuState.Items))
                time.sleep(settings.DELAY_BEFORE_TABLE_UI_ENTERED)
                self.current_state = data.MenuState.Items
                self.find_table_roi()
            elif self.remaining_items_count(data.MenuState.Equipments) > 0:
                self.scroll_count_while_not_found = 0
                lua_helper.find_and_click(data.get_assetname_by_state(data.MenuState.Equipments))
                time.sleep(settings.DELAY_BEFORE_TABLE_UI_ENTERED)
                self.current_state = data.MenuState.Equipments
                self.find_table_roi()
            else:
                imax.print('something went wrong')

        elif self.current_state == data.MenuState.Items:  # count items
            self.counting_resources(data.MenuState.Items)
            time.sleep(settings.DELAY_AFTER_TABLE_RECOGNITION_LOOP)

        elif self.current_state == data.MenuState.Equipments:  # count equipments
            self.counting_resources(data.MenuState.Equipments)
            time.sleep(settings.DELAY_AFTER_TABLE_RECOGNITION_LOOP)

    def counting_resources(self, state):
        if self.remaining_items_count(state) == 0:
            lua_helper.find_and_click('back_button')
            # returning to lobby occurs network request -- then can't send any input til request ends
            time.sleep(settings.DELAY_AFTER_BACK_BUTTON)
            # TODO: check 'NOW LOADING' image disappear
            self.current_state = data.MenuState.Option
            return

        item_type = data.get_item_type_by_state(state)
        skip_search = []
        area_search_finished = self.check_area_skippable(state)
        for item_id, v in self.collectibles.items():
            if area_search_finished:
                break
            if v['type'] != item_type or item_id in skip_search or item_id in self.skip_until_scroll:
                continue
            searched_results = self.count_resource(item_id, v, state)
            for searched in searched_results:
                found_key = searched['item_id']
                self.result.setdefault(found_key, 0)
                if self.result[found_key] != searched['count']:
                    self.result[found_key] = searched['count']
                    self.current_clicked_positions.append(searched['position'])
                    imax.print(f'[[{v} found({self.result[found_key]} entities)]]')
                if searched['detail_searched']:
                    skip_search.append(found_key)
            if len(searched_results) == 0:
                self.skip_until_scroll.append(item_id)
            area_search_finished = self.check_area_skippable(state)
        found_items_count = 0
        for k, v in self.result.items():
            if k in self.collectibles and self.result[k] > 0:
                if state == data.MenuState.Items:
                    self.result['Xp'] += (self.result[k] * self.collectibles[k]['xp'])
                elif state == data.MenuState.Equipments:
                    self.result['GearXp'] += (self.result[k] * self.collectibles[k]['xp'])
                self.collectibles.pop(k)
                found_items_count += self.result[k]

        imax.print(f'[Scrolling: {settings.SCROLL_COUNT_LIMIT_UNTIL_FOUND - self.scroll_count_while_not_found} time(s) remaining]{found_items_count} item(s) found this time')
        if found_items_count == 0:
            if self.scroll_count_while_not_found < settings.SCROLL_COUNT_LIMIT_UNTIL_FOUND:
                lua_helper.scroll_and_wait(settings.TABLE_SCROLL_AMOUNT, settings.DELAY_AFTER_TABLE_SCROLL, data.scaled_sizes.get_scale_factor())
                self.skip_until_scroll.clear()
                self.current_clicked_positions.clear()
            self.scroll_count_while_not_found += 1
        else:
            self.scroll_count_while_not_found = 0

        # there's no items which we're looking for, escape
        if self.scroll_count_while_not_found >= settings.SCROLL_COUNT_LIMIT_UNTIL_FOUND:
            for k, v in self.collectibles.items():
                self.result[k] = 0
            # remove items which not found
            self.collectibles = {k: v for k, v in self.collectibles.items() if v['type'] != item_type}

    # NOTE: there's pretty different UI between 'ITEMS' and 'EQUIPMENTS' so it should take OCR target parameters
    # NOTE: multi-return for ambiguous images(BD, Skillbooks)
    # process ocr when image found
    def count_resource(self, target_key, target_data, state):
        asset_name = target_data['asset_name']
        ocr_asset_name = data.ocr_assets[state]['item_count']['asset_name']
        ocr_result_var = data.ocr_assets[state]['item_count']['variable_name']
        # TODO: remove 'similar_items' data
        need_detailed_search = target_data['similar_items'] is not None or target_data['school'] is not None
        count = 0
        results = []
        lua_helper.set_image_roi(asset_name, self.roi_table)
        if need_detailed_search:
            for searched in lua_helper.search_all_images_from_screen(asset_name):
                lua_helper.click(searched['ix'], searched['iy'])
                time.sleep(settings.DELAY_AFTER_ITEM_CLICK)  # UI refresh rate
                # item detailed name OCR
                ocr_item_name_line0 = data.ocr_assets[state]['item_name_0']['asset_name']
                ocr_item_name_line0_result = data.ocr_assets[state]['item_name_0']['variable_name']
                item_name = lua_helper.ocr(ocr_item_name_line0, ocr_item_name_line0_result)
                item_name = self.handle_ocr_misunderstood_words(item_name)
                # school name OCR
                ocr_item_name_line1 = data.ocr_assets[state]['item_name_1']['asset_name']
                ocr_item_name_line1_result = data.ocr_assets[state]['item_name_1']['variable_name']
                school_name = lua_helper.ocr(ocr_item_name_line1, ocr_item_name_line1_result)
                school_name = self.handle_ocr_misunderstood_words(school_name)
                imax.print(f'School Name: {school_name} Item Name: {item_name}')

                fallback_item = None
                item_type_matched = 0
                target_types = target_data['item_type'].split(',')
                if target_data['grade'] is not None:
                    target_types.append(target_data['grade'])
                for t in target_types:
                    if t == '상급' and '최상급' in item_name:
                        continue  # dirty exception handling
                    if t in item_name:
                        item_type_matched += 1
                school_name_matched = False
                if target_data['school'] in school_name:
                    school_name_matched = True
                imax.print(f'detailed search: school({school_name_matched}), type_match({item_type_matched})')

                count = lua_helper.ocr_count(ocr_asset_name, ocr_result_var)
                if not school_name_matched or item_type_matched < len(target_types):
                    fallback_item = data.resource_data.find(item_name, school_name)
                if fallback_item is not None and target_key != fallback_item:
                    imax.print(f'[WARNING]you tried to search {target_key}, but found item is {fallback_item}')
                    misrecognition_list = self.misrecognitions.setdefault(target_key, [])
                    misrecognition_list.append(fallback_item)
                    results.append({
                        'item_id': fallback_item,
                        'count': count,
                        'detail_searched': True,
                        'position': [searched['ix'], searched['iy']]
                    })
                else:
                    results.append({
                        'item_id': target_key,
                        'count': count,
                        'detail_searched': True,
                        'position': [searched['ix'], searched['iy']]
                    })
                if (school_name_matched and item_type_matched == len(target_types)) or fallback_item == target_key:
                    break  # found item which we're looking for

        else:
            searched = lua_helper.search_image(asset_name)
            if searched['succeed']:
                lua_helper.click(searched['ix'], searched['iy'])
                time.sleep(settings.DELAY_AFTER_ITEM_CLICK)  # UI refresh rate
                count = lua_helper.ocr_count(ocr_asset_name, ocr_result_var)
                results.append({
                    'item_id': target_key,
                    'count': count,
                    'detail_searched': False,
                    'position': [searched['ix'], searched['iy']]
                })

        return results

    def handle_ocr_misunderstood_words(self, str):
        # OCR provides unexpected linebreaks or whitespaces.
        str = str.replace(' ', '').replace('\n', '').replace('\r', '')
        if str == '기조전술교육D':
            return '기초전술교육BD'
        if str == '육일반전술교육':
            return '일반전술교육BD'
        if str == '상급전술교육':
            return '상급전술교육BD'
        if str == '최싱최상급전술교육' or str == '최싱최상급전술교육BD':
            return '최상급전술교육BD'
        if str == '기조기술노트':
            return '기초기술노트'
        return str

    # current_clicked_positions shouldn't contain too closed positions
    def check_area_skippable(self, state):
        # for now, only Items UI requires detailed search and skip algorithm
        if state != data.MenuState.Items:
            return False
        # resources_data is sorted by items id
        # so, we're able to know if we got left-top item and bottom-right item
        # but table UI height is not fit to items(4.5row) then we should find where last line is
        # ---- or ----
        # just check count of unique cell count of table if you can control drag heights
        if len(self.current_clicked_positions) < 2:
            return False
        # current_clicked_positions should like this: [[x, y], [x, y], ...]
        positions = copy.deepcopy(self.current_clicked_positions)
        origin_x = self.roi_table[0]
        origin_y = self.roi_table[1]
        ypos_limit = data.scaled_sizes.get_size(state, 'cell_consider_line')[1]
        y_sorted = sorted(positions, key=lambda x: x[1])
        preview = list(filter(lambda x: abs(x[1] - y_sorted[0][1]) < ypos_limit, y_sorted))
        items_by_line = []
        while len(y_sorted) > 0:
            items_by_line.append(sorted(list(filter(lambda x: abs(x[1] - y_sorted[0][1]) < ypos_limit, y_sorted)), key=lambda x: x[0]))
            for item in items_by_line[-1]:
                y_sorted.pop(0)

        # if line count is under 2, we scrolled 2 lines, so it didn't checked all
        if len(items_by_line) < settings.LINES_TO_CHECK_PER_SCROLL:
            return False
        first_line = items_by_line[0]
        last_line = items_by_line[-1]
        # if line's element count is under 5, we didn't checked whole line
        if len(last_line) < 5 or len(first_line) < 5:
            return False
        # is it rightmost and undermost position?
        cell_size = data.scaled_sizes.get_size(state, 'cell')
        cell_width = cell_size[0]
        cell_height = cell_size[1]
        overed_height = self.roi_table[3] % cell_height
        table_right = self.roi_table[0] + self.roi_table[2]
        table_bottom = self.roi_table[1] + self.roi_table[3]
        last_cell_position = last_line[-1]
        # if it was last column in current table screen
        if last_cell_position[0] > (table_right - cell_width) and \
                last_cell_position[1] > (table_bottom - (cell_height + overed_height)):
            return True

        return False

    def find_table_roi(self):
        roi = data.scaled_sizes.get_size(self.current_state, 'table_roi')
        imax.print(f'current table roi: {roi[0]}, {roi[1]}, {roi[2]}, {roi[3]}')
        self.roi_table = list(roi)
        # self.roi_table = self.makeRoi(roi[0], roi[1], roi[2], roi[3], 166, 140)

        # TODO: search table ROI and calculate
        # top_asset_name = 'i_table_top' if self.current_state == data.MenuState.Items else 'e_table_top'
        # bottom_asset_name = 'i_table_bottom' if self.current_state == data.MenuState.Items else 'e_table_bottom'
        # top_asset = lua_helper.search_image(top_asset_name)
        # roi = [0, 0, 0, 0]
        # if top_asset["succeed"]:
        #     roi[0] = top_asset["sx"]
        #     roi[1] = top_asset["sy"] + 36  # magic number(height)
        # bottom_asset = lua_helper.search_image(bottom_asset_name)
        # if bottom_asset["succeed"]:
        #     roi[2] = bottom_asset["sx"] + 850  # magic number(width)
        #     roi[3] = bottom_asset["sy"]
        #
        # if not top_asset["succeed"] or not bottom_asset["succeed"]:
        #     imax.print("image search failed: table top/bottom")
        #     return
        #
        # imax.print(f'box roi: {roi[0]}, {roi[1]}, {roi[2]}, {roi[3]}')
        # self.roi_table = self.makeRoi(roi[0], roi[1], roi[2], roi[3], 166, 140)

