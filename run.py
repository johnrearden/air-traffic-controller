import threading
import sys
import string
import random
from constants import UniChars, AnsiCommands, Direction, Colors, EntryPoints
from utilities import getMoveCursorString

allow_list = ["n", "north", "e", "east", "s", "south", "w", "west",
              "circle", "c", "land", "l", "5000", "4000", "3000", "2000", "1000"]
runway = {"start": (14, 10), "end": (25, 10)}
AIRFIELD_WIDTH = 80
AIRFIELD_HEIGHT = 20

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
        start = runway["start"][0] + width * (runway["end"][1] - 1)
        end = runway["end"][0] + width * (runway["end"][1] - 1) + 1
        list_1 = list(range(start, end))
        runway_string = "---RUNWAY---"
        for ind, char in zip(list_1, runway_string):
            self.cells[ind - width] = UniChars.HORIZONTAL_LINE
            self.cells[ind] = char
            self.cells[ind + width] = UniChars.HORIZONTAL_LINE
        runway_arrow_index = runway["end"][0] + 4 + (runway["end"][1] - 1) * width
        self.cells[runway_arrow_index] = UniChars.LEFT_ARROW
        self.cells[runway_arrow_index + 4] = UniChars.LEFT_ARROW
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
        self.landing = False

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

        # If the plane has landed, flag it as eliminated
        if self.landing and self.x_pos <= runway["start"][0]:
            self.eliminated = True

        # Print the plane to the display, as long as it has not just been eliminated
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
                elif abbreviation == "l":
                    self.attempt_landing()

    def change_altitude(self, new_alt):
        """Sets a new altitude target for this plane and begins to adjust the 
           current altitude incrementally"""
        self.altitude = int(new_alt)
        print_message(f"Plane {self.identity}: altitude set to {new_alt}")

    def change_direction(self, new_dir):
        """Sets a new direction target for this plane and begins to adjust the 
           current altitude incrementally"""
        self.direction = Direction.get_direction(new_dir)
        print_message(f"Plane {self.identity}: heading set to {new_dir}")

    def attempt_landing(self):
        """Checks to see if landing conditions are met, and if so, lands the plane"""
        altitude_ok = self.altitude == 1000
        end = runway["end"][1]
        y_pos_ok = self.y_pos == end
        x_pos_ok = self.x_pos > runway["end"][0]
        print_message(f"{self.y_pos},{end}")
        if altitude_ok and y_pos_ok and x_pos_ok:
            self.landing = True
            print_message(f"Plane {self.identity} cleared for landing")

    def print(self):
        """Prints this plane to the display"""
        sys.stdout.write(AnsiCommands.SAVE_CURSOR)
        sys.stdout.write(getMoveCursorString(self.x_pos, self.y_pos))
        sys.stdout.write(self.color.value)
        sys.stdout.write(f"{self.direction.get_character()}")
        sys.stdout.write(AnsiCommands.NORMAL)
        sys.stdout.write(AnsiCommands.RESTORE_CURSOR)
        sys.stdout.flush()

    def print_info(self):
        """Prints this plane's identity and altitude to the display"""
        sys.stdout.write(AnsiCommands.SAVE_CURSOR)
        if self.x_pos < AIRFIELD_WIDTH - 2:
            sys.stdout.write(getMoveCursorString(self.x_pos + 2, self.y_pos))
            sys.stdout.write(f"{self.color.value}")
            sys.stdout.write(f"{AnsiCommands.FAINT}{self.identity}")
        sys.stdout.write(getMoveCursorString(self.x_pos - 1, self.y_pos + 1))
        if self.y_pos < AIRFIELD_HEIGHT - 1:
            sys.stdout.write(AnsiCommands.BLINK)
            alt =  "land" if self.landing else str(self.altitude)
            sys.stdout.write(str(alt))
        sys.stdout.write(AnsiCommands.NORMAL)
        sys.stdout.write(AnsiCommands.RESTORE_CURSOR)
        sys.stdout.flush()

def main_loop(airfield, planes, counter):
    """The main game loop"""
    airfield.print(planes)
    rand = random.randint(1, 100)
    should_add_plane = (len(planes) < 5 and rand < 30) or len(planes) == 0
    if should_add_plane:
        next_identifier = airfield.plane_names.pop(0)
        plane = Plane(next_identifier)
        planes[next_identifier] = plane
        airfield.plane_names.append(next_identifier)
    for plane in planes.values():
        plane.update()
    for plane in planes.values():
        if not plane.eliminated:
            plane.print_info()
    airfield.planes = {key:plane for (key, plane) in planes.items() if plane.eliminated is False}
    timer = threading.Timer(2.5, main_loop, [airfield, airfield.planes, counter + 1])
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

def print_intro():
    """Print welcome message and instructions to display"""
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.flush()
    print(f"{Colors.FOREGROUND_GREEN}WELCOME TO AIR TRAFFIC CONTROLLER!\n{AnsiCommands.DEFAULT_COLOR}")
    print("You run a coffee stall in the airport. Zombie invaders have taken over the")
    print("control tower and there is nobody left to run the computers! You have found")
    print("an old terminal under the counter in your stall that by a lucky accident is")
    print("still connected to the air traffic control system!")
    print()
    print("Unfortunately the controls are a bit rudimentary :(")
    print()
    print("You must use the command line to give the planes their orders.")
    print()
    print("First enter the letter assigned to the plane you want to give an order to.")
    print("Then, after a space, you can enter one of the following directions:")
    print("(w)est, (e)ast, (n)orth, (s)outh")
    print(f"Example : {Colors.FOREGROUND_ORANGE}'a west'{AnsiCommands.DEFAULT_COLOR} or {Colors.FOREGROUND_ORANGE}'a w'")
    print(f"{AnsiCommands.DEFAULT_COLOR}")
    print("To change a plane's altitude, enter its letter, a space, and then the new")
    print(f"altitude in multiples of 1000 ... e.g. {Colors.FOREGROUND_ORANGE}'a 3000'{AnsiCommands.DEFAULT_COLOR}")
    print()
    print("Once the plane is heading for the runway, at an altitude of 1000, you can")
    print(f"order it to land like this - {Colors.FOREGROUND_ORANGE}'a land'{AnsiCommands.DEFAULT_COLOR}")
    print()
    while True:
        command = input("Enter (s)tart when ready... : ")
        if command == "s" or command == "start":
            print(AnsiCommands.TERMINAL_BELL)
            break

def main():
    """Entry point for the program"""
    print_intro()
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.flush()
    airfield = Airfield(AIRFIELD_WIDTH, AIRFIELD_HEIGHT)
    airfield.initial_print()
    main_loop(airfield, airfield.planes, 0)
    while True:
        command = input("Enter command : ")
        validate_command(command, airfield.planes, allow_list)
        sys.stdout.write(AnsiCommands.CURSOR_UP_ONE_LINE)
        sys.stdout.write(AnsiCommands.CLEAR_LINE)
        sys.stdout.flush()

main()
