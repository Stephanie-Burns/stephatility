
from enum import StrEnum


NUMBER_ROW_DIGIT_KEY_CODES      = range(9, 20)
NUMPAD_DIGIT_KEY_CODES          = range(78, 91)
DIGIT_KEYCODES                  = NUMBER_ROW_DIGIT_KEY_CODES and NUMPAD_DIGIT_KEY_CODES
SHIFT_MODIFIER_APPLIED_CODE     = 17


class EventAction(StrEnum):
    """Enumeration of actions to take in response to TkInter events."""
    BREAK = "break"
    CONTINUE = "continue"


class EntryValidation(StrEnum):
    """Enumeration of types of TkInter EntryWidget validation."""
    INSERT = '1'
    DELETE = '0'


class KeySym(StrEnum):
    """
    Enumeration of common TkInter keyboard symbols.
    Detailed map at: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
    """
    Return = "Return"
    KP_Enter = "KP_Enter"
    Tab = "Tab"
    ISO_Left_Tab = "ISO_Left_Tab"
    Period = "."
