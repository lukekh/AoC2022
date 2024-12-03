"""AoC :: Day 22"""
from enum import Enum
from dataclasses import dataclass
import re
import time
from typing import Literal
day = 22



# Parse inputs
with open('Day22/Day22.in', encoding="utf8") as f:
    boardtext, pathtext = f.read().split("\n\n")

# Clean up inputs
boardtext = boardtext.strip("\n")
pathtext = pathtext.strip()

# Separate instructions into list
re_instruction = re.compile(r"\d+|R|L")
PATH = [int(i) if i not in ("R", "L") else i for i in re_instruction.findall(pathtext)]
# Test to see that no instructions were dropped
assert len(pathtext) == len("".join(str(p) for p in PATH)), "Instructions are missing after parsing, check regex catches all possibilities"

# Construct board with warping
LENGTH = 50
class Face(Enum):
    """map faces onto larger grid"""
    A = (1, 0)
    B = (2, 0)
    C = (1, 1)
    D = (1, 2)
    E = (0, 2)
    F = (0, 3)

    @staticmethod
    def determine_face(x: int, y: int):
        """A helper function to determine the face"""
        fx = (x-1)//LENGTH
        fy = (y-1)//LENGTH
        return Face((fx, fy))

    def determine_position(self, rel_x: int, rel_y: int) -> tuple[int, int]:
        """A helper function to determine the face"""
        Dx, Dy = self.value
        return rel_x + 1 + LENGTH * Dx, rel_y + LENGTH * Dy + 1

    def warp(self, x: int, y: int, direction: "Direction"):
        """
        Where do you end up leaving a face
        
        (x, y) is your current position before the warp
        """
        x_face, y_face = [fi + di for fi, di in zip(self.value, direction.value)]

        rel_x, rel_y = ((x-1) % LENGTH, (y-1) % LENGTH)
        match (x_face, y_face):
            # Go left off A
            case (0, 0):
                rel_y = LENGTH - 1 - rel_y
                rel_x = 0
                new_face = Face.E
                new_direction = Direction.RIGHT
                new_x, new_y = new_face.determine_position(rel_x, rel_y)
                return (new_x, new_y), new_direction
            # Go up off A
            case (1, -1):
                rel_y = rel_x
                rel_x = 0
                new_face = Face.F
                new_direction = Direction.RIGHT
                new_x, new_y = new_face.determine_position(rel_x, rel_y)
                return (new_x, new_y), new_direction
            # Go up off B
            case (2, -1):
                # rel_x stays the same
                rel_y = LENGTH - 1
                new_face = Face.F
                new_direction = Direction.UP
                new_x, new_y = new_face.determine_position(rel_x, rel_y)
                return (new_x, new_y), new_direction
            # Go right off B
            case (3, 0):
                rel_y = LENGTH - 1 - rel_y
                rel_x = LENGTH - 1
                new_face = Face.D
                new_direction = Direction.LEFT
                new_x, new_y = new_face.determine_position(rel_x, rel_y)
                return (new_x, new_y), new_direction
            # Go down off B or right off C
            case (2, 1):
                if direction.name == "DOWN":
                    rel_y = rel_x
                    rel_x = LENGTH - 1
                    new_face = Face.C
                    new_direction = Direction.LEFT
                    new_x, new_y = new_face.determine_position(rel_x, rel_y)
                    return (new_x, new_y), new_direction
                elif direction.name == "RIGHT":
                    rel_x = rel_y
                    rel_y = LENGTH - 1
                    new_face = Face.B
                    new_direction = Direction.UP
                    new_x, new_y = new_face.determine_position(rel_x, rel_y)
                    return (new_x, new_y), new_direction
                raise ValueError("Not sure how you got here")
            # Go right off D
            case (2, 2):
                rel_y = LENGTH - 1 - rel_y
                rel_x = LENGTH - 1
                new_face = Face.B
                new_direction = Direction.LEFT
                new_x, new_y = new_face.determine_position(rel_x, rel_y)
                return (new_x, new_y), new_direction
            # Go down off D or right off F
            case (1, 3):
                if direction.name == "DOWN":
                    rel_y = rel_x
                    rel_x = LENGTH - 1
                    new_face = Face.F
                    new_direction = Direction.LEFT
                    new_x, new_y = new_face.determine_position(rel_x, rel_y)
                    return (new_x, new_y), new_direction
                elif direction.name == "RIGHT":
                    rel_x = rel_y
                    rel_y = LENGTH - 1
                    new_face = Face.D
                    new_direction = Direction.UP
                    new_x, new_y = new_face.determine_position(rel_x, rel_y)
                    return (new_x, new_y), new_direction
                raise ValueError("Not sure how you got here")
            # Go down off F
            case (0, 4):
                # rel_x stays the same
                rel_y = 0
                new_face = Face.B
                new_direction = Direction.DOWN
                new_x, new_y = new_face.determine_position(rel_x, rel_y)
                return (new_x, new_y), new_direction
            # Go left off F
            case (-1, 3):
                rel_x = rel_y
                rel_y = 0
                new_face = Face.A
                new_direction = Direction.DOWN
                new_x, new_y = new_face.determine_position(rel_x, rel_y)
                return (new_x, new_y), new_direction
            # Go left off E
            case (-1, 2):
                rel_y = LENGTH - 1 - rel_y
                rel_x = 0
                new_face = Face.A
                new_direction = Direction.RIGHT
                new_x, new_y = new_face.determine_position(rel_x, rel_y)
                return (new_x, new_y), new_direction
            # Go up off E or left off C
            case (0, 1):
                if direction.name == "UP":
                    rel_y = rel_x
                    rel_x = 0
                    new_face = Face.C
                    new_direction = Direction.RIGHT
                    new_x, new_y = new_face.determine_position(rel_x, rel_y)
                    return (new_x, new_y), new_direction
                elif direction.name == "LEFT":
                    rel_x = rel_y
                    rel_y = 0
                    new_face = Face.E
                    new_direction = Direction.DOWN
                    new_x, new_y = new_face.determine_position(rel_x, rel_y)
                    return (new_x, new_y), new_direction

