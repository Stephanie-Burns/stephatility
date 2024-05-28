
import os
import json

from src.application_config.app_logger import app_logger
from src.application_config.base.base_settings import BaseSettings
from src.engine.file_center.file_center_settings import FileCenterSettings
from src.engine.network_center.network_center_settings import NetworkCenterSettings


class UserSettings:
    def __init__(self, settings_path: str):
        self.settings_path = settings_path
        self.file_center = FileCenterSettings()
        self.network_center = NetworkCenterSettings()

        self.load_settings()

    def load_settings(self) -> None:
        if not os.path.exists(self.settings_path) or os.stat(self.settings_path).st_size == 0:
            app_logger.info("Settings file does not exist or is empty. Creating default settings.")
            self.save_settings()
        else:
            app_logger.info("Loading settings from %s", self.settings_path)
            try:
                with open(self.settings_path, 'r') as file:
                    settings_data = json.load(file)

                for attr, value in self.__dict__.items():
                    if isinstance(value, BaseSettings):
                        settings_section = settings_data.get(value.__class__.__name__, {})
                        updated_settings = value.__class__.from_dict(settings_section)
                        setattr(self, attr, updated_settings)
                app_logger.info("Settings loaded successfully.")

            except Exception as e:
                app_logger.error("Failed to load settings: %s", e)
                app_logger.info("Creating default settings.")
                self.save_settings()

    def save_settings(self) -> None:
        all_settings = {
            value.__class__.__name__: value.as_dict()
            for value in self.__dict__.values()
            if isinstance(value, BaseSettings)
        }

        try:
            with open(self.settings_path, 'w') as file:
                json.dump(all_settings, file, indent=4)
            app_logger.info("Settings saved successfully to %s", self.settings_path)
        except Exception as e:
            app_logger.error("Failed to save settings: %s", e)
