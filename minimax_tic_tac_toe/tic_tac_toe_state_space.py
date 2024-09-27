"""
Simple script that will create all possible future board states of
a Tic-Tac-Toe game given a current game state.

The states are printed to the terminal and a networkx graph of the search space
will be produced.

@author elegantmoose
"""

import argparse
import networkx as nx
import copy
import matplotlib.pyplot as plt


OPEN_SQUARE = 0
USER_SQUARE = 1
AI_SQUARE = 2


USER_WIN = -100
AI_WIN = 100


WIN_LINES = [
    (0, 3, 6),
    (0, 4, 8),
    (0, 1, 2),
    (1, 4, 7),
    (2, 4, 6),
    (2, 5, 8),
    (3, 4, 5),
    (6, 7, 8),
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

    def __init__(self, depth=0, state=[0, 0, 0, 0, 0, 0, 0, 0, 0], utility=0):
        global STATE_ID_COUNTER
        self.id = str(STATE_ID_COUNTER)
        STATE_ID_COUNTER += 1
        self.depth = depth
        self.utility = utility

    def asdict(self):
        return {
            "id": self.id,
            "depth": self.depth,
            "state": self.state,
            "utility": self.utility,
        }


def next_turn(turn):
    return USER_SQUARE if turn == AI_SQUARE else AI_SQUARE


def _line_moves(line, state):
    state_squares = [state.state[line[0]], state.state[line[1]], state.state[line[2]]]
    line_moves = {0: 0, 1: 0, 2: 0}
    for square in state_squares:
        line_moves[square] += 1
    return line_moves


def eval_function(state):
    """
    Eval = 3*X2 + X1 - (3*O2 + O1)

    where:

    Xn is number of rows, columns or diaganols with exactly n X's and no O's

    On is number of rows, columns or diaganols with exactly n O's and no X's
    """
    x_1 = 0
    x_2 = 0
    o_1 = 0
    o_2 = 0
    for line in WIN_LINES:
        line_moves = _line_moves(line, state)
        if line_moves == {0: 0, 1: 3, 2: 0}:
            return USER_WIN
        elif line_moves == {0: 0, 1: 0, 2: 3}:
            return AI_WIN
        elif line_moves == {0: 1, 1: 2, 2: 0}:
            o_2 += 1
        elif line_moves == {0: 2, 1: 1, 2: 0}:
            o_1 += 1
        elif line_moves == {0: 1, 1: 0, 2: 2}:
            x_2 += 1
        elif line_moves == {0: 2, 1: 0, 2: 1}:
            x_1 += 1
        else:
            pass
    return 3 * x_2 + x_1 - (3 * o_2 + o_1)


def expand(state, turn):
    # print(f"(EXPAND) State: {state.asdict()},  turn: {turn}")
    expanded_states = []
    for idx, i in enumerate(state.state):
        if i == 0:  # open square
            new_state = TicTacToeState()
            new_state.state = copy.copy(state.state)
            new_state.state[idx] = turn
            new_state.depth = state.depth + 1
            new_state.utility = eval_function(new_state)
            expanded_states.append(new_state)
    return expanded_states


def search(graph, state, turn, stop_depth=None):
    if state.utility in [USER_WIN, AI_WIN]:
        return []
    if stop_depth and state.depth > stop_depth:
        return []
    expanded_states = expand(state, turn)
    for new_state in expanded_states:
        graph.add_node(new_state.id, **new_state.asdict())
        graph.add_edge(state.id, new_state.id)

        substates = search(
            graph,
            new_state,
            next_turn(turn),
            stop_depth=(stop_depth - 1) if stop_depth is not None else None,
        )
        # add subtree max-min values
    print(f"(SEARCH) State: {state.asdict()}     Turn: {turn}")
    print(f"---Expanded to:")
    for s in expanded_states:
        print(f"--- {s.asdict()}")
    return expanded_states


def color_best_states(graph):
    """ """
    best = {}
    running_best = 0
    for node_id in graph.nodes():
        state = graph.nodes[node_id]
        if state["utility"] >= running_best:
            if state["id"] not in best:
                best[state["id"]] = [state["id"]]
            else:
                best[state["utility"]].append(state["id"])
            running_best = state["utility"]

    # removing all but highest value nodes
    best = best[sorted(list(best.keys()), reverse=True)[0]]

    node_color_map = []
    for node_id in graph.nodes():

        if node_id in best:
            node_color_map.append("green")
        else:
            node_color_map.append("blue")

    return node_color_map


def _get_argparser():
    """to organize and clean format argparser args"""
    parser = argparse.ArgumentParser()

    parser.add_argument("--depth", default=None, help="search depth")

    return parser


def main():
    parser = _get_argparser()
    args = parser.parse_args()

    # initialize root state
    initial_state = TicTacToeState()
    initial_state.state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    initial_state.utility = eval_function(initial_state)

    # initialize graph with first node
    G = nx.Graph()
    G.add_node(initial_state.id, **initial_state.asdict())

    # execute search
    search(graph=G, state=initial_state, turn=AI_SQUARE, stop_depth=int(args.depth))

    # best path
    node_color_map = color_best_states(G)

    # -- Print search
    print(f"Graph node count (states): {len(list(G.nodes))}")
    print(f"Best states:")
    for idx, color in enumerate(node_color_map):
        if color == "green":
            print(G.nodes[str(idx)])
    nx.draw_networkx(G, with_labels=True, node_color=node_color_map)
    plt.show()


if __name__ == "__main__":
    main()
