# Работа с конфигурационным файлом
import yaml
import os
from config_models import Settings

class ConfigManager:
    """Загрузка и сохранение настроек из YAML."""

    def __init__(self, config_file='configs/skneyro_config.yaml'):
        self.config_file = config_file
        self.settings = self.load_config()

    def load_config(self) -> Settings:
        """Чтение конфигурации или создание файла по умолчанию."""
        if not os.path.exists(self.config_file):
            settings = Settings()
            self.save_config(settings.model_dump(by_alias=True))
            return settings
        with open(self.config_file, 'r') as f:
            data = yaml.safe_load(f)
        settings = Settings(**data)
        return settings

    def save_config(self, config_dict):
        """Сохранение конфигурации на диск."""
        with open(self.config_file, 'w') as f:
            yaml.dump(config_dict, f)

    def update_config(self, key, value):
        """Обновление отдельного параметра конфигурации."""
        keys = key.split('.')
        cfg = self.settings.model_dump(by_alias=True)
        ref = cfg
        for k in keys[:-1]:
            ref = ref.setdefault(k, {})
        ref[keys[-1]] = value
        self.settings = Settings(**cfg)
        self.save_config(cfg)