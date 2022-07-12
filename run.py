import threading
import sys
import enum

class UniChars(str, enum.Enum):
    MIDDLE_DOT = "\u00B7"
    PLANE_EAST = "\u25B6"
    PLANE_WEST = "\u25C0"
    PLANE_NORTH = "\u25B2"
    PLANE_SOUTH = "\u25BC"

class Colors(str, enum.Enum):
    BLUE = "\x1b[38;5;12"

class AnsiCommands(str, enum.Enum):
    SAVE_CURSOR = f"\x1b7"
    RESTORE_CURSOR = f"\x1b8"
    CARRIAGE_RETURN = f"\r"
    TERMINAL_BELL = f"\a"
    CLEAR_SCREEN = f"\x1b[2J"
    CLEAR_LINE = f"\x1b[2K"
    CURSOR_TO_HOME = f"\x1b[H"
    CURSOR_UP_ONE_LINE = f"\x1b[1A"

class Direction(enum.Enum):
    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"

class Airfield:
    """
    Represents the airfield that the game is played on
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
        for _ in range(width * height):
            if _ % self.width < 60:
                self.cells.append(UniChars.MIDDLE_DOT)
            else:
                self.cells.append(" ")
        self.background = self.cells[:]

    def update(self, planes):
        self.cells = self.background[:]
        for plane in planes:
            cell_number = plane.x_pos + plane.y_pos * self.width
            if plane.direction == Direction.NORTH:
                self.cells[cell_number] = UniChars.PLANE_NORTH
            elif plane.direction == Direction.SOUTH:
                self.cells[cell_number] = UniChars.PLANE_SOUTH
            elif plane.direction == Direction.WEST:
                self.cells[cell_number] = UniChars.PLANE_WEST
            else:
                self.cells[cell_number] = UniChars.PLANE_EAST

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
        """Prints the airfield string without saving the cursor"""
        sys.stdout.write(AnsiCommands.CURSOR_UP_ONE_LINE)
        sys.stdout.write(AnsiCommands.CURSOR_TO_HOME)
        sys.stdout.write(self.stringify())
        sys.stdout.flush()

class Plane:
    """
    Represents an airplane
    """
    def __init__(self):
        self.x_pos = 10
        self.y_pos = 10
        self.altitude = 5
        self.fuel = 50
        self.direction = Direction.EAST
        self.color = None
    
    def update(self):
        if self.direction == Direction.EAST:
            self.x_pos += 1
        elif self.direction == Direction.WEST:
            self.x_pos -= 1
        elif self.direction == Direction.NORTH:
            self.y_pos -= 1
        else:
            self.y_pos += 1

        self.fuel -= 1

    def parse_command(self, command):
        if command == "n":
            self.direction = Direction.NORTH
        elif command == "s":
            self.direction = Direction.SOUTH
        elif command == "e":
            self.direction = Direction.EAST
        elif command == "w":
            self.direction = Direction.WEST

def main_loop(airfield, planes):
    for plane in planes:
        plane.update()
    airfield.update(planes)
    airfield.print()
    t = threading.Timer(1, main_loop, [airfield, planes])
    t.start()


def main():
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.flush()
    airfield = Airfield(80, 20)
    airfield.initial_print()
    planes = []
    plane_1 = Plane()
    planes.append(plane_1)
    main_loop(airfield, planes)
    while True:
        command = input("Enter command : ")
        plane_1.parse_command(command)
        sys.stdout.write(AnsiCommands.CURSOR_UP_ONE_LINE)
        sys.stdout.write(AnsiCommands.CLEAR_LINE)

main()