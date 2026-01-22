from core.display_number import get_display_number

WINDOW_MAIN_SIZE = [
    get_display_number( multipler=0.5, based="width" ),
    get_display_number( multipler=0.5, based="height" )
]

SET_ITEM_DIALOG_SIZE = [
    get_display_number( multipler=0.3, based="width" ),
    get_display_number( multipler=0.5, based="height" )
]

FONT_SIZE = get_display_number( multipler=0.0085, based="width" )
MARGIN_XY = [
    get_display_number( multipler=0.003, based="width" ),
    get_display_number( multipler=0.003, based="height" )
]
PADDING_SPACE = get_display_number( multipler=0.003, based="width" )
