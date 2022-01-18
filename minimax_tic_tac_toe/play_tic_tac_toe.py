import argparse
from os import stat
import networkx as nx
import copy
from enum import Enum
#import matplotlib.pyplot as plt
import time

import logging


OPEN_SQUARE = 0
USER_SQUARE = 1
AI_SQUARE = 2
NOT_TERMINAL = 3

POS_INFINITY = 1000
NEG_INFINITY = -1000

MAX = AI_SQUARE
MIN = USER_SQUARE


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

logging.basicConfig(filename='minimax.log', level=logging.DEBUG)


class AdversaryAI(Enum):
    MINIMAX = 'minimax'
    MINIMAX_AB_PRUNE = 'minimax-ab-prune'


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
    def __init__(self, depth=0, state=[0,0,0,0,0,0,0,0,0], utility=None):
        self.id = self.create_state_id()
        self.depth = depth
        self.utility = utility
        self.state = state
        self.next_state = -1
    
    def asdict(self):
        return {'id': self.id, 'depth': self.depth, 'state': self.state, 'utility': self.utility, 'next_state': self.next_state}

    def __str__(self):
        return str(self.asdict())

    @staticmethod
    def create_state_id():
        global STATE_ID_COUNTER
        id = str(STATE_ID_COUNTER)
        STATE_ID_COUNTER += 1 
        return id


""" Minimax Functions"""


def terminal_state_utility(state):
    """ """
    winner = terminal_state(state)
    if winner == AI_SQUARE:
        return 1
    elif winner == USER_SQUARE:
        return -1
    elif winner == OPEN_SQUARE:
        return 0
    else:
        return NOT_TERMINAL


def expand_ttt_states(state, turn):
    """ """
    expanded_states = []
    for idx, i in enumerate(state.state):
        if i == OPEN_SQUARE: # open square
            new_state = TicTacToeState()
            new_state.state = copy.copy(state.state)
            new_state.state[idx] = turn
            new_state.utility = POS_INFINITY if turn == AI_SQUARE else NEG_INFINITY
            new_state.depth = state.depth + 1
            expanded_states.append(new_state)
    return expanded_states


def minimax_search(GAME_BOARD, ab_prune=False):
    # initialize root state
    initial_state = TicTacToeState()
    initial_state.state = copy.copy(GAME_BOARD)
    initial_state.utility = NEG_INFINITY

    # initialize minimax tree
    MINIMAX_TREE = nx.Graph()
    MINIMAX_TREE.add_node(initial_state.id, **initial_state.asdict())

    # minimax search
    states_explored = max_value(initial_state, [], MINIMAX_TREE, ab_prune=ab_prune)
    return initial_state.next_state, states_explored, MINIMAX_TREE


def max_value(state, sibling_state_utilities, graph, ab_prune=False):
    states_explored = 0
    if terminal_state(state) != NOT_TERMINAL:
        state.utility = terminal_state_utility(state)
        state.next_state = None
        return 1

    expanded_states = expand_ttt_states(state, turn=MAX)
    expanded_sibling_state_utilities = set([])
    for next_state in expanded_states:
        if ab_prune and alpha_beta_prune(state, sibling_state_utilities, turn=MAX):
            # no need to recurse further, there is a parent sibling
            # utility score that will at least be better than the utility
            # found on this state recursion
            break
    
        graph.add_node(next_state.id, **next_state.asdict())
        graph.add_edge(state.id, next_state.id)
        sub_states_explored = min_value(next_state, expanded_sibling_state_utilities, graph, ab_prune=ab_prune)
        # logging.info("max---")
        # logging.info(f"state: {state}")
        # logging.info(f"next_state: {next_state}")
        if next_state.utility > state.utility:
            # logging.info(f'--max updating utility: {state.utility} --> {next_state.utility}')
            state.utility = next_state.utility
            state.next_state = next_state
        states_explored += sub_states_explored
    #assert state.next_state != -1
    return states_explored


def min_value(state, sibling_state_utilities, graph, ab_prune=False):
    states_explored = 0
    if terminal_state(state) != NOT_TERMINAL:
        state.utility = terminal_state_utility(state)
        state.next_state = None
        return 1

    expanded_states = expand_ttt_states(state, turn=MIN)
    expanded_sibling_state_utilities = set([])
    for next_state in expanded_states:
        if ab_prune and alpha_beta_prune(state, sibling_state_utilities, turn=MIN):
            # no need to recurse further, there is a parent sibling
            # utility score that will at least be better than the utility
            # found on this state recursion
            break

        graph.add_node(next_state.id, **next_state.asdict())
        graph.add_edge(state.id, next_state.id)

        sub_states_explored = max_value(next_state, expanded_sibling_state_utilities, graph, ab_prune=ab_prune)
        # logging.info("min---")
        # logging.info(f"state: {state}")
        # logging.info(f"next_state: {next_state}")
        if next_state.utility < state.utility:
            # logging.info(f'--min updating utility: {state.utility} --> {next_state.utility}')
            state.utility = next_state.utility
            state.next_state = next_state
        expanded_sibling_state_utilities.add(next_state.utility)
        states_explored += sub_states_explored
    #assert state.next_state != -1
    return states_explored


