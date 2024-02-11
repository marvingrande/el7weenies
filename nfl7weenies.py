import sys
import pandas as pd

_NAMES_FILE = "names.txt"
_SQUARES_FILE = "squares.txt"
_FILLER_NAMES = [
    "Shotslana",
    "Beeriana",
    "Winedolyn",
    "Juicyfer",
    "Usher",
    "Taylor",
    "Yash",
    "Kenny G",
    "Trogdor",
    "Gandalf"
]


def main():
    squares = NFL7Weenies()


class NFL7Weenies:

    def __init__(self):
        # prompt for names
        self.names = []
        self.enter_names()
        # generate squares
        self.df_squares = None
        self.make_squares()

    def enter_names(self):
        # check if names list exists, prompt if not
        try:
            with open(_NAMES_FILE) as infile:
                self.names = infile.read().splitlines()
            self.list_names()
            if self.prompt("Use existing names (y/n)?", str, yes_no=True):
                mod_finished = False
            else:
                raise MakeNewFile
            while not mod_finished:
                action = self.prompt("(a)dd new name, (m)odify existing name, (d)elete name, ENTER to finish: ", str)
                if action in ['a']:
                    new_name = self.prompt("Enter new name: ", str)
                    self.names.append(new_name)
                    self.list_names()
                elif action in ['m']:
                    name_index = self.prompt("Modify which name (0-{})?".format(len(self.names)-1), int)
                    new_name = self.prompt("Change name from {} to: ".format(self.names[name_index]), str)
                    self.names.pop(name_index)
                    self.names.insert(name_index, new_name)
                    self.list_names()
                elif action in ['d']:
                    name_index = self.prompt("Delete which name (0-{})?".format(len(self.names)-1), int)
                    self.names.pop(name_index)
                    self.list_names()
                else:
                    mod_finished = True
            self.write_names()
        except MakeNewFile:
            # create list of new names
            self.names = []
            names_finished = False
            while not names_finished:
                new_name = self.prompt("Enter new name (ENTER when finished): ", str)
                if new_name:
                    self.names.append(new_name)
                else:
                    names_finished = True
                self.list_names()
            self.write_names()

    def list_names(self):
        for i, name in enumerate(self.names):
            print("{i}: {n}".format(i=i, n=name))
        print("\n")

    def write_names(self):
        with open(_NAMES_FILE, 'w') as outfile:
            for name in self.names:
                outfile.write("{n}\n".format(n=name))

    def make_squares(self):
        import random
        squares = {}
        possible_xy = []
        columns = [i for i in range(0, 10)]
        index = [i for i in range(0, 10)]
        for x in index:
            for y in columns:
                possible_xy.append((x, y))
        num_squares = len(possible_xy)
        empty_grid = {}
        for col in columns:
            empty_grid[col] = [''] * len(index)
        self.df_squares = pd.DataFrame(empty_grid)
        while num_squares % len(self.names):
            name_add = _FILLER_NAMES.pop(random.randrange(0, len(_FILLER_NAMES)))
            self.names.append(name_add)
        # randomly assign possible x, y for each player
        squares_per_player = num_squares / len(self.names)
        print("Generating {} squares for each player".format(squares_per_player))
        random.shuffle(self.names)
        for name in self.names:
            squares[name] = []
        while len(possible_xy) > 0:
            for player, square_list in squares.items():
                rand_index = random.randrange(0, len(possible_xy))
                squares[player].append(possible_xy.pop(rand_index))
        # convert to grid
        #print(squares)
        for player, square_list in squares.items():
            for (x, y)  in square_list:
                self.df_squares.at[x, y] = player
        print(self.df_squares)

    @staticmethod
    def prompt(query, ret_type, yes_no=False):
        import re
        valid_response = False
        response = None
        hinted_options = re.findall("\((\w)\)", query)
        while not valid_response:
            response = input(query)
            try:
                response = ret_type(response)
                if yes_no:
                    response = response.lower()
                    assert response in ['y', 'n']
                    response = True if response in ['y'] else False
                if hinted_options and response:
                    assert response in hinted_options
            except (AssertionError, TypeError, ValueError):
                print("Invalid input, weenie, try again")
            else:
                valid_response = True
        return response

class MakeNewFile(Exception):
    pass



if __name__ == "__main__":
    main()
    sys.exit()