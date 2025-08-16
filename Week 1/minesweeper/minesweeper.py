import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:     
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
   

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        # if cell in self.mines:
        #     self.mines.remove(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_surroundings(self, cell):
        left_x = cell[1] - 1
        right_x = cell[1] + 1
        up_y = cell[0] - 1
        down_y = cell[0] + 1
        left_bound = (cell[1] == 0)
        right_bound = (cell[1] == self.width-1)
        upper_bound = (cell[0] == 0)
        lower_bound = (cell[0] == self.height-1)

        surroundings = []
        if left_bound:
            if upper_bound:
                surroundings.append((down_y, 0))
                surroundings.append((down_y, 1))

            elif lower_bound:
                surroundings.append((up_y, 0))
                surroundings.append((up_y, 1))
            else:
                surroundings.append((up_y, 0))
                surroundings.append((up_y, 1))
                surroundings.append((down_y, 0))
                surroundings.append((down_y, 1))
                
            surroundings.append((cell[0], right_x))

        elif right_bound:
            if upper_bound:
                surroundings.append((down_y, cell[1]))
                surroundings.append((down_y, left_x))
            elif lower_bound:
                surroundings.append((up_y, left_x))
                surroundings.append((up_y, cell[1]))
            else:
                surroundings.append((up_y, left_x))
                surroundings.append((up_y, cell[1]))
                surroundings.append((down_y, left_x))
                surroundings.append((down_y, cell[1]))
                
            surroundings.append((cell[0], left_x))

        elif upper_bound:
            if left_bound:
                surroundings.append((down_y, right_x))
                surroundings.append((cell[0], right_x))
            elif right_bound:
                surroundings.append((down_y, left_x))
                surroundings.append((cell[0], left_x))
            else:
                surroundings.append((down_y, left_x))
                surroundings.append((cell[0], left_x))
                surroundings.append((down_y, right_x))
                surroundings.append((cell[0], right_x))

            surroundings.append((down_y, cell[1]))

        elif lower_bound:
            if left_bound:
                surroundings.append((up_y, right_x))
                surroundings.append((cell[0], right_x))
            elif right_bound:
                surroundings.append((up_y, left_x))
                surroundings.append((cell[0], left_x))
            else:
                surroundings.append((up_y, left_x))
                surroundings.append((cell[0], left_x))
                surroundings.append((up_y, right_x))
                surroundings.append((cell[0], right_x))

            surroundings.append((up_y, cell[1]))

        else:
            surroundings.append((cell[0], left_x))
            surroundings.append((up_y, left_x))
            surroundings.append((down_y, left_x))

            surroundings.append((cell[0], right_x))
            surroundings.append((up_y, right_x))
            surroundings.append((down_y, right_x))

            surroundings.append((up_y, cell[1]))
            surroundings.append((down_y, cell[1]))

        return surroundings

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        sent = Sentence([], count)
        # Check each surrounding cell
        for c in self.get_surroundings(cell):
            if count == 0:
                if c not in self.safes and c not in self.mines:
                    sent.cells.add(c)
                    self.safes.add(c)
            else:
                if c not in self.mines and c not in self.safes:
                    sent.cells.add(c)
                if c in self.mines:
                    sent.count -= 1

        self.knowledge.append(sent)
    
        # Inference Logic 
        # Loop is to ensure that we check every sentence every time the knowledge changed
        knowledge_changed = True
        while knowledge_changed:
            knowledge_changed = False

            remove_empty = []
            safes = set()
            mines = set()
            for sentence in self.knowledge:
                safes = safes.union(sentence.known_safes())
                mines = mines.union(sentence.known_mines())

                if len(sentence.cells) == 0 and sentence.count == 0:
                    remove_empty.append(sentence)

            # Remove empty sentences
            self.knowledge = [x for x in self.knowledge if x not in remove_empty]

            # Mark known safes and mines
            for safe in safes:
                self.mark_safe(safe)
                knowledge_changed = True

            for mine in mines:
                self.mark_mine(mine)
                knowledge_changed = True

            # Combine sentences and add new logic
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 == s2:
                        continue

                    elif s1.cells.issubset(s2.cells):
                        new_sentence = Sentence([], 0)
                        new_sentence.cells = s2.cells - s1.cells
                        new_sentence.count = s2.count - s1.count

                        self.knowledge.append(new_sentence)
                        self.knowledge.remove(s2)
                        knowledge_changed = True
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made:
                return safe_cell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for x in range(self.width):
            for y in range(self.height):
                cell = (y, x)
                if cell not in self.moves_made and cell not in self.mines:
                    return cell

