"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Block class, the main data structure used in the game.
"""
from typing import Optional, Tuple, List
import random
import math
from renderer import COLOUR_LIST, TEMPTING_TURQUOISE, BLACK, colour_name

HIGHLIGHT_COLOUR = TEMPTING_TURQUOISE
FRAME_COLOUR = BLACK


class Block:
    """A square block in the Blocky game.

    === Public Attributes ===
    position:
        The (x, y) coordinates of the upper left corner of this Block.
        Note that (0, 0) is the top left corner of the window.
    size:
        The height and width of this Block.  Since all blocks are square,
        we needn't represent height and width separately.
    colour:
        If this block is not subdivided, <colour> stores its colour.
        Otherwise, <colour> is None and this block's sublocks store their
        individual colours.
    level:
        The level of this block within the overall block structure.
        The outermost block, corresponding to the root of the tree,
        is at level zero.  If a block is at level i, its children are at
        level i+1.
    max_depth:
        The deepest level allowed in the overall block structure.
    highlighted:
        True iff the user has selected this block for action.
    children:
        The blocks into which this block is subdivided.  The children are
        stored in this order: upper-right child, upper-left child,
        lower-left child, lower-right child.
    parent:
        The block that this block is directly within.

    === Representation Invariations ===
    - len(children) == 0 or len(children) == 4
    - If this Block has children,
        - their max_depth is the same as that of this Block,
        - their size is half that of this Block,
        - their level is one greater than that of this Block,
        - their position is determined by the position and size of this Block,
          as defined in the Assignment 2 handout, and
        - this Block's colour is None
    - If this Block has no children,
        - its colour is not None
    - level <= max_depth
    """
    position: Tuple[int, int]
    size: int
    colour: Optional[Tuple[int, int, int]]
    level: int
    max_depth: int
    highlighted: bool
    children: List['Block']
    parent: Optional['Block']

    def __init__(self, level: int,
                 colour: Optional[Tuple[int, int, int]] = None,
                 children: Optional[List['Block']] = None) -> None:
        """Initialize this Block to be an unhighlighted root block with
        no parent.

        If <children> is None, give this block no children.  Otherwise
        give it the provided children.  Use the provided level and colour,
        and set everything else (x and y coordinates, size,
        and max_depth) to 0.  (All attributes can be updated later, as
        appropriate.)
        """
        self.position = (0, 0)
        self.size = 0
        if children is None:
            # if block doesn't have any child, then it has colour
            self.colour = colour
            self.children = []
        else:
            # if the block has children, then it doesn't have colour
            self.colour = None
            self.children = children
        self.level = level
        self.max_depth = 0
        self.highlighted = False
        self.parent = None

    def rectangles_to_draw(self) -> List[Tuple[Tuple[int, int, int],
                                               Tuple[int, int],
                                               Tuple[int, int],
                                               int]]:
        """
        Return a list of tuples describing all of the rectangles to be drawn
        in order to render this Block.

        This includes (1) for every undivided Block:
            - one rectangle in the Block's colour
            - one rectangle in the FRAME_COLOUR to frame it at the same
              dimensions, but with a specified thickness of 3
        and (2) one additional rectangle to frame this Block in the
        HIGHLIGHT_COLOUR at a thickness of 5 if this block has been
        selected for action, that is, if its highlighted attribute is True.

        The rectangles are in the format required by method Renderer.draw.
        Each tuple contains:
        - the colour of the rectangle
        - the (x, y) coordinates of the top left corner of the rectangle
        - the (height, width) of the rectangle, which for our Blocky game
          will always be the same
        - an int indicating how to render this rectangle. If 0 is specified
          the rectangle will be filled with its colour. If > 0 is specified,
          the rectangle will not be filled, but instead will be outlined in
          the FRAME_COLOUR, and the value will determine the thickness of
          the outline.

        The order of the rectangles does not matter.
        """
        size = (self.size, self.size)  # just to avoid writing this tuple
        lst = []
        if self.highlighted is True:
            # if it's highlighted, there will be a frame around it
            lst.extend([(HIGHLIGHT_COLOUR, self.position, size, 5)])
        if len(self.children) == 0:
            lst.extend([(self.colour, self.position, size, 0)])
            # if it doesn't have any child, there should be a rectangle
            # filled with it's colour
            lst.extend([(FRAME_COLOUR, self.position, size, 3)])
            # there should be frame around it with frame_colour
            return lst
        else:
            for block in self.children:
                lst.extend(block.rectangles_to_draw())
                # if it has children, call the method on each child
            return lst

    def swap(self, direction: int) -> None:
        """Swap the child Blocks of this Block.

        If <direction> is 1, swap vertically.  If <direction> is 0, swap
        horizontally. If this Block has no children, do nothing.
        """
        if len(self.children) == 0:
            # if the block doesn't have any child, therefore swaping won't do
            # any thing
            pass
        elif direction == 0:
            # swapping horizontally :
            # 1 -> 0
            # 0 -> 1
            # 2 -> 3
            # 3 -> 2
            self.children[0], self.children[1] = (self.children[1],
                                                  self.children[0])

            self.children[2], self.children[3] = (self.children[3],
                                                  self.children[2])

        elif direction == 1:
            # swapping vertically :
            # 0 -> 3
            # 3 -> 0
            # 1 -> 2
            # 2 -> 1
            self.children[0], self.children[3] = (self.children[3],
                                                  self.children[0])
            self.children[1], self.children[2] = (self.children[2],
                                                  self.children[1])

        self.update_block_locations(self.position, self.size)
        # Update the position and size of each of the Blocks within this Block.

    def rotate(self, direction: int) -> None:
        """Rotate this Block and all its descendants.

        If <direction> is 1, rotate clockwise.  If <direction> is 3, rotate
        counterclockwise. If this Block has no children, do nothing.
        """
        if len(self.children) == 0:
            # if it doens't have any child, then rotating it won't change
            # anything
            pass

        elif direction == 1:
            # rotaing clocwise:
            # 0 -> 3
            # 3 -> 2
            # 2 -> 1
            # 1 -> 0
            (self.children[3],
             self.children[2],
             self.children[1],
             self.children[0]) = (

                 self.children[0],
                 self.children[3],
                 self.children[2],
                 self.children[1])

            for block in self.children:
                # rotating all of it's descendants with recursive call on its
                # children with same direction
                block.rotate(1)

        elif direction == 3:
            # rotaing counterclocwise:
            # 2 -> 3
            # 1 -> 2
            # 0 -> 1
            # 3 -> 0
            (self.children[3],
             self.children[2],
             self.children[1],
             self.children[0]) = (

                 self.children[2],
                 self.children[1],
                 self.children[0],
                 self.children[3])

            for block in self.children:
                # rotating all of it's descendants with recursive call on its
                # children with same direction
                block.rotate(3)

        self.update_block_locations(self.position, self.size)
        # Update the position and size of each of the Blocks within this Block.

    def smash(self) -> bool:
        """Smash this block.

        If this Block can be smashed,
        randomly generating four new child Blocks for it.  (If it already
        had child Blocks, discard them.)
        Ensure that the RI's of the Blocks remain satisfied.

        A Block can be smashed iff it is not the top-level Block and it
        is not already at the level of the maximum depth.

        Return True if this Block was smashed and False otherwise.
        """
        if (self.level == self.max_depth) or (self.level == 0):
            # if the block is the unit cell it can't be smashed
            # if it's mother block (level = 0) it can't be smashed because it
            # will change the entire game
            return False

        elif len(self.children) != 0:
            # if it has children discard them first
            self.children.clear()

        for _ in range(4):
            # creating 4 new block with the level: self.level + 1 to add it to
            # the children of the block that we are smashing
            # (creating 4 new block as children for the block that we're
            # smashing)
            new_block = random_init(self.level + 1, self.max_depth)
            new_block.parent = self
            self.children.append(new_block)

        self.update_block_locations(self.position, self.size)
        # Update the position and size of each of the Blocks within this Block.
        return True

    def update_block_locations(self, top_left: Tuple[int, int],
                               size: int) -> None:
        """
        Update the position and size of each of the Blocks within this Block.

        Ensure that each is consistent with the position and size of its
        parent Block.

        <top_left> is the (x, y) coordinates of the top left corner of
        this Block.  <size> is the height and width of this Block.
        """
        self.position = top_left  # position of the mother block (level = 0)
        self.size = size  # size of the mother block (level = 0)
        if len(self.children) == 0:
            pass
        else:
            new_size = round(size / 2.0)
            # size of the each child is half of the size of its parent
            self.children[0].update_block_locations((top_left[0] + new_size,
                                                     top_left[1]), new_size)
            self.children[1].update_block_locations(top_left, new_size)
            self.children[2].update_block_locations((top_left[0], top_left[1] +
                                                     new_size), new_size)
            self.children[3].update_block_locations((top_left[0] + new_size,
                                                     top_left[1] + new_size),
                                                    new_size)

    def get_selected_block(self, location: Tuple[int, int], level: int) \
            -> 'Block':
        """Return the Block within this Block that includes the given location
        and is at the given level. If the level specified is lower than
        the lowest block at the specified location, then return the block
        at the location with the closest level value.

        <location> is the (x, y) coordinates of the location on the window
        whose corresponding block is to be returned.
        <level> is the level of the desired Block.  Note that
        if a Block includes the location (x, y), and that Block is subdivided,
        then one of its four children will contain the location (x, y) also;
        this is why <level> is needed.

        Preconditions:
        - 0 <= level <= max_depth
        """
        width = self.position[0] + self.size
        height = self.position[1] + self.size

        if (self.position[0] <= location[0] <= width) and \
                (self.position[1] <= location[1] <= height) and \
                ((self.level == level) or (level == 0) or
                 (len(self.children) == 0)):
            # it means that the given location is inside the area of the block
            # if (self.level == level) or (level == 0) or \
            # (len(self.children) == 0):
            # when the given level is also equal to the block level
            # or our block doesn't have any other children(so it has reachs
            # the max level that it could reach ( which can be different
            # than max_depth))
            # or when the given level is 0 ( when we're lookin for the
            # mother block ( level = 0))

            return self
        elif (self.position[0] <= location[0] <= width) and \
                (self.position[1] <= location[1] <= height) and \
                ((self.level == level) or (level == 0) or
                 (len(self.children) == 0)) is False:
            for block in self.children:
                # looping through its children and if given location is
                # inside the area of the its children, then call the
                # function on that child ( which usualy there is only one
                # child which has this property )
                new_width = block.position[0] + block.size
                new_height = block.position[1] + block.size
                if (block.position[0] <= location[0] <= new_width) and \
                        (block.position[1] <= location[1] <= new_height):
                    return block.get_selected_block(location, level)

        else:
            return self  # when the given location is out of the block area

    def flatten(self) -> List[List[Tuple[int, int, int]]]:
        """Return a two-dimensional list representing this Block as rows
        and columns of unit cells.

        Return a list of lists L, where, for 0 <= i, j < 2^{self.level}
            - L[i] represents column i and
            - L[i][j] represents the unit cell at column i and row j.
        Each unit cell is represented by 3 ints for the colour
        of the block at the cell location[i][j]

        L[0][0] represents the unit cell in the upper left corner of the Block.
        """
        if self.max_depth == self.level:
            # if it's unit cell, just return the list conting a list which only
            # has its colour
            return [[self.colour]]

        elif len(self.children) == 0:
            dimention = 2 ** (self.max_depth - self.level)
            # length of the flatten list and also length of each list inside it
            column = []
            for _ in range(dimention):
                row = [[self.colour] * dimention]
                # row = [[self.colour, self.colour, self.colour,...]]
                # len(row[0]) = dimention
                column.extend(row)
                # column = [[row0], [row1], .... ]
            return column
        else:

            left = []
            right = []
            for index in range(2 ** (self.max_depth - self.children[0].level)):
                # we know that index right now iterate till the dimention of
                # the self.children.flatten(), so it won't go out of range

                left.append(self.children[1].flatten()[index] +
                            self.children[2].flatten()[index])
                # left will be the flatten list of left children of the self
                # ( = self.children [1] and self.children[2] )
                right.append(self.children[0].flatten()[index] +
                             self.children[3].flatten()[index])
                # right will be the flatten list of right children of the self
                # ( = self.children [0] and self.children[3] )

            return left + right


def random_init(level: int, max_depth: int) -> 'Block':
    """Return a randomly-generated Block with level <level> and subdivided
    to a maximum depth of <max_depth>.

    Throughout the generated Block, set appropriate values for all attributes
    except position and size.  They can be set by the client, using method
    update_block_locations.

    Precondition:
        level <= max_depth
    """
    if (level == max_depth) or (random.random() >= math.exp(-0.25 * level)):
        # if level == max_depth it means our block is the unit cell so it can't
        # have any children, the other statement is from handout that help us
        # to make the interesting, unpredictable board for the game
        # in this case our block doesn't have children
        num = random.randint(0, len(COLOUR_LIST) - 1)
        colour = COLOUR_LIST[num]
        # num is the random index that determine the different colour for the
        # block
        block = Block(level, colour, None)
        block.max_depth = max_depth
        return block
    else:
        # our block has children and doesn't have colour, and for producing the
        # children we do the recursive call on random_init
        block = Block(level, None, [random_init(level + 1, max_depth),
                                    random_init(level + 1, max_depth),
                                    random_init(level + 1, max_depth),
                                    random_init(level + 1, max_depth)])
        block.max_depth = max_depth
        for board in block.children:  # assigning the parent to all the children
            board.parent = block
        # as we can see we have assigned value to every attribute of the block
        # except position and size
        return block


def attributes_str(b: Block, verbose) -> str:
    """Return a str that is a concise representation of the attributes of <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Note: These are attributes that every Block has.
    """
    answer = f'pos={b.position}, size={b.size}, level={b.level}, '
    if verbose:
        answer += f'highlighted={b.highlighted}, max_depth={b.max_depth}'
    return answer


def print_block(b: Block, verbose=False) -> None:
    """Print a text representation of Block <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.
    """
    print_block_indented(b, 0, verbose)


def print_block_indented(b: Block, indent: int, verbose) -> None:
    """Print a text representation of Block <b>, indented <indent> steps.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.
    """
    if len(b.children) == 0:
        # b a leaf.  Print its colour and other attributes
        print(f'{"  " * indent}{colour_name(b.colour)}: ' +
              f'{attributes_str(b, verbose)}')
    else:
        # b is not a leaf, so it doesn't have a colour.  Print its
        # other attributes.  Then print its children.
        print(f'{"  " * indent}{attributes_str(b, verbose)}')
        for child in b.children:
            print_block_indented(child, indent + 1, verbose)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['print_block_indented'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer', 'math'
        ],
        'max-attributes': 15
    })

    # This tiny tree with one node will have no children, highlighted False,
    # and will have the provided values for level and colour; the initializer
    # sets all else (position, size, and max_depth) to 0.
    b0 = Block(0, COLOUR_LIST[2])
    # Now we update position and size throughout the tree.
    b0.update_block_locations((0, 0), 750)
    print("=== tiny tree ===")
    # We have not set max_depth to anything meaningful, so it still has the
    # value given by the initializer (0 and False).
    print_block(b0, True)

    b1 = Block(0, children=[
        Block(1, children=[
            Block(2, COLOUR_LIST[3]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, COLOUR_LIST[2]),
        Block(1, children=[
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[3]),
            Block(2, COLOUR_LIST[1])
        ])
    ])
    b1.update_block_locations((0, 0), 750)
    print("\n=== handmade tree ===")
    # Similarly, max_depth is still 0 in this tree.  This violates the
    # representation invariants of the class, so we shouldn't use such a
    # tree in our real code, but we can use it to see what print_block
    # does with a slightly bigger tree.
    print_block(b1, True)

    # Now let's make a random tree.
    # random_init has the job of setting all attributes except position and
    # size, so this time max_depth is set throughout the tree to the provided
    # value (3 in this case).
    b2 = random_init(0, 3)
    # Now we update position and size throughout the tree.
    b2.update_block_locations((0, 0), 750)
    print("\n=== random tree ===")
    # All attributes should have sensible values when we print this tree.
    print_block(b2, True)
