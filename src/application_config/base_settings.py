
from dataclasses import dataclass, fields
from typing import Any, Dict

@dataclass
class BaseSettings:
    def as_dict(self) -> Dict[str, Any]:
        # Properly use fields here
        return {field.name: getattr(self, field.name) for field in fields(self)}

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]):
        field_names = {f.name for f in fields(cls)}
        filtered_dict = {k: v for k, v in config_dict.items() if k in field_names}
        return cls(**filtered_dict)

    def reset_to_defaults(self):
        for field in fields(self):
            setattr(self, field.name, field.default_factory())

    def validate(self) -> bool:
        raise NotImplementedError("Each subclass must implement its own validation method.")
