class Page(object):
    def __init__(self, chinese, answer, hint='', error_count_before_hint=2, show_survey=0,
                 is_test=False, marker_data = ''):
        self.chinese = chinese
        self.answer = answer
        self.error_count_before_hint = error_count_before_hint
        self.hint = hint
        self.show_survey = show_survey
        self.is_test = is_test
        self.marker_data = marker_data

PAGES = [
    Page('红', 'red', hint='红 = red'),
    Page('黄', 'yellow', hint='黄 = yellow'),
    Page('红', 'red'),
    Page('黄', 'yellow'),
    Page('红', 'red'),
    Page('黄', 'yellow'),
    Page('红', 'red'),
    Page('黄', 'yellow'),
    Page('红', 'red'),
    Page('黄', 'yellow', show_survey=1),
    
    Page('绿', 'green', hint='绿 = green'),
    Page('绿', 'green'),
    Page('紫', 'purple', hint='紫 = purple'),
    Page('紫', 'purple'),
    Page('绿 紫', 'green purple'),
    Page('紫 绿', 'purple green'),
    Page('蓝', 'blue', hint='蓝 = blue'),
    Page('蓝', 'blue'),
    Page('蓝 绿', 'blue green'),
    Page('紫 蓝', 'purple blue', show_survey=2),

    Page('黑', 'black', hint='黑 = black'),
    Page('橙', 'orange', hint='橙 = orange'),
    Page('棕', 'brown', hint='棕 = brown'),
    Page('粉', 'pink', hint='粉 = pink'),
    Page('白', 'white', hint='白 = white'),
    Page('白 棕 粉', 'white brown pink'),
    Page('橙 绿 蓝', 'orange green blue'),
    Page('黑 红 粉', 'black red pink'),
    Page('紫 棕 蓝', 'purple brown blue'),
    Page('绿 黄 白', 'green yellow white', show_survey=3),
]

    

