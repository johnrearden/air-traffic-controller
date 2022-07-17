import threading
import sys
import string
import random
from constants import UniChars, AnsiCommands, Direction, Colors, EntryPoints
from utilities import getMoveCursorString

allow_list = ["n", "north", "e", "east", "s", "south", "w", "west",
              "circle", "c", "land", "l", "5000", "4000", "3000", "2000", "1000"]

class Airfield:
    """
    Represents the airfield that the game is played on
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.planes = {}
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
        
        for entry_point in EntryPoints:
            x = entry_point.value[0]
            y = entry_point.value[1]
            self.cells[x + y * width] = " "

        self.output_string = self.stringify()

    def stringify(self):
        """Converts the cells array into a printable string for stdout"""
        return ''.join(self.cells)

    def print(self, planes):
        """Prints the airfield string and plane summary to the terminal"""
        
        sys.stdout.write(AnsiCommands.SAVE_CURSOR)
        sys.stdout.write(AnsiCommands.CURSOR_TO_HOME)
        sys.stdout.write(self.output_string)

        # Write the details of the planes to the plane summary
        sys.stdout.write(getMoveCursorString(63, 0))
        sys.stdout.write(f"{UniChars.PLANE_EAST}  FUEL ALTITUDE")
        display_list = list(enumerate(planes.values(), start=2))
        for item in display_list:
            y = item[0]
            plane = item[1]
            sys.stdout.write(getMoveCursorString(63, y))
            sys.stdout.write(plane.color.value)
            sys.stdout.write(plane.identity)
            sys.stdout.write(f"   {plane.fuel}")
            sys.stdout.write(getMoveCursorString(71, y))
            sys.stdout.write(f"{plane.altitude}")

        # Restore the cursor to the input line and flush the buffer
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
        self.altitude = 5000
        self.fuel = 50
        self.color = Colors.random()
        self.eliminated = False

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

        # If the plane has left the airfield, flag it as eliminated
        if self.x_pos < 1 or self.x_pos > 58 or self.y_pos < 2 or self.y_pos > 19:
            self.eliminated = True

        # If the plane has run out of fuel, flag it as eliminated
        if self.fuel <= 0:
            self.eliminated = True

        if not(self.eliminated):
            self.print()

    def execute_commands(self, commands):
        """Takes a validated set of commands and passed them on
           to the correct functions for modifying plane properties"""
        for command in commands:
            if command.isdigit():
                self.change_altitude(command)
            else :
                abbreviation = command[0]
                if abbreviation in ["n", "e", "s", "w"]:
                    self.change_direction(abbreviation)

    def change_altitude(self, new_alt):
        """Sets a new altitude target for this plane and begins to adjust the 
           current altitude incrementally"""
        self.altitude = int(new_alt)
        print_message(f"Plane {self.identity}: r waltitude set to {new_alt}")

    def change_direction(self, new_dir):
        """Sets a new direction target for this plane and begins to adjust the 
           current altitude incrementally"""
        self.direction = Direction.get_direction(new_dir)
        print_message(f"Plane {self.identity}: heading set to {new_dir}")
    
    def print(self):
        """Prints this plane to the display"""
        sys.stdout.write(AnsiCommands.SAVE_CURSOR)
        sys.stdout.write(getMoveCursorString(self.x_pos, self.y_pos))
        sys.stdout.write(self.color.value)
        sys.stdout.write(f"{self.direction.get_character()} {AnsiCommands.FAINT}{self.identity}")
        sys.stdout.write(AnsiCommands.NORMAL)
        sys.stdout.write(AnsiCommands.RESTORE_CURSOR)
        sys.stdout.flush()

def main_loop(airfield, planes, counter):
    """The main game loop"""
    airfield.print(planes)
    rand = random.randint(1, 100)
    should_add_plane = (len(planes) < 4 and rand < 30) or len(planes) == 0
    if should_add_plane:
        next_identifier = airfield.plane_names.pop(0)
        plane = Plane(next_identifier)
        planes[next_identifier] = plane
        airfield.plane_names.append(next_identifier)
    for plane in planes.values():
        plane.update()
    airfield.planes = {key:plane for (key, plane) in planes.items() if plane.eliminated is False}
    timer = threading.Timer(3, main_loop, [airfield, airfield.planes, counter + 1])
    timer.start()

def validate_command(command, planes, allowed_commands):
    """Ensure commands entered by user are valid"""
    if len(command) == 0:
        print_message("You didn't enter anything!", True)
        return
    if len(command) > 16:
        print_message("Command is too long!", True)
        return

    elements = command.split(" ")
    if elements[0] not in planes.keys():
        print_message("Sorry! No such plane!", True)
        return

    plane_key = elements.pop(0)
    for comm in elements:
        if comm not in allowed_commands:
            print_message(f"'{comm}' is not allowed!")
            return
    
    planes[plane_key].execute_commands(elements)


def print_message(message, error=False):
    """Print a message to the console (in red for errors, in white for confirmations)"""
    sys.stdout.write(AnsiCommands.SAVE_CURSOR)
    sys.stdout.write(getMoveCursorString(0, 22))
    if error:
        sys.stdout.write(Colors.FOREGROUND_RED)
    sys.stdout.write(AnsiCommands.CLEAR_LINE)
    sys.stdout.write(message)
    sys.stdout.write(AnsiCommands.RESTORE_CURSOR)
    sys.stdout.flush()

def main():
    """Entry point for the program"""
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.flush()
    airfield = Airfield(80, 20)
    airfield.initial_print()
    main_loop(airfield, airfield.planes, 0)
    while True:
        command = input("Enter command : ")
        validate_command(command, airfield.planes, allow_list)
        sys.stdout.write(AnsiCommands.CURSOR_UP_ONE_LINE)
        sys.stdout.write(AnsiCommands.CLEAR_LINE)
        sys.stdout.flush()

main()
