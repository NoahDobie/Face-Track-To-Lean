import json

class ConfigManager:
    def __init__(self, config_file="user_config.json"):
        self.config_file = config_file
        self.config = {
            "left_line_position": 300,
            "right_line_position": 340,
            "left_key": 'q',
            "right_key": 'e',
            "start_stop_key": ']'
        }
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.save_config()  # Save default config if file not found

    def save_config(self):
        with open(self.config_file, "w") as file:
            json.dump(self.config, file, indent=4)

    def get_config(self):
        return self.config

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config()
        print(f"Updated config: {key} = {value}")