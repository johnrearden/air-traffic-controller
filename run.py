import threading
import sys
import enum

class UniChars(enum.Enum):
    MIDDLE_DOT = "\u00B7"

class AnsiCommands(enum.Enum):
    SAVE_CURSOR = "\x1b7"
    RESTORE_CURSOR = "\x1b8"
    CARRIAGE_RETURN = "\r"
    CURSOR_TO_HOME = "\x1b[H"

class Airfield:
    """
    Represents the airfield that the game is played on
    """
    def __init__(self, width, height):
        self.cells = []
        for _ in range(width * height):
            self.cells.append(UniChars.MIDDLE_DOT)

    def stringify(self):
        """Converts the cells array into a printable string for stdout"""
        return ''.join(self.cells)

    def print(self):
        """Prints the airfield string to the terminal"""
        sys.stdout.write(AnsiCommands.SAVE_CURSOR)
        sys.stdout.write(AnsiCommands.CURSOR_TO_HOME)
        sys.stdout.write(self.stringify())
        sys.stdout.write(AnsiCommands.RESTORE_CURSOR)
        sys.stdout.flush()

          