import sys
import time
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
import lua_helper
import data
import imax


class ResourceCounter:
    def __init__(self):
        self.scroll_count_while_not_found = 0
        self.current_state = data.MenuState.Main
        self.items = data.items_to_asset.copy()
        self.equipments = data.equipments_to_asset.copy()
        self.result = {}
        self.roi_table = []
        imax.print("ResourceCounter initialized")

    def is_finished(self):
        return len(self.items.keys()) == 0 and len(self.equipments.keys()) == 0

    def save(self):
        with open(f'{util.root_path}/output.json', 'w') as f:
            json.dump(self.result, f)
        f.close()

    def run(self):
        while not self.is_finished():
            self.update_state()
        self.save()

    # state switch
    def update_state(self):
        if self.current_state == data.MenuState.Main:  # enter to options
            lua_helper.find_and_click(data.get_assetname_by_state(data.MenuState.Option))
            time.sleep(1)
            self.current_state = data.MenuState.Option

        elif self.current_state == data.MenuState.Option:  # enter to items or equipments
            if len(self.items.keys()) > 0:
                self.scroll_count_while_not_found = 0
                lua_helper.find_and_click(data.get_assetname_by_state(data.MenuState.Items))
                time.sleep(1)
                self.current_state = data.MenuState.Items
                self.find_table_roi()
            elif len(self.equipments.keys()) > 0:
                self.scroll_count_while_not_found = 0
                lua_helper.find_and_click(data.get_assetname_by_state(data.MenuState.Equipments))
                time.sleep(1)
                self.current_state = data.MenuState.Equipments
                self.find_table_roi()
            else:
                imax.print('something went wrong')

        elif self.current_state == data.MenuState.Items:  # count items
            if len(self.items.keys()) == 0:
                lua_helper.find_and_click('back_button')
                # returning to lobby occurs network request -- then can't send any input til request ends
                time.sleep(3.5)
                # TODO: check 'NOW LOADING' image disappear
                self.current_state = data.MenuState.Option
                return

            for k, v in self.items.items():
                self.result[k] = self.count_resource(v, 'OCR', 'ocr_result')
                if self.result[k] > 0:
                    imax.print(f'[[{v} found({self.result[k]} entities)]]')
            found_items_count = 0
            for k, v in self.result.items():
                if k in self.items and self.result[k] > 0:
                    self.items.pop(k)
                    found_items_count += self.result[k]
            imax.print(f'[{self.scroll_count_while_not_found}/{data.SCROLL_COUNT_LIMIT_UNTIL_FOUND}]{found_items_count}')
            if found_items_count == 0:
                lua_helper.scroll_and_wait()
                self.scroll_count_while_not_found += 1
            else:
                self.scroll_count_while_not_found = 0

            # there's no items which we're looking for, escape
            if self.scroll_count_while_not_found >= data.SCROLL_COUNT_LIMIT_UNTIL_FOUND:
                for k, v in self.items.items():
                    self.result[k] = 0
                self.items.clear()
            time.sleep(0.5)

        elif self.current_state == data.MenuState.Equipments:  # count equipments
            if len(self.equipments.keys()) == 0:
                lua_helper.find_and_click('back_button')
                time.sleep(1)
                self.current_state = data.MenuState.Option
            for k, v in self.equipments.items():
                self.result[k] = self.count_resource(v, 'OCR_equip', 'ocr_e_result')
                if self.result[k] > 0:
                    imax.print(f'[[{v} found({self.result[k]} entities)]]')
            found_items_count = 0
            for k, v in self.result.items():
                if k in self.equipments and self.result[k] > 0:
                    self.equipments.pop(k)
                    found_items_count += self.result[k]
            imax.print(f'[{self.scroll_count_while_not_found}/{data.SCROLL_COUNT_LIMIT_UNTIL_FOUND}]{found_items_count}')
            if found_items_count == 0:
                lua_helper.scroll_and_wait()
                self.scroll_count_while_not_found += 1
            else:
                self.scroll_count_while_not_found = 0

            # there's no items which we're looking for, escape
            if self.scroll_count_while_not_found >= data.SCROLL_COUNT_LIMIT_UNTIL_FOUND:
                for k, v in self.equipments.items():
                    self.result[k] = 0
                self.equipments.clear()
            time.sleep(0.5)

    # NOTE: there's pretty different UI between 'ITEMS' and 'EQUIPMENTS' so it should take OCR target parameters
    # process ocr when image found
    def count_resource(self, asset_name, ocr_asset_name, ocr_result_var):
        for i in range(len(self.roi_table)):
            lua_helper.set_image_roi(asset_name, self.roi_table[i])
            # searched = lua_helper.search_image(asset_name)
            searched = lua_helper.find_and_click(asset_name)
            if searched:
                time.sleep(0.5)  # UI refresh rate
                return lua_helper.ocr_count(ocr_asset_name, ocr_result_var)
            # if searched["succeed"]:
            #     return lua_helper.ocr_count(self.roi_table[i])
        return 0

    def find_table_roi(self):
        # magic
        roi = [1035, 228, 1035 + 831, 228 + 614] if self.current_state == data.MenuState.Items else [1031, 228, 1031 + 831, 228 + 765]
        imax.print(f'box roi: {roi[0]}, {roi[1]}, {roi[2]}, {roi[3]}')
        self.roi_table = [roi]
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

    # ROI 생성 함수 : 영역 설정(sx, sy, ex, ey), 이미지 ROI 사이즈(img_w, img_y)
    def makeRoi(self, _sx, _sy, _ex, _ey, _img_w, _img_h):
        # 서치할 영역의 폭(x), 높이(h) 계산
        width = _ex - _sx
        height = _ey - _sy
        imax.print(f'width : {width}, height : {height}')
        # 서치할 영역 분할 갯수 (서치 영역의 폭 / 검색 거리 간격)
        width_split = int(width / _img_w) - 1
        height_split = int(height / _img_h) - 1
        imax.print(f'width_split : {width_split}, height_split : {height_split}')
        # roi 테이블 생성!
        new_roi_table = []
        # X, Y 좌표 초기값 설정
        x = _sx
        y = _sy
        # ROI용 좌표 생성
        for i in range(0, width_split):
            for j in range(0, height_split):
                x = x + (_img_w*i)
                y = y + (_img_h*j)
            w = _img_w
            h = _img_h
            # print(i, x, y, w, h)
            new_roi_table.append([x, y, w, h])

        # > 저장된 값을 확인해보기 위한 코드
        checker_index = 0
        for value in new_roi_table:
            imax.print(f'#roi no: {checker_index}')
            imax.print(f'x: {value[0]}, y: {value[1]}, w: {value[2]}, h: {value[3]}')
            checker_index += 1
        # imax.print('>> ROI를 생성 완료하였습니다.')
        return new_roi_table

    # NOTE: I wanted to import data but scripting guide is limited
    def set_items_to_count(self, items_dict):
        self.items = items_dict.copy()  # shallow copy(there's no pointer type)

    def set_equipments_to_count(self, equipments_dict):
        self.equipments = equipments_dict.copy()  # shallow copy(there's no pointer type)

