MAIN_FONT = "comic-sans"

class Theme:
    def __init__(self, theme_data:dict):
        self.theme_data = theme_data

    def get(self):
        return self.theme_data
    
    def set(self, theme_data:dict):
        for key in theme_data:
            self.theme_data[key] = theme_data[key]

# Themes
# button themes
BUTTON_DARK = Theme({
    "color": (20,20,20),
    "fore_color": (200,200,200),
    "border_radius": 10,
    "border_width": 2,
    "border_color": (150,150,150),
    "hover_color": (50, 50, 50),
    "filled": True,
})

BUTTON_DARK_NO_FILL = Theme({
    "color": (20,20,20),
    "fore_color": (200,200,200),
    "border_radius": 10,
    "border_width": 0,
    "border_color": (150,150,150),
    "hover_color": (50, 50, 50),
    "filled": False,
})


# label themes
LABEL_DARK = Theme({
    "color": (20,20,20),
    "fore_color": (200,200,200),
    "border_radius": 0,
    "border_width": 0,
    "border_color": (0,0,0),
    "filled": False,
})


# slider themes
SLIDER_DARK = Theme({
    "dot_size": 10,
    "thickness": 5,
    "line_color": (100,100,100),
    "dot_color": (200,200,200),
})

# dropdown themes
DROPDOWN_DARK = Theme({
    "color": (20,20,20),
    "fore_color": (200,200,200),
    "border_radius": 10,
    "border_width": 2,
    "border_color": (150,150,150),
    "hover_color": (50, 50, 50),
    "filled": True,
})