MAIN_FONT = r"C:\Users\oliver\Documents\code\python\computing\project\Tower-Defence---Project\assets\fonts\RobotoSlab-VariableFont_wght.ttf"


class Theme:
    def __init__(self, theme_data:dict):
        self.theme_data = theme_data

    def get(self):
        return self.theme_data
    
    def set(self, theme_data:dict):
        for key in theme_data:
            self.theme_data[key] = theme_data[key]

# colors
DARK_BACKGROUND_COLOR = (20, 19, 23)
DARK_SURFACE_LOW_COLOR = (29, 27, 32)
DARK_SURFACE_HOVER_COLOR = (51, 45, 65)
DARK_FOREGROUND_COLOR = (160, 157, 165)
DARK_OUTLINE_COLOR = (110, 109, 117)
DARK_ACCENT_COLOR = (171, 149, 217)

# Themes
# button themes
BUTTON_DARK = Theme({
    "color": DARK_SURFACE_LOW_COLOR,
    "fore_color": DARK_FOREGROUND_COLOR,
    "border_radius": 10,
    "border_width": 0,
    "border_color": DARK_OUTLINE_COLOR,
    "hover_color": DARK_SURFACE_HOVER_COLOR,
    "filled": True,
})

BUTTON_DARK_NO_FILL = Theme({
    "color": DARK_SURFACE_LOW_COLOR,
    "fore_color": DARK_FOREGROUND_COLOR,
    "border_radius": 10,
    "border_width": 0,
    "border_color": DARK_OUTLINE_COLOR,
    "hover_color": DARK_SURFACE_HOVER_COLOR,
    "filled": False,
})


# label themes
LABEL_DARK = Theme({
    "color": DARK_BACKGROUND_COLOR,
    "fore_color": DARK_FOREGROUND_COLOR,
    "border_radius": 0,
    "border_width": 0,
    "border_color": DARK_OUTLINE_COLOR,
    "filled": False,
})

LABEL_DARK_FILLED = Theme({
    "color": DARK_SURFACE_LOW_COLOR,
    "fore_color": DARK_FOREGROUND_COLOR,
    "border_radius": 0,
    "border_width": 0,
    "border_color": DARK_OUTLINE_COLOR,
    "filled": True,
})


# slider themes
SLIDER_DARK = Theme({
    "dot_size": 10,
    "thickness": 5,
    "line_color": DARK_OUTLINE_COLOR,
    "dot_color": DARK_FOREGROUND_COLOR,
})

# dropdown themes
DROPDOWN_DARK = Theme({
    "color": DARK_SURFACE_LOW_COLOR,
    "fore_color": DARK_FOREGROUND_COLOR,
    "border_radius": 10,
    "border_width": 0,
    "border_color": DARK_OUTLINE_COLOR,
    "hover_color": DARK_SURFACE_HOVER_COLOR,
    "filled": True,
})

# rect themes   
RECT_DARK = Theme({
    "color": DARK_BACKGROUND_COLOR,
    "border_radius": 10,
    "border_width": 2,
    "border_color": DARK_OUTLINE_COLOR,
    "filled": True,
})

RECT_DARK_NO_FILL = Theme({
    "color": DARK_BACKGROUND_COLOR,
    "border_radius": 10,
    "border_width": 5,
    "border_color": DARK_OUTLINE_COLOR,
    "filled": False,
})