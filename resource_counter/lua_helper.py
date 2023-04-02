import time
import base64
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
        'ix': int(ix),
        'iy': int(iy),
        'sx': int(sx),
        'sy': int(sy),
        'succeed': int(result) == 1,
        'accuracy': float(accuracy)
    }


# return all searched images from screen(sorted by most accurate)
def search_all_images_from_screen(asset_name):
    imax.lua(f"result_count, result_table = ImageSearchMultipleResults('{asset_name}', SORT_PTDIST, {{0, 0}})")
    # copied code: remove same position images (in fact, it's not sqrt comparison)
    # I just don't wanted to type code for this... TODO:fixthis
    imax.lua(f"""for i=1, result_count do
                    if i+1 <= result_count and math.abs(result_table[i].ix-result_table[i+1].ix)+math.abs(result_table[i].iy-result_table[i+1].iy)<=15 then
                    table.remove(result_table, i)
                    result_count = result_count-1
                    i = i - 1
                end
            end""")
    # lua's array index starts from 1, weird...
    results = []
    result_count = int(imax.lua_get_value('result_count'))
    for index in range(1, 1 + result_count):
        # imax.lua_get_value() can't retrieve like 'array[index].property'... so make it global variable
        imax.lua(f"""mix = result_table[{index}].ix
        miy = result_table[{index}].iy
        msx = result_table[{index}].sx
        msy = result_table[{index}].sy
        macc = result_table[{index}].acc""")
        ix = imax.lua_get_value(f'mix')
        iy = imax.lua_get_value(f'miy')
        sx = imax.lua_get_value(f'msx')
        sy = imax.lua_get_value(f'msy')
        accuracy = imax.lua_get_value(f'macc')
        results.append({'ix': int(ix), 'iy': int(iy), 'sx': int(sx), 'sy': int(sy), 'accuracy': float(accuracy)})

    results = sorted(results, key=lambda x: x['accuracy'], reverse=True)
    return results


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


def ocr(ocr_asset_name, ocr_variable_name):
    imax.lua(f"ImageSearch('{ocr_asset_name}')")

    # imax lua script throws cp949 string and occurs error when string contains korean(on imax.lua_get_value() executed)
    # so make string base64 encoded, then decode on python script
    imax.lua(f'temp_target = {ocr_variable_name}')
    imax.lua('''local b='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
-- encoding
function enc(data)
    return ((data:gsub('.', function(x) 
        local r,b='',x:byte()
        for i=8,1,-1 do r=r..(b%2^i-b%2^(i-1)>0 and '1' or '0') end
        return r;
    end)..'0000'):gsub('%d%d%d?%d?%d?%d?', function(x)
        if (#x < 6) then return '' end
        local c=0
        for i=1,6 do c=c+(x:sub(i,i)=='1' and 2^(6-i) or 0) end
        return b:sub(c+1,c+1)
    end)..({ '', '==', '=' })[#data%3+1])
end
    temp_target = enc(temp_target)
    ''')

    ocr_result = imax.lua_get_value('temp_target')
    result_bytes = base64.b64decode(ocr_result)
    result = result_bytes.decode('cp949')
    result = result.strip()

    return result


def find_and_click(asset_name):
    imax.lua(f"find_and_click_result = ImageClick('{asset_name}')")
    return int(imax.lua_get_value('find_and_click_result')) == 1


def click(ix, iy):
    imax.lua(f'Mouse(LBUTTON, CLICK, {ix}, {iy})')


# scroll_amount: negative is wheel-up, positive is wheel-down
def scroll_and_wait(scroll_amount=-380, sleep_time=1.0):
    base_y = 755
    # Mouse(LBUTTON, WHEELDOWN, ...) method is not working, so use DRAG instead.
    imax.lua(f'Mouse(LBUTTON, DRAG, 1275, {base_y}, 1275, {base_y + scroll_amount})')
    time.sleep(sleep_time)

