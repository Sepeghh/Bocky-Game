"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block
from renderer import colour_name


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def score(self, board: Block) -> int:
        """Return the current score of the player whose goal is BlobGoal on the
        given board.

        The score is always greater than or equal to 0.
        """
        platform = board.flatten()
        # with this we create a list[list[colour(in the tuple format)]] of the
        # board game that make our life easier to calculate the score
        visited = []
        # it's the two dimention list which shows the elements that we have
        # checked from the platform
        # it has this properties:
        # -1 if the cell has not been visited yet
        # 0 if it has been visited, and it is not of the target colour
        # 1 if it has been visited and is of the target colour

        dimention = 2 ** board.max_depth
        # the length of the platfrom ( and also every list inside the platform))
        # the length of visited ( and also every list inside the visited ))

        for i in range(dimention):
            column = []
            for j in range(dimention):
                column.append(-1)
                # first we make all of the elements inside -1 because we haven't
                #  check any cells yet
            visited.append(column)

        score = 0
        # define it so we can compare it later and we knowthe minimum score is 0
        for i in range(dimention):
            for j in range(dimention):
                # use the nested for to check every each element inside the
                # platform( which is basically the colour)

                unit_score = self._undiscovered_blob_size((i, j), platform,
                                                          visited)
                # the score that will drive from this cell
                if score < unit_score:
                    score = unit_score
                    # store the highest score in the board ( biggest bulb )
        return score

    def description(self) -> str:
        """Return a description of the BlobGoal.
        """
        return f"Make the bigges bulb of {colour_name(self.colour)}"

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        if (pos[0] < 0) or (pos[1] < 0) or (pos[0] > len(board) - 1) or \
                (pos[1] > len(board[0]) - 1):
            # it means the pos is out of bounds for board
            return 0
        elif visited[pos[0]][pos[1]] == -1:
            # if we haven't visited this cell before
            if board[pos[0]][pos[1]] == self.colour:
                visited[pos[0]][pos[1]] = 1
                # it means cell has been visited and discovered to be of the
                # target colour
                return \
                    (
                        self._undiscovered_blob_size((pos[0] + 1, pos[1]),
                                                     board,
                                                     visited) +
                        self._undiscovered_blob_size((pos[0] - 1, pos[1]),
                                                     board,
                                                     visited) +
                        self._undiscovered_blob_size((pos[0], pos[1] + 1),
                                                     board,
                                                     visited) +
                        self._undiscovered_blob_size((pos[0], pos[1] - 1),
                                                     board,
                                                     visited) + 1)
                # return the sccre(bulb size) of the its neighbours plus 1
                # which that 1 has came from itself
            else:
                visited[pos[0]][pos[1]] = 0
                # so this cell doesn't have the target colour so make it 0
                return 0
        else:
            return 0


class PerimeterGoal(Goal):
    """A goal is to put the most possible units of a given colour on the outer
    perimeter of the board"""

    def score(self, board: Block) -> int:
        """Return the current score of the player whose goal is PerimeterGoal
        on the fiven board

        The score is always greater than or equal to 0.
        """
        platform = board.flatten()
        # with this we create a list[list[colour(in the tuple format)]] of the
        # board game that make our life easier to calculate the score
        score = 0
        # the Minimum score is Zero.
        dimention = 2 ** board.max_depth
        # the length of the platform ( and also every list inside the platform))
        for i in range(dimention):
            if platform[i][0] == self.colour:
                score += 1
            # checking the first row
            if platform[0][i] == self.colour:
                score += 1
            # checking the first column
            if platform[dimention - 1][i] == self.colour:
                score += 1
            # checking the last column
            # dimention - 1 because we knoe index starts from 0 to x-1
            if platform[i][dimention - 1] == self.colour:
                score += 1
            # checking the last row
            # dimention - 1 because we knoe index starts from 0 to x-1

        return score
        # as we can see we have already count the corners twice(for example:
        # once when we was checking the last row, and once when we was checking
        # the first column)

    def description(self) -> str:
        """Return a description of the PerimeterGoal.
        """
        return f"Put the most possible units of {colour_name(self.colour)}" \
               f"on the outer perimeter of the board."


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
