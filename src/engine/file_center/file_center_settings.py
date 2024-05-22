
from dataclasses import dataclass, field
from typing import List

from src.application_config.base_settings import BaseSettings


def default_directories_to_police() -> List[str]:
    return [
        "C:/Viper",
        "C:/ViperConfigData",
    ]


def default_temp_file_extensions() -> List[str]:
    return [
        ".py", ".cs", ".md", ".txt",
    ]


@dataclass
class FileCenterSettings(BaseSettings):
    directories_to_police: List[str] = field(default_factory=default_directories_to_police)
    temp_file_extensions: List[str] = field(default_factory=default_temp_file_extensions)

    def validate(self) -> bool:
        return True
