import threading
import sys
from constants import UniChars, AnsiCommands, Direction

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
        self.output_string = self.stringify()

    def stringify(self):
        """Converts the cells array into a printable string for stdout"""
        return ''.join(self.cells)

    def print(self):
        """Prints the airfield string to the terminal"""
        sys.stdout.write(AnsiCommands.SAVE_CURSOR)
        sys.stdout.write(AnsiCommands.CURSOR_TO_HOME)
        sys.stdout.write(self.output_string)
        sys.stdout.write(AnsiCommands.RESTORE_CURSOR)
        sys.stdout.flush()

    def initial_print(self):
        """Prints the airfield string without saving the cursor"""
        sys.stdout.write(AnsiCommands.CURSOR_TO_HOME)
        sys.stdout.write(self.output_string)
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
        """Updates the planes position and altitude"""
        if self.direction == Direction.EAST:
            self.x_pos += 2
        elif self.direction == Direction.WEST:
            self.x_pos -= 2
        elif self.direction == Direction.NORTH:
            self.y_pos -= 1
        else:
            self.y_pos += 1

        self.fuel -= 1

        self.print()

    def parse_command(self, command):
        """Interprets validated commands from the user"""
        if command == "n":
            self.direction = Direction.NORTH
        elif command == "s":
            self.direction = Direction.SOUTH
        elif command == "e":
            self.direction = Direction.EAST
        elif command == "w":
            self.direction = Direction.WEST

    def print(self):
        """Prints this plane to the display"""
        sys.stdout.write(AnsiCommands.SAVE_CURSOR)
        sys.stdout.write(f"\x1b[{self.y_pos};{self.x_pos}H")
        sys.stdout.write(UniChars.PLANE_EAST)
        sys.stdout.write(AnsiCommands.RESTORE_CURSOR)
        sys.stdout.flush()

def main_loop(airfield, planes):
    """The main game loop"""
    airfield.print()
    for plane in planes:
        plane.update()
    timer = threading.Timer(1, main_loop, [airfield, planes])
    timer.start()


def main():
    """Entry point for the program"""
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
