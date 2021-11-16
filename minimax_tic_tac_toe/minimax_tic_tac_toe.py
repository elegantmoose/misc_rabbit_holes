"""
A basic MiniMax implementation for Tic-Tac-Toe w/ verbose terminal output.

The script initializes a desired Tic-Tac-Toe state and starts the
MiniMax algo on the initial Tic-Tac-Toe state, printing out all the steps
of MiniMax algo.

@author elegantmoose
"""

import copy


OPEN_SQUARE = 0
USER_SQUARE = 1
AI_SQUARE = 2


USER_WIN = -1
AI_WIN = 1
DRAW = 0
NOT_TERMINAL = 2324


NEGATIVE_INFINITY = -100
POSITIVE_INFINITY = 100


WIN_LINES = [
    (0, 3, 6),
    (0, 4, 8),
    (0, 1, 2),
    (1, 4, 7),
    (2, 4, 6),
    (2, 5, 8),
    (3, 4, 5),
    (6, 7, 8)
]


STATE_ID_COUNTER = 0


class TicTacToeState:
    """
    Notes
    A '0' is open
    A '1' is a user mark (0)
    A '2' in the place idx is an AI mark (X)
   
    The board is laid out as:
    
        0  3  6
        1  4  7
        2  5  8
    """
    state_counter = 0
    def __init__(self, depth=0, state=[0,0,0,0,0,0,0,0,0], action=None, turn=None):
        global STATE_ID_COUNTER
        self.id = str(STATE_ID_COUNTER)
        STATE_ID_COUNTER += 1 
        self.depth = depth
        self.state = state
        self.turn = turn
        self.action = action
        self.terminal = False
    
    def asdict(self):
        return {'id': self.id, 'depth': self.depth, 'state': self.state, 'terminal': self.terminal}

    def print(self):
        indent =  self.get_print_indent()
        print(f'{indent}State: {self.id}  Depth: {self.depth}')
        self.print_state_board()

    def print_state_board(self):
        indent =  self.get_print_indent()
        present = copy.copy(self.state)
        for idx, i in enumerate(present):
            if i == OPEN_SQUARE:
                present[idx] = ' '
            elif i == USER_SQUARE:
                present[idx] = 'O'
            elif i == AI_SQUARE:
                present[idx] = 'X'

        print("\n")
        print(f"{indent}{present[0]} | {present[3]} | {present[6]} ")
        print(f"{indent}----------")
        print(f"{indent}{present[1]} | {present[4]} | {present[7]} ")
        print(f"{indent}----------")
        print(f"{indent}{present[2]} | {present[5]} | {present[8]} ")
        print('\n')

    def get_print_indent(self):
        return ' '.join(['        ']*self.depth)
    
    def get_pretty_turn(self):
        return 'O' if self.turn == USER_SQUARE else 'X'


def next_turn(turn):
    return USER_SQUARE if turn == AI_SQUARE else AI_SQUARE


def _line_moves(line, state):
    state_squares = [state.state[line[0]], state.state[line[1]], state.state[line[2]]]
    line_moves = {0: 0, 1:0, 2:0}
    for square in state_squares:
        line_moves[square] += 1
    return line_moves


def is_terminal(state):
    for line in WIN_LINES:
        line_moves = _line_moves(line, state)
        if line_moves == {0:0, 1:3, 2:0}:
            return USER_WIN
        elif line_moves == {0:0, 1:0, 2:3}:
            return AI_WIN
    if 0 not in state.state:
        return DRAW
    return NOT_TERMINAL


def expand(state, turn):
    expanded_states = []
    for idx, i in enumerate(state.state):
        if i == 0: # open square
            new_state = TicTacToeState()
            new_state.state = copy.copy(state.state)
            new_state.state[idx] = turn
            new_state.turn = turn
            new_state.action = idx
            new_state.depth = state.depth + 1
            expanded_states.append(new_state)
    return expanded_states


def min_max_search(state, turn):
    """ """
    if turn == AI_SQUARE:
        value, move = max_value(state, turn)
    elif turn == USER_SQUARE:
        value, move = min_value(state, turn)
    return move


def max_value(state, turn):
    """ """
    v = NEGATIVE_INFINITY
    indent = state.get_print_indent()
    print(f'{indent}--------------------max_value()')
    state.print()
    print(f'{indent}v={v}')
    state.terminal = is_terminal(state)
    if state.terminal != NOT_TERMINAL:
        print(f'{indent}Terminal State Reached.')
        print(f'{indent}Utility: {state.terminal}')
        print(f'{indent}v updated:  v={v} --> v={state.terminal}')
        return state.terminal, None
    move = None
    for a in expand(state, turn):
        print(f"{indent}|")
        print(f"{indent}|")
        print(f"{indent} Player {a.get_pretty_turn()} - Action: {a.action}")
        print(f'{indent}|')
        print(f'{indent}|')
        v2, a2 = min_value(a, next_turn(turn))
        print(f'{indent}v2={v2}')
        if v2 > v:
            print(f'{indent}v updated:  v={v} --> v={v2}')
            print(f'{indent}move updated:  move={move} --> move={a.action}')
            v = v2
            move = a.action
    print(f'{indent}Complete--------------------max_value()')
    print(f'{indent}Returning: v={v}  move={move}')
    return v, move


def min_value(state, turn):
    """ """
    v = POSITIVE_INFINITY
    indent = state.get_print_indent()
    print(f'{indent}--------------------min_value()')
    state.print()
    print(f'{indent}v={v}')
    state.terminal = is_terminal(state)
    if state.terminal != NOT_TERMINAL:
        print(f'{indent}Terminal State Reached.')
        print(f'{indent} Utility: {state.terminal}')
        print(f'{indent}v updated:  v={v} --> v={state.terminal}')
        return state.terminal, None
    move = None
    for a in expand(state, turn):
        print(f"{indent}|")
        print(f"{indent}|")
        print(f"{indent} Player {a.get_pretty_turn()} - Action: {a.action}")
        print(f'{indent}|')
        print(f'{indent}|')
        v2, a2 = max_value(a, next_turn(turn))
        print(f'\n{indent}v2={v2}')
        if v2 < v:
            print(f'{indent}v updated:  v={v} --> v={v2}')
            print(f'{indent}move updated:  move={move} --> move={a.action}')
            v = v2
            move = a.action
    print(f'{indent}Complete--------------------min_value()')
    print(f'{indent}Returning: v={v}  move={move}')
    return v, move


def main():
    # initialize root state
    initial_state = TicTacToeState()
    initial_state.state = [2,0,0,0,1,0,1,0,2]

    # execute mini max
    min_max_search(initial_state, turn=AI_SQUARE)


if __name__ == "__main__":
    main()
