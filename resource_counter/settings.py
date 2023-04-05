# settings should be separated by env(DEV, STG, PROD), but this is just script so use plain variables

# debug options
DEBUG_SAVE_MISRECOGNITIONS = False
DEBUG_SAVE_NAME_REPLACED_RESULT = False

# output options
SAVE_RESULT_DIFF = True
RESULT_DIFF_WARNING_THRESHOLD = 50

# stop searching and scrolling if there is no result during N times of scrolling
SCROLL_COUNT_LIMIT_UNTIL_FOUND = 5

# returning to lobby occurs network request -- then can't send any input til request ends
DELAY_AFTER_BACK_BUTTON = 3.5

# delay before table ui refreshed
DELAY_BEFORE_TABLE_UI_ENTERED = 1.5

# delay after each recognition loop
DELAY_AFTER_TABLE_RECOGNITION_LOOP = 0.5

# delay after table scroll
DELAY_AFTER_TABLE_SCROLL = 1.0

# amount for each table scrolling
TABLE_SCROLL_AMOUNT = -380

# minimum lines to skip searching(depend on TABLE_SCROLL_AMOUNT)
LINES_TO_CHECK_PER_SCROLL = 2

# delay after clicked items which we're looking for (wait for UI refreshed)
DELAY_AFTER_ITEM_CLICK = 0.25
