import settings
import json


class ConfigManager:
    @staticmethod
    def get_config() -> dict:
        return json.load(open(settings.CONFIG_FILE, 'r'))

    @staticmethod
    def update_config(new_config: dict) -> None:
        json.dump(new_config, open(settings.CONFIG_FILE, 'w'))