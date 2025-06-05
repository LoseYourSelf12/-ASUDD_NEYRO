# src/config_manager.py
import yaml
import os
from config_models import Settings

class ConfigManager:
    def __init__(self, config_file='configs/skneyro_config.yaml'):
        self.config_file = config_file
        self.settings = self.load_config()

    def load_config(self) -> Settings:
        if not os.path.exists(self.config_file):
            settings = Settings()
            self.save_config(settings.dict())
            return settings
        with open(self.config_file, 'r') as f:
            data = yaml.safe_load(f)
        settings = Settings(**data)
        return settings

    def save_config(self, config_dict):
        with open(self.config_file, 'w') as f:
            yaml.dump(config_dict, f)

    def update_config(self, key, value):
        keys = key.split('.')
        cfg = self.settings.dict()
        ref = cfg
        for k in keys[:-1]:
            ref = ref.setdefault(k, {})
        ref[keys[-1]] = value
        self.settings = Settings(**cfg)
        self.save_config(cfg)