def alpha_beta_prune(state, parent_state_sibling_utilities, turn):
    """ """
    if state.utility in [NEG_INFINITY, POS_INFINITY]:
        # state hasnt been recursed on at all yet
        return False
    for utility in parent_state_sibling_utilities:
        if turn == MAX:
            if utility > state.utility:
                return True
        elif turn == MIN:
            if utility < state.utility:
                return True
    return False


def terminal_state(state):
    for line in WIN_LINES:
        if state.state[line[0]] != OPEN_SQUARE:
            if state.state[line[0]] == state.state[line[1]] and state.state[line[1]] == state.state[line[2]]:
                return state.state[line[0]]
    if 0 not in set(state.state):
        return OPEN_SQUARE
    return NOT_TERMINAL


""" Game Utilities """


def next_ai_move(GAME_BOARD, ai=AdversaryAI.MINIMAX, stats=False):
    ab_prune = True if ai == AdversaryAI.MINIMAX_AB_PRUNE else False
    start_time = time.time()
    next_state, states_explored, minimax_tree = minimax_search(GAME_BOARD, ab_prune=ab_prune)
    stop_time = time.time()
    search_stats = None
    if stats:
        search_stats = {
            'time': (stop_time - start_time),
            'states_explored': states_explored,
            'tree': minimax_tree
        }
    return copy.copy(next_state.state), search_stats


def next_turn(turn):
    return USER_SQUARE if turn == AI_SQUARE else AI_SQUARE


def prompt_and_apply_user_move(GAME_BOARD):
    print_board_layout()
    print('Your move:')
    user_move = int(input())
    assert user_move in [0,1,2,3,4,5,6,7,8,9] and GAME_BOARD[user_move] == OPEN_SQUARE
    GAME_BOARD[user_move] = USER_SQUARE


""" Print Utilities """


def print_minimax_tree(graph):
    for node, neighbors in graph.adj.items():
        print(node)
        print('----')
        print(neighbors)



def print_board_layout():
    print("--Board layout--")
    print('   0  3  6')
    print('   1  4  7')
    print('   2  5  8')
    print('--------------')


def show_winner(GAME_BOARD):
    for line in WIN_LINES:
        if GAME_BOARD[line[0]] != OPEN_SQUARE:
            if GAME_BOARD[line[0]] == GAME_BOARD[line[1]] and GAME_BOARD[line[1]] == GAME_BOARD[line[2]]:
                print("Game Over")
                if GAME_BOARD[line[0]] == USER_SQUARE:
                    print('User wins.')
                else:
                    print('AI wins.')
                return True
    if not len([i for i in GAME_BOARD if i == 0]):
        print('Game Over. Tie.')
        return True
    return False


def print_board(GAME_BOARD):
    present = copy.copy(GAME_BOARD)
    for idx, i in enumerate(present):
        if i == 0:
            present[idx] = ' '
        elif i == 1:
            present[idx] = 'O'
        else:
            present[idx] = 'X'

    print("\n")
    print(f"{present[0]} | {present[3]} | {present[6]} ")
    print(f"----------")
    print(f"{present[1]} | {present[4]} | {present[7]} ")
    print(f"----------")
    print(f"{present[2]} | {present[5]} | {present[8]} ")
    print('\n')


""" Main """


def play_game(ai=AdversaryAI.MINIMAX, stats=False):
    """
    The board is laid out as:
    
        0  3  6
        1  4  7
        2  5  8
    """
    GAME_BOARD = [0,0,0,0,0,0,0,0,0]

    # start game
    while True:
        print_board(GAME_BOARD)
        prompt_and_apply_user_move(GAME_BOARD)
        print_board(GAME_BOARD)
        if show_winner(GAME_BOARD):
            break
        GAME_BOARD, search_stats = next_ai_move(GAME_BOARD, stats=stats, ai=ai)
        if stats:
            print(f"Took AI {search_stats['time']} seconds and searched {search_stats['states_explored']} states.")
        print_board(GAME_BOARD)
        if show_winner(GAME_BOARD):
            break


def _get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ai',
        dest='ai',
        default=AdversaryAI.MINIMAX,
        help='type of AI adversary. Options include: "minimax", "mimimax-ab-prune'
    )
    
    parser.add_argument(
        '--stats',
        dest='stats',
        action='store_true',
        default=False,
        help="verbose mode to print out AI adversarial game search stats"
    )

    return parser


def main():
    args = _get_argparser().parse_args()
    if args.ai == AdversaryAI.MINIMAX_AB_PRUNE.value:
        args.ai = AdversaryAI.MINIMAX_AB_PRUNE
    play_game(ai=args.ai, stats=args.stats)


if __name__ == '__main__':
    main()
