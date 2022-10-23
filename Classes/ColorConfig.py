import json

class ColorConfigObject():
    def __init__(self, color_config_file) -> None:
        self.color_config_file = color_config_file
        self.theme = ""
        self.color1 = ""
        self.color2 = ""
        self.color3 = ""
        self.color4 = ""
        self.get_config_values()
        
    def get_config_values(self):
        with open(self.color_config_file) as f:
            config_file = json.load(f)
        self.color1 = config_file["color1"]
        self.color2 = config_file["color2"]    
        self.color3 = config_file["color3"]
        self.color4 = config_file["color4"]
        self.theme = config_file["Theme"]
        return


colorConfig = ColorConfigObject('./config_files/colorConfig.json')