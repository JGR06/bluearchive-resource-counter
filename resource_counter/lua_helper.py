import imax


def test():
    a = (137, 132)
    imax.lua("ret, acc, ix, iy, sx, sy = ImageSearch('OCR')")
    imax.lua("print(string.format('ret: %d, acc: %f, ix: %d, iy: %d', ret, acc, ix, iy))")
    ix = imax.lua_get_value('ix')
    iy = imax.lua_get_value('iy')
    imax.lua_set_value('ix', int(ix)-68)
    imax.lua_set_value('iy', int(iy)-66)
    imax.lua("roi = {ix, iy, 137, 132}")
    imax.lua("SetImageROI('OCR', roi)")
    imax.lua("ImageSearch('OCR')")
    ocr_result = imax.lua_get_value("ocr_result")
    imax.print('ix, iy: ', ix, iy)
    imax.print('ocr_result: ', ocr_result)


# roi = integer array
def set_roi_variable(variable_name, roi):
    roi_ix = roi[0]
    roi_iy = roi[1]
    roi_w = roi[2]
    roi_h = roi[3]
    imax.lua(f"{variable_name} = {{{roi_ix}, {roi_iy}, {roi_w}, {roi_h}}}")


def search_image(asset_name):
    imax.lua(f"ret, acc, ix, iy, sx, sy = ImageSearch('{asset_name}')")
    ix = imax.lua_get_value('ix')
    iy = imax.lua_get_value('iy')
    sx = imax.lua_get_value('sx')
    sy = imax.lua_get_value('sy')
    result = imax.lua_get_value('ret')
    accuracy = imax.lua_get_value('acc')

    return {
        "ix": int(ix),
        "iy": int(iy),
        "sx": int(sx),
        "sy": int(sy),
        "succeed": int(result) == 1,
        "accuracy": float(accuracy)
    }


def set_image_roi(asset_name, roi):
    imax.lua(f"SetImageROI('{asset_name}', {{{roi[0]}, {roi[1]}, {roi[2]}, {roi[3]}}})")


# roi = integer array
def ocr_specific_roi(roi, ocr_asset_name='OCR_custom_roi', ocr_variable_name='ocr_custom_roi_result'):
    set_roi_variable('ocr_roi', roi)
    imax.lua(f"SetImageROI('{ocr_asset_name}', ocr_roi)")
    ocr_count(ocr_asset_name, ocr_variable_name)


def ocr_count(ocr_asset_name='OCR', ocr_variable_name='ocr_result'):
    imax.lua(f"ImageSearch('{ocr_asset_name}')")

    ocr_result = imax.lua_get_value(ocr_variable_name)
    # exception handling
    ocr_result = ocr_result.strip()
    ocr_result = ocr_result.replace(' ', '')  # dirty exception handler
    imax.print(f'[OCR_Result]{ocr_asset_name}: {ocr_result}(will be removed except digits)')
    ocr_result = ''.join(filter(str.isdigit, ocr_result))

    # add or modify here when exception found
    if len(ocr_result) > 0:
        result = int(ocr_result)
    else:
        result = 0

    return result


def find_and_click(asset_name):
    imax.lua(f"find_and_click_result = ImageClick('{asset_name}')")
    return int(imax.lua_get_value('find_and_click_result')) == 1


