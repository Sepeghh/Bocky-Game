"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the player class hierarchy.
"""

import random
from typing import Optional
import pygame
from renderer import Renderer, BOARD_WIDTH
from block import Block
from goal import Goal

TIME_DELAY = 600


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    renderer:
        The object that draws our Blocky board on the screen
        and tracks user interactions with the Blocky board.
    id:
        This player's number.  Used by the renderer to refer to the player,
        for example as "Player 2"
    goal:
        This player's assigned goal for the game.
    """
    renderer: Renderer
    id: int
    goal: Goal

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.renderer = renderer
        self.id = player_id

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """A human player.

    A HumanPlayer can do a limited number of smashes.

    === Public Attributes ===
    num_smashes:
        number of smashes which this HumanPlayer has performed
    === Representation Invariants ===
    num_smashes >= 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the user has most recently selected for action;
    #     changes upon movement of the cursor and use of arrow keys
    #     to select desired level.
    # _level:
    #     The level of the Block that the user selected
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0

    # The total number of 'smash' moves a HumanPlayer can make during a game.
    MAX_SMASHES = 1

    num_smashes: int
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self.num_smashes = 0

        # This HumanPlayer has done no smashes yet.
        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._selected_block = None

    def process_event(self, board: Block,
                      event: pygame.event.Event) -> Optional[int]:
        """Process the given pygame <event>.

        Identify the selected block and mark it as highlighted.  Then identify
        what it is that <event> indicates needs to happen to <board>
        and do it.

        Return
           - None if <event> was not a board-changing move (that is, if was
             a change in cursor position, or a change in _level made via
            the arrow keys),
           - 1 if <event> was a successful move, and
           - 0 if <event> was an unsuccessful move (for example in the case of
             trying to smash in an invalid location or when the player is not
             allowed further smashes).
        """
        # Get the new "selected" block from the position of the cursor
        block = board.get_selected_block(pygame.mouse.get_pos(), self._level)

        # Remove the highlighting from the old "_selected_block"
        # before highlighting the new one
        if self._selected_block is not None:
            self._selected_block.highlighted = False
        self._selected_block = block
        self._selected_block.highlighted = True

        # Since get_selected_block may have not returned the block at
        # the requested level (due to the level being too low in the tree),
        # set the _level attribute to reflect the level of the block which
        # was actually returned.
        self._level = block.level

        if event.type == pygame.MOUSEBUTTONDOWN:
            block.rotate(event.button)
            return 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if block.parent is not None:
                    self._level -= 1
                return None

            elif event.key == pygame.K_DOWN:
                if len(block.children) != 0:
                    self._level += 1
                return None

            elif event.key == pygame.K_h:
                block.swap(0)
                return 1

            elif event.key == pygame.K_v:
                block.swap(1)
                return 1

            elif event.key == pygame.K_s:
                if self.num_smashes >= self.MAX_SMASHES:
                    print('Can\'t smash again!')
                    return 0
                if block.smash():
                    self.num_smashes += 1
                    return 1
                else:
                    print('Tried to smash at an invalid depth!')
                    return 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.
        """
        self._level = 0
        self._selected_block = board

        # Remove all previous events from the queue in case the other players
        # have added events to the queue accidentally.
        pygame.event.clear()

        # Keep checking the moves performed by the player until a valid move
        # has been completed. Draw the board on every loop to draw the
        # selected block properly on screen.
        while True:
            self.renderer.draw(board, self.id)
            # loop through all of the events within the event queue
            # (all pending events from the user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1

                result = self.process_event(board, event)
                self.renderer.draw(board, self.id)
                if result is not None and result > 0:
                    # un-highlight the selected block
                    self._selected_block.highlighted = False
                    self.renderer.draw(board, self.id)
                    return 0


