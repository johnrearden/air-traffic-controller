import enum
import random

class UniChars(str, enum.Enum):
    """ 
    Holds the Unicode characters used in the game 
    """
    MIDDLE_DOT = "\u00B7"
    PLANE_EAST = "\u25B6"
    PLANE_WEST = "\u25C0"
    PLANE_NORTH = "\u25B2"
    PLANE_SOUTH = "\u25BC"
    BOX_HORIZONTAL = "\u2550"
    BOX_VERTICAL = "\u2551"
    BOX_TOP_LEFT = "\u2554"
    BOX_TOP_RIGHT = "\u2557"
    BOX_BOTTOM_RIGHT = "\u255D"
    BOX_BOTTOM_LEFT = "\u255A"
    HORIZONTAL_LINE = "\u2500"
    LEFT_ARROW = "\u27F5"
    STAR = "\u2605"

class Colors(str, enum.Enum):
    """
    Holds the colors used in the game
    """
    FOREGROUND_BLUE = "\x1b[38;5;12m"
    FOREGROUND_CYAN = "\x1b[38;5;14m"
    FOREGROUND_GREEN = "\x1b[38;5;10m"
    FOREGROUND_YELLOW = "\x1b[38;5;11m"
    FOREGROUND_PURPLE = "\x1b[38;5;13m"
    FOREGROUND_ORANGE = "\x1b[38;5;208m"
    FOREGROUND_RED = "\x1b[38;5;9m"

    @staticmethod
    def random():
        """Choose a random color from the above values"""
        return random.choice(list(Colors))

    @staticmethod
    def random_full():
        """Create a random color"""
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return f"\x1b[38;2;{red};{green};{blue}"

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
    BLINK = "\x1b[5m"
    NORMAL = "\x1b[0m"
    FAINT = "\x1b[2m"
    DEFAULT_COLOR = "\x1b[00m"

class Direction(enum.Enum):
    """
    An enum representing the four cardinal points of the compass
    """
    NORTH = UniChars.PLANE_NORTH
    EAST = UniChars.PLANE_EAST
    SOUTH = UniChars.PLANE_SOUTH
    WEST = UniChars.PLANE_WEST

    def get_character(self):
        """Returns the value associated with the enum key"""
        return self.value

    @staticmethod
    def get_direction(letter):
        """Returns the direction enum associated with the given string"""
        if letter == "n":
            return Direction.NORTH
        if letter == "e":
            return Direction.EAST
        if letter == "s":
            return Direction.SOUTH
        else:
            return Direction.WEST

class EntryPoints(enum.Enum):
    """
    An enum representing the coordinates at which a plane can 
    enter the airfield, and the initial direction the plane
    is travelling in. The values are wrapped in a tuple.
    """
    POINT_1 = (50, 1, Direction.SOUTH)
    POINT_2 = (24, 19, Direction.NORTH)
    POINT_3 = (12, 1, Direction.SOUTH)
    POINT_4 = (0, 6, Direction.EAST)
    POINT_5 = (60, 14, Direction.WEST)

    @staticmethod
    def random():
        """Choose a random entry point from the above values"""
        return random.choice(list(EntryPoints)).value

