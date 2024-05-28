
from dataclasses import dataclass, fields
from typing import Any, Callable, Dict, Optional


@dataclass
class BaseSettings:
    # save_callback: Optional[Callable] = None

    def as_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("Each subclass must implement its own as_dict method.")

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]):
        raise NotImplementedError("Each subclass must implement its own from_dict method.")

    def validate(self) -> bool:
        raise NotImplementedError("Each subclass must implement its own validation method.")

    def reset_to_defaults(self):
        for field in fields(self):
            setattr(self, field.name, field.default_factory())


class DefaultDictMixin:
    def as_dict(self) -> Dict[str, Any]:
        """Convert the current configuration to a dictionary."""
        return {field.name: getattr(self, field.name) for field in fields(self)}

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'DefaultDictMixin':
        """Create an instance from a dictionary."""
        field_names = {f.name for f in fields(cls)}
        filtered_dict = {k: v for k, v in config_dict.items() if k in field_names}
        return cls(**filtered_dict)
