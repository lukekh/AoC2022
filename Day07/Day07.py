# AoC :: Day 7
import time
day = 7


# Parse inputs
inputs = [i[:-1].split(' ') if i[:2] == 'cd' else i[:-1].split('\n') for i in open('Day07.in').read().split('$ ')][1:]


# utils
class Folder:
    def __init__(self, name:str, parent:'Folder'=None, root=False):
        self.name = name
        self.parent = parent
        if root:
            self.root = self
        else:
            self.root = parent.root
        
        self.folders = {}
        self.files = {}

    def __contains__(self, other:str):
        return (other in self.folders) or (other in self.files)
    
    def add_dir(self, dir:str):
        if dir in self:
            raise Exception("This directory already exists")
        else:
            self.folders[dir] = Folder(dir, self)
    
    def add_file(self, name:str, size:int):
        self.files[name] = size

    def size(self) -> int:
        return sum(self.files.values()) + sum([child.size() for child in self.folders.values()])
    
    def cd(self, arg:str) -> 'Folder':
        if arg == '.':
            return self
        if arg == '..':
            if self.parent is None:
                raise Exception(f"there is no parent to folder {self.name}")
            else:
                return self.parent
        if arg == self.root.name:
            return self.root
        else:
            try:
                return self.folders[arg]
            except KeyError:
                raise Exception(f"cannot cd into {arg} from folder {self.name}")
    
    def __getitem__(self, item:str):
        return self.cd(item)

    def ls(self, *args):
        for arg in args:
            val, name = arg.split(' ')
            if val == 'dir':
                self.add_dir(name)
            else:
                # Assume val must be an integer and a file
                val = int(val)
                self.add_file(name, val)
    
    def execute(self, cmd, *args) -> 'Folder':
        if cmd == "cd":
            return self.cd(args[0])
        elif cmd == "ls":
            self.ls(*args)
            return self
        else:
            raise Exception(f"unknown command '{cmd}' with args {args} sent to folder {self.name}")
    
    def __str__(self) -> str:
        return f'Folder[folders=({", ".join(self.folders.keys())}), files=({", ".join(self.files.keys())})]'

    def path(self, only=True) -> str:
        if self.parent is None:
            return self.name if only else ""
        else:
            return f"{self.parent.path(only=False)}/{self.name}"

    def pretty_string(self, prefix="") -> str:
        next_prefix = prefix + "  |"
        s = f"{prefix[:-1]}|--{self.name}\n"
        for file in self.files.keys():
            s += f"{prefix}  |- *{file}\n"
        for i, folder in enumerate(self.folders.values()):
            if i == len(self.folders) - 1:
                next_prefix = prefix + "   "
            s += folder.pretty_string(prefix=next_prefix)
        
        return s

    def pretty_print(self):
        print(self.pretty_string())

    def part_one(self, max_size=100_000):
        size = self.size()
        total = size if size <= max_size else 0
        for folder in self.folders.values():
            total += folder.part_one(max_size)
        return total
    
    def part_two(self, space_required, candidate_dirs=None):
        if candidate_dirs is None:
            candidate_dirs = {}
        
        size = 0
        abort_branch = False

        for folder in self.folders.values():
            big_enough, n, candidate_dirs = folder.part_two(space_required, candidate_dirs=candidate_dirs)
            if big_enough:
                abort_branch = True
                m = n
            size += n
        
        if abort_branch:
            return True, m, candidate_dirs
        
        size += sum(self.files.values())

        if size >= space_required:
            candidate_dirs[self.path()] = size
            return True, size, candidate_dirs
        else:
            return False, size, candidate_dirs
            

def parse(inputs):
    # init
    root_folder = Folder("/", parent=None, root=True)
    folder = root_folder

    for cmd, *args in inputs:
        folder = folder.execute(cmd, *args)
        
    return root_folder


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    root_folder = parse(inputs)
    print(f"The sum of the total sizes is {root_folder.part_one():,}")
    t1 += time.time()
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    root_size = root_folder.size()
    space_required = 30000000 - (70000000 - root_size)
    _, _, candidate_dirs = root_folder.part_two(space_required)
    min_dir = min(candidate_dirs, key=candidate_dirs.get)
    print(f"The smallest directory to delete is {min(candidate_dirs, key=candidate_dirs.get)} which has size {candidate_dirs[min_dir]:,}")
    t2 += time.time()
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
