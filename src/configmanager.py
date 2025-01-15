import configparser

class ConfigManager:
    def __init__(self, config_file='./config/config.properties'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.config_file = config_file

    def get_config(self):
        return {
            "camera_preview_width": self.config.getint('DEFAULT', 'camera.preview.width'),
            "camera_preview_height": self.config.getint('DEFAULT', 'camera.preview.height'),
            "left_line_position": self.config.getint('DEFAULT', 'left.line.position'),
            "right_line_position": self.config.getint('DEFAULT', 'right.line.position'),
            "left_key": self.config.get('DEFAULT', 'left.key'),
            "right_key": self.config.get('DEFAULT', 'right.key'),
            "start_stop_key": self.config.get('DEFAULT', 'start.stop.key')        
        }

    def update_config(self, key, value):
        # Ensure the value is saved as an integer if it is a line position
        if key in ["left.line.position", "right.line.position"]:
            value = int(value)
        self.config.set('DEFAULT', key, str(value))
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)