import enum

class UniChars(str, enum.Enum):
    """ 
    Holds the Unicode characters used in the game 
    """
    MIDDLE_DOT = "\u00B7"
    PLANE_EAST = "\u25B6"
    PLANE_WEST = "\u25C0"
    PLANE_NORTH = "\u25B2"
    PLANE_SOUTH = "\u25BC"

class Colors(str, enum.Enum):
    """
    Holds the colors used in the game
    """
    BLUE = "\x1b[38;5;12"

class AnsiCommands(str, enum.Enum):
    """
    Holds the cursor movement and output deletion commands
    """
    SAVE_CURSOR = f"\x1b7"
    RESTORE_CURSOR = f"\x1b8"
    CARRIAGE_RETURN = f"\r"
    TERMINAL_BELL = f"\a"
    CLEAR_SCREEN = f"\x1b[2J"
    CLEAR_LINE = f"\x1b[2K"
    CURSOR_TO_HOME = f"\x1b[H"
    CURSOR_UP_ONE_LINE = f"\x1b[1A"

class Direction(enum.Enum):
    """
    An enum representing the four cardinal points of the compass
    """
    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"