import threading
import sys
import string
import random
from constants import UniChars, AnsiCommands, Direction, Colors, EntryPoints

class Airfield:
    """
    Represents the airfield that the game is played on
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.plane_names = list(string.ascii_lowercase)
        random.shuffle(self.plane_names)
        self.cells = []
        for _ in range(width * height):
            self.cells.append(" ")
        for ind in range(60):
            self.cells[ind] = UniChars.BOX_HORIZONTAL
            self.cells[ind + width * (height - 1)] = UniChars.BOX_HORIZONTAL
        for ind in range(0, 20):
            self.cells[width * ind] = UniChars.BOX_VERTICAL
            self.cells[ind * width - 20] = UniChars.BOX_VERTICAL
        list_1 = [i for i in range(822, 837)]
        list_2 = ["-", "-", " ", "R", "U", "N", "W", "A", "Y", " ", "-", "-"]
        for ind, char in zip(list_1, list_2):
            self.cells[ind] = UniChars.HORIZONTAL_LINE
            self.cells[ind + width * 2] = UniChars.HORIZONTAL_LINE
            self.cells[ind + width] = char
        self.cells[915] = UniChars.LEFT_ARROW
        self.cells[0] = UniChars.BOX_TOP_LEFT
        self.cells[60] = UniChars.BOX_TOP_RIGHT
        self.cells[19 * width] = UniChars.BOX_BOTTOM_LEFT
        self.cells[19 * width + 60] = UniChars.BOX_BOTTOM_RIGHT
        list_1 = [i for i in range(62, 73)]
        list_2 = [UniChars.PLANE_EAST, " "," ", "F", "U", "E", "L", " ", "A", "L", "T"]
        for ind, char in zip(list_1, list_2):
            self.cells[ind] = char
        
        for entry_point in EntryPoints:
            x = entry_point.value[0]
            y = entry_point.value[1]
            self.cells[x + y * width] = " "

        self.output_string = self.stringify()

    def stringify(self):
        """Converts the cells array into a printable string for stdout"""
        return ''.join(self.cells)

    def print(self):
        """Prints the airfield string to the terminal"""
        sys.stdout.write(AnsiCommands.SAVE_CURSOR)
        sys.stdout.write(AnsiCommands.CURSOR_TO_HOME)
        sys.stdout.write(self.output_string)

        # Write the details of the planes to the plane display
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
    def __init__(self, identity):
        self.identity = identity
        (self.x_pos, self.y_pos, self.direction) = EntryPoints.random()
        self.altitude = 5
        self.fuel = 50
        self.color = Colors.random()

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
        sys.stdout.write(f"\x1b[{self.y_pos + 1};{self.x_pos + 1}H")
        sys.stdout.write(self.color.value)
        sys.stdout.write(f"{self.direction.get_character()} {self.identity}")
        sys.stdout.write(AnsiCommands.RESTORE_CURSOR)
        sys.stdout.flush()

def main_loop(airfield, planes, counter):
    """The main game loop"""
    airfield.print()
    if len(planes) < 8:
        next_identifier = airfield.plane_names.pop(0)
        plane = Plane(next_identifier)
        planes[next_identifier] = plane
        airfield.plane_names.append(next_identifier)
    for plane in planes.values():
        plane.update()
    timer = threading.Timer(1, main_loop, [airfield, planes, counter + 1])
    timer.start()


def main():
    """Entry point for the program"""
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.flush()
    airfield = Airfield(80, 20)
    airfield.initial_print()
    planes = {}
    main_loop(airfield, planes, 0)
    while True:
        command = input("Enter command : ")
        plane_1.parse_command(command)
        sys.stdout.write(AnsiCommands.CURSOR_UP_ONE_LINE)
        sys.stdout.write(AnsiCommands.CLEAR_LINE)

main()