@dataclass
class Tile:
    """A tile on the board including position (x, y) and kind ("." or "#)"""
    x: int
    y: int
    kind: Literal[".", "#"]

    # Introduced in part two
    face: Face

    @property
    def position(self):
        """Return the (x, y) coordinate of the tile"""
        return (self.x, self.y)

class Direction(Enum):
    """The direction you're facing"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def turn(self, instruction: Literal["L", "R"]):
        """Given an instruction, calculate next direction"""
        match self.name:
            case "UP":
                return Direction.LEFT if instruction == "L" else Direction.RIGHT
            case "DOWN":
                return Direction.RIGHT if instruction == "L" else Direction.LEFT
            case "LEFT":
                return Direction.DOWN if instruction == "L" else Direction.UP
            case "RIGHT":
                return Direction.UP if instruction == "L" else Direction.DOWN

    def write(self):
        """Given an instruction, calculate next direction"""
        match self.name:
            case "UP":
                return "^"
            case "DOWN":
                return "v"
            case "LEFT":
                return "<"
            case "RIGHT":
                return ">"

    def password(self):
        """the value of the direction in the password for part one"""
        match self.name:
            case "RIGHT":
                return 0
            case "DOWN":
                return 1
            case "LEFT":
                return 2
            case "UP":
                return 3


@dataclass
class Cursor:
    """Where you currently are on the board"""
    x: int
    y: int
    direction: Direction

class Board:
    """
    A board initialised with a string 2D map input
    """
    def __init__(self, boardtext_: str):
        self.tiles: dict[tuple[int, int], Tile] = {}
        self.rows: dict[int, list[Tile]] = {}
        self.cols: dict[int, list[Tile]] = {}

        for y, row in enumerate(boardtext_.split("\n")):
            new_row = []
            for x, char in enumerate(row):
                if x+1 not in self.cols:
                    self.cols[x+1] = []
                col = self.cols[x+1]
                if char in (".", "#"):
                    tile = Tile(x+1, y+1, char, Face.determine_face(x+1, y+1))
                    self.tiles[(x+1, y+1)] = tile
                    new_row.append(tile)
                    col.append(tile)
            self.rows[y+1] = new_row

        cursor_pos = self.get_row(1)[0].position
        self._origin = cursor_pos
        self.cursor = Cursor(*cursor_pos, Direction.RIGHT)

        self.cube_map = [list(row) for row in boardtext.split("\n")]

    def reset_cursor(self):
        """reset the cursor to its original position"""
        self.cursor = Cursor(*self._origin, Direction.RIGHT)

    def __getitem__(self, pos: tuple[int, int]):
        return self.tiles[pos]

    def get_row(self, y: int):
        """Return all of the tiles with a particular y coordinate"""
        return self.rows[y]

    def get_col(self, x: int):
        """Return all of the tiles with a particular x coordinate"""
        return self.cols[x]

    def move(self, steps: int):
        """take steps in the current direction"""
        match self.cursor.direction.name:
            case "UP":
                self._move_up(steps)
            case "DOWN":
                self._move_down(steps)
            case "LEFT":
                self._move_left(steps)
            case "RIGHT":
                self._move_right(steps)

    def move_cube(self, steps: int):
        """take steps on the cube one at a time"""
        for _ in range(steps):
            tile = self.step()
            if tile.kind == "#":
                break

    def step(self):
        """
        Perform a step given current cursor position and return the tile
        to check whether movement stops
        """
        x, y = self.cursor.x, self.cursor.y
        dx, dy = self.cursor.direction.value
        nx, ny = (x + dx, y + dy)

        # If no warp needs to occur, perform step with simple logic
        if (nx, ny) in self.tiles:
            next_tile = self[nx, ny]
            if next_tile.kind == ".":
                self.cursor.x = nx
                self.cursor.y = ny
                self.cube_map[y-1][x-1] = self.cursor.direction.write()
        # Otherwise warp
        else:
            face = self[x, y].face
            next_position, next_direction = face.warp(x, y, self.cursor.direction)
            next_tile = self[next_position]
            if next_tile.kind == ".":
                self.cursor.x, self.cursor.y  = next_position
                self.cube_map[y-1][x-1] = self.cursor.direction.write()
                self.cursor.direction = next_direction

        return next_tile

    def _move_up(self, steps: int):
        assert self.cursor.direction is Direction.UP, "wrong method being used"
        # Get column of tiles
        col = self.get_col(self.cursor.x)
        N = len(col)
        min_y = col[0].y

        # Figure out cursors y position relative to columns list
        relative_start_y = self.cursor.y - min_y
        assert relative_start_y >= 0, "something is wrong with the relative y position"

        # If there are less steps than the length of the column, we need to check
        # if anything in that line is a wall and stop, else we terminate in that spot
        ahead = col[relative_start_y-1::-1] + col[:relative_start_y-1:-1]
        if steps < N:
            ahead = ahead[:steps]
            new_y = self.cursor.y
            for tile in ahead:
                if tile.kind == "#":
                    break
                new_y = tile.y
            self.cursor.y = new_y
        else:
            new_y = self.cursor.y
            for tile in ahead:
                if tile.kind == "#":
                    break
                new_y = tile.y
            else:
                new_y = min_y + (self.cursor.y - steps % N)
            self.cursor.y = new_y

    def _move_down(self, steps: int):
        assert self.cursor.direction is Direction.DOWN, "wrong method being used"
        # Get column of tiles
        col = self.get_col(self.cursor.x)
        N = len(col)
        min_y = col[0].y

        # Figure out cursors y position relative to columns list
        relative_start_y = self.cursor.y - min_y
        assert relative_start_y >= 0, "something is wrong with the relative y position"

        # If there are less steps than the length of the column, we need to check
        # if anything in that line is a wall and stop, else we terminate in that spot
        ahead = col[relative_start_y+1:] + col[:relative_start_y+1]
        if steps < N:
            ahead = ahead[:steps]
            new_y = self.cursor.y
            for tile in ahead:
                if tile.kind == "#":
                    break
                new_y = tile.y
            self.cursor.y = new_y
        else:
            new_y = self.cursor.y
            for tile in ahead:
                if tile.kind == "#":
                    break
                new_y = tile.y
            else:
                new_y = min_y + (self.cursor.y + steps % N)
            self.cursor.y = new_y

    def _move_left(self, steps: int):
        assert self.cursor.direction is Direction.LEFT, "wrong method being used"
        # Get column of tiles
        row = self.get_row(self.cursor.y)
        N = len(row)
        min_x = row[0].x

        # Figure out cursors x position relative to columns list
        relative_start_x = self.cursor.x - min_x
        assert relative_start_x >= 0, "something is wrong with the relative x position"

        # If there are less steps than the length of the column, we need to check
        # if anything in that line is a wall and stop, else we terminate in that spot
        ahead = row[relative_start_x-1::-1] + row[:relative_start_x-1:-1]
        if steps < N:
            ahead = ahead[:steps]
            new_x = self.cursor.x
            for tile in ahead:
                if tile.kind == "#":
                    break
                new_x = tile.x
            self.cursor.x = new_x
        else:
            new_x = self.cursor.x
            for tile in ahead:
                if tile.kind == "#":
                    break
                new_x = tile.x
            else:
                new_x = min_x + (self.cursor.x - steps % N)
            self.cursor.x = new_x

    def _move_right(self, steps: int):
        assert self.cursor.direction is Direction.RIGHT, "wrong method being used"
        # Get column of tiles
        row = self.get_row(self.cursor.y)
        N = len(row)
        min_x = row[0].x

        # Figure out cursors x position relative to columns list
        relative_start_x = self.cursor.x - min_x
        assert relative_start_x >= 0, "something is wrong with the relative x position"

        # If there are less steps than the length of the column, we need to check
        # if anything in that line is a wall and stop, else we terminate in that spot
        ahead = row[relative_start_x+1:] + row[:relative_start_x+1]
        if steps < N:
            ahead = ahead[:steps]
            new_x = self.cursor.x
            for tile in ahead:
                if tile.kind == "#":
                    break
                new_x = tile.x
            self.cursor.x = new_x
        else:
            new_x = self.cursor.x
            for tile in ahead:
                if tile.kind == "#":
                    break
                new_x = tile.x
            else:
                new_x = min_x + (self.cursor.x + steps % N)
            self.cursor.x = new_x


    def instruct(self, instruction: int | Literal["L", "R"]):
        """process an instruction"""
        match instruction:
            case int():
                self.move(instruction)
            case _:
                self.cursor.direction = self.cursor.direction.turn(instruction)

    def instruct_cube(self, instruction: int | Literal["L", "R"]):
        """process an instruction on the cube"""
        match instruction:
            case int():
                self.move_cube(instruction)
            case _:
                self.cursor.direction = self.cursor.direction.turn(instruction)

    def print_cube(self):
        """Print the path taken by the cursor"""
        cur = self.cube_map[self.cursor.y][self.cursor.x]
        self.cube_map[self.cursor.y][self.cursor.x] = "X"
        print("\n".join(["".join(row) for row in self.cube_map]))
        self.cube_map[self.cursor.y][self.cursor.x] = cur



    def final_password(self):
        """the final password formula defined in part one"""
        return self.cursor.y * 1000 + self.cursor.x * 4 + self.cursor.direction.password()

BOARD = Board(boardtext)

# part one
def part_one(board: Board, path: list[int | str]):
    """Solution to part one"""
    for instruction in path:
        board.instruct(instruction)
    return board.final_password()


# part two
def part_two(board: Board, path: list[int | str]):
    """Solution to part two"""
    for instruction in path:
        board.instruct_cube(instruction)
    return board.final_password()


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(BOARD, PATH)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    BOARD.reset_cursor()
    a2 = part_two(BOARD, PATH)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