class RandomPlayer(Player):
    """ A Random player

    which choose a random block and do a random action (smash, swap or rotate)
    with it.

    It has a unlimited number of smash moves, but it its smash move is invalid
    it will use its turn
    """

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this RandomPlayer with the given <renderer>, <player_id>
                and <goal>. by calling its superclass __init__"""

        super().__init__(renderer, player_id, goal)

    def make_move(self, board: Block) -> int:

        """Produce a random move that RandomPlayer will chooose by calling
         the random_method on the random block that will be generated by
         producing random location and random level( <= board.max_depth )
         on the given <board>.

         Return 0 upon successful completion of a move. And since random player
         can't Quit therefore it won't return 1 in any case.

         """
        x = random.randint(0, BOARD_WIDTH)
        y = random.randint(0, BOARD_WIDTH)
        # producing random location (x, y) which is inside the area of the board

        random_level = random.randint(0, board.max_depth)
        # producing random level ( <= board.max_depth )
        block = board.get_selected_block((x, y), random_level)
        # choose a block on the board base on the identities that we randomly
        # generate

        block.highlighted = True
        # select the generated block

        self.renderer.draw(board, self.id)
        # to draw the frame around the selected block with HIGHLIGHT_COLOUR

        pygame.time.wait(TIME_DELAY)
        # to introduce a delay so that the user can see what is happening.

        random_move(random.randint(0, 4), block)
        # random.randint will produce a number from {0, 1, 2, 3, 4} which
        # tell the functiom (random_move) what to do to the block

        block.highlighted = False
        # unselect the block

        self.renderer.draw(board, self.id)
        # to draw the change that happens because of our random_move

        return 0


class SmartPlayer(Player):
    """ A Smart player

    which choose number of random moves base on its given difficulty and will do
    the one which will gain the most score among them for the player.

    === Public Attributes ===
    moves_to_check:
        number of moves which this SmartPlayer will check and do the most
        valuable one ( the one which will gain biggest score among the others )
    === Representation Invariants ===
    0 <= moves_to_check <= 150

    SmartPlayer can't do the smash move.

    """
    moves_to_check: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal,
                 difficulty: int) -> None:
        """
        Initialize this SmartPlayer with the given < renderer >,
        < player_id > and < goal >. by calling it's superclass initializer.

        And also set the move_to_check attribute of it base on the given
        <difficulty> . Base on this shcheme:

        difficulty = 0 --> need to check and compare 5 moves
        difficulty = 1 --> need to check and compare 10 moves
        difficulty = 2 --> need to check and compare 25 moves
        difficulty = 3 --> need to check and compare 50 moves
        difficulty = 4 --> need to check and compare 100 moves
        difficulty >= 5 --> need to check and compare 150 moves

        """
        super().__init__(renderer, player_id, goal)

        if difficulty == 0:
            self.moves_to_check = 5
        elif difficulty == 1:
            self.moves_to_check = 10
        elif difficulty == 2:
            self.moves_to_check = 25
        elif difficulty == 3:
            self.moves_to_check = 50
        elif difficulty == 4:
            self.moves_to_check = 100
        else:
            # difficulty >= 5
            self.moves_to_check = 150

    def make_move(self, board: Block):
        """Produce random moves (moves_to_check) times and make those moves
         on the <board> to calculate their score and then undo them. Then store
         the identities that lead us to the maximum score among other moves that
         we have produced. And do that move to gain the biggest possible score
         among the other moves that we have generated.

         Each random move will be produced by calling the _move method on the
         random block that will be generated by producing random location and
         random level( <= board.max_depth ) on the given <board>.

         Return 0 upon successful completion of a move. And since random player
         can't Quit therefore it won't return 1 in any case.

         """

        max_score = 0
        # minimum score is 0.

        best_move = 0
        # it will save the number( that later in _move function determine the
        # action) of the best move ( to generate on the block )

        best_block: Block
        # the identity that will help us to store the block on the board which
        # will lead us through our goal

        for _ in range(self.moves_to_check):

            x = random.randint(0, BOARD_WIDTH)
            y = random.randint(0, BOARD_WIDTH)
            # producing random location (x, y)
            # which is inside the area of the board

            random_level = random.randint(0, board.max_depth)
            # producing random level ( <= board.max_depth )

            block = board.get_selected_block((x, y), random_level)
            # choose a block on the board base on the identities that we
            # randomly generated

            decider = random.randint(0, 3)
            # it is the number between 0 and 3 which base on it's value, our
            # _move function will do the action on the block. it doesn't contain
            # 4 because base on the implementiation of the function random_move
            # 4 will do the smash however Smartplayer can't smash any block

            random_move(decider, block)
            # to the generated action on the generated block
            if max_score < self.goal.score(board):
                # check if the score that has been generated from the move that
                # that we made is greater than the existing max_score, then
                # save the identities of the move.
                best_move = decider
                best_block = block
                max_score = self.goal.score(board)

            undo_move(block, decider)
            # undo the move that we have (done and calculated its score)

        block = best_block
        # chooose the stored block as the best_block to lead us to the highest
        # possible score among the other moves that we haved check

        block.highlighted = True
        # select the block

        self.renderer.draw(board, self.id)
        # to draw the frame around the selected block with HIGHLIGHT_COLOUR

        pygame.time.wait(TIME_DELAY)
        # to introduce a delay so that the user can see what is happening.

        random_move(best_move, block)
        # move the selected block with the best action to gain more score

        block.highlighted = False
        # unselect the block

        self.renderer.draw(board, self.id)
        # to draw the change that happens because of our random_move

        return 0


def random_move(decider: int, block: Block) -> None:
    """It generate the action on the given <block> base on the value of
    the <decider>

    decider == 0 -> clockwise rotate
    decider == 1 -> counterclockwise rotate
    decider == 2 -> horizontally swap
    decider == 3 -> vertically swap
    decider == 4 -> SMASH!

    Precondition : 0 <= decider <= 4

    However since as a precondition we knoe that 0 <= decider <= 4
    so if decider is not 0 or 1 or 2 or 3, it will be 4.
    """
    if decider == 0:
        block.rotate(1)
        # clockwise rotate
        return
    elif decider == 1:
        block.rotate(3)
        # counterclockwise rotate
        return
    elif decider == 2:
        block.swap(0)
        # horizontally swap
        return
    elif decider == 3:
        block.swap(1)
        # vertically swap
        return
    else:
        # therefor decider = 4
        # Smash
        if block.smash():
            # print(f"Random player smash on level {block.level}")
            # it means that the smash move is valid
            return
        else:
            # print(f"Random player chose wrong smash move")
            # it means that the smash move is invlid however by return,
            # the player will loose its turn

            return


def undo_move(block: Block, pervious: int):
    """It undo the action(move) that has been taken before it.

    we insert the number that we had put inside the random_move to generate the
    action as <pervious> inside this function to call the random_move in the way
     to neutral the action that had happened on <block> when we call random_move
     by <pervious>

    pervious == 0 -> pervious move :clockwise rotate
                                    -> counterclockwise rotate to undo that

    pervious == 1 -> pervious move :counterclockwise rotate
                                    -> clockwise rotate to undo that

    pervious == 2 -> pervious move :horizontally swap
                                    -> horizontally swap to undo that

    pervious == 3 -> pervious move :vertically swap
                                    -> vertically swap to undo that
    precondition: 0 <= pervious <= 3

    because we know that ( at least till now ) we only use this function for
    SmartPlayer and SmartPlayer can't do the smash move, therefore(base on
    random_move docstring)) pervious won't be 4

    The reason I implement this function as the seperate function is maybe later
    we can add undo for Humanplayer as well.
     """
    if pervious == 0:
        random_move(1, block)
        # it will do the counterclockwise rotate
        return
    elif pervious == 1:
        random_move(0, block)
        # it will do the clockwise rotate
        return
    elif pervious == 2:
        random_move(2, block)
        # it will do the horizontally swap
        return
    elif pervious == 3:
        random_move(3, block)
        # it weill do the vertically swap
        return


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer',
            'pygame'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
