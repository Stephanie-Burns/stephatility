
from enum import StrEnum


class EventAction(StrEnum):
    """Enumeration of actions to take in response to TkInter events."""
    BREAK = "break"
    CONTINUE = "continue"


class EntryValidation(StrEnum):
    """Enumeration of types of TkInter EntryWidget validation."""
    INSERT = '1'
    DELETE = '0'

class WidgetState(StrEnum):
    ENABLED = "!disabled"
    DISABLED = "disabled"


class KeySym(StrEnum):
    """
    Enumeration of common TkInter keyboard symbols.
    Detailed map at: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
    """
    RETURN = "Return"
    KP_Enter = "KP_Enter"
    TAB = "Tab"
    PERIOD = "."


class KeyBind(StrEnum):
    RETURN = '<Return>'
    ENTER = '<KP_Enter>'
    KEY_RELEASE = '<KeyRelease>'
