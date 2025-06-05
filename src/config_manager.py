# src/config_manager.py
import yaml
import os

class ConfigManager:
    def __init__(self, config_file='configs/skneyro_config.yaml'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            default_config = {
                "NDC": {
                    "apply": False,
                    "Time_zone": "+3",
                    "type_id": 101,
                    "id": "Demo",
                    "zone_pref": "1",
                    "Name_Obj": "Test_Van_1",
                    "adr_1": "http://192.168.2.100:8000",
                    "adr_2": "http://192.168.2.101:8000"
                },
                "PTI": {
                    "apply": True,
                    "interval": 15,
                    "tim_beg": "00:00:00"
                },
                "DII": {
                    "apply": True,
                    "display": 0
                }
                # Дополнительные параметры протокола можно добавить здесь
            }
            self.save_config(default_config)
            return default_config
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def save_config(self, config):
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f)
        self.config = config

    def update_config(self, key, value):
        keys = key.split('.')
        cfg = self.config
        for k in keys[:-1]:
            cfg = cfg.setdefault(k, {})
        cfg[keys[-1]] = value
        self.save_config(self.config)
