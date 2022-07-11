import threading
import sys
import enum

class UniChars(str, enum.Enum):
    MIDDLE_DOT = "\u00B7"

class AnsiCommands(str, enum.Enum):
    SAVE_CURSOR = f"\x1b7"
    RESTORE_CURSOR = f"\x1b8"
    CARRIAGE_RETURN = f"\r"
    TERMINAL_BELL = f"\a"
    CLEAR_SCREEN = f"\x1b[2J"
    CURSOR_TO_HOME = f"\x1b[H"

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

    def initial_print(self):
        sys.stdout.write(AnsiCommands.CURSOR_TO_HOME)
        sys.stdout.write(self.stringify())
        sys.stdout.flush()

CLEAR_SCREEN = "\x1b[2J"

def main():
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.flush()
    airfield = Airfield(80, 20)
    airfield.initial_print()
    command = input("Enter command : ")

main()