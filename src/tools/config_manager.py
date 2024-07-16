import json
import os.path


class ConfigManager:
    config_path: str = ''

    def __init__(self, config_path: str = 'config.json') -> None:
        self.config_path = config_path

    def get_config(self) -> dict:
        if not os.path.exists(self.config_path):
            self.create_config()

        return json.load(open(self.config_path))

    def get_value(self, key: str):
        return self.get_config()[key]

    def create_config(self) -> None:
        new_config: dict = {
            "music_dir": '',
            "hitmo_integration": False
        }

        json.dump(new_config, open(self.config_path, 'w'), indent=4)

    def update_config(self, new_config: dict) -> None:
        json.dump(new_config, open(self.config_path, 'w'))

    def update_value(self, key: str, new_value) -> None:
        config: dict = self.get_config()
        config[key] = new_value
        self.update_config(config)
