
from dataclasses import dataclass, field
from typing import Dict, List

from src.application_config.app_logger import app_logger
from src.application_config.base.base_settings import BaseSettings


def default_directories_to_police() -> Dict[str, str]:
    return {
        '0': "C:/Viper",
        '1': "C:/ViperConfigData",
        '2': "",
        '3': "",
    }


def default_temp_file_extensions() -> Dict[str, List[str]]:
    return {
        '0': [".py", ".cs"],
        '1': [".md", ".txt"],
    }


@dataclass
class FileCenterSettings(BaseSettings):
    directories_to_police: Dict[str, str] = field(default_factory=default_directories_to_police)
    temp_file_extensions: Dict[str, List[str]] = field(default_factory=default_temp_file_extensions)

    def get_directory_to_police(self, uid: int) -> str:
        return self.directories_to_police.get(str(uid), "Error")

    def set_directory_to_police(self, uid: int, value: str):
        self.directories_to_police[str(uid)] = value

    def get_temp_file_extensions(self, uid: int) -> List[str]:
        return self.temp_file_extensions.get(str(uid), ['Error'])

    def set_temp_file_extensions(self, uid: int, value: List[str]):
        self.temp_file_extensions[str(uid)] = value

    def validate(self) -> bool:
        return self._validate_directories() and self._validate_extensions()

    def _validate_directories(self) -> bool:
        for key, directory in self.directories_to_police.items():
            if not isinstance(key, str):
                app_logger.error("Invalid key: %s", key)
                return False
            if not isinstance(directory, str):
                app_logger.error("Invalid directory: %s", directory)
                return False
        return True

    def _validate_extensions(self) -> bool:
        for key, extensions in self.temp_file_extensions.items():
            if not isinstance(key, str):
                app_logger.error("Invalid key: %s", key)
                return False
            if not all(isinstance(ext, str) for ext in extensions):
                app_logger.error("Invalid extensions in key %s: %s", key, extensions)
                return False
        return True
