from math import inf
from gamestate import GameState
from board import Board
from player import Player

PRUNE = [0]


# creates obj
class MinimaxInfo:
    def __init__(self, value, action):
        self.value = value
        self.action = action


def TO_MOVE(board):
    """
        function that takes a state
        returns the player who moves next from that state.
        (This might just be a variable stored in the state object itself.)
    """
    curr_player = board.get_player_to_move_next()
    #   print("TO_MOVE // current player is ", curr_player)
    return curr_player


def ACTIONS(board, DEBUG):
    """
        returns all legal actions from current state
    """
    actions = []
    cols = board.num_cols
    #   if DEBUG:
    #       print(cols)
    # print(board.is_column_full(cols))

    for col in range(cols):
        #     print(col)
        if not board.is_column_full(col):
            actions.append(col)

    #   print("ACTIONS: ", actions)
    return actions


def UTILITY(board, DEBUG):
    """
        calculates the utility of a terminal state
        such as Win, Loss, Draw
        considers the number of moves for this
    """
    utility = 0
    moves = board.moves_made_so_far
    #    print("Game state: ", board.game_state)
    #   print("MAX WIN? ", GameState.MAX_WIN)
    rows = float(board.get_rows())
    cols = float(board.get_cols())
    #  print("rows = ", rows, "cols = ", cols)
    if board.game_state == GameState.MAX_WIN:
        utility = (10000.0 * rows * cols) / moves
    #      if DEBUG:
    #          print(utility)
    if board.game_state == GameState.MIN_WIN:
        utility = (-10000.0 * rows * cols) / moves
    #      if DEBUG:
    #          print(utility)
    return utility


def RESULT(board, action):
    """
        takes in the current board and an action
        returns a new state (the child state) that results from taking
        the action in the original state
        assumes that the next move is legal
    """
    next_move = board.make_move(action)
    #    print("next move is: ", next_move)
    return next_move


def IS_TERMINAL(board, DEBUG):
    """
        returns true if state is a terminal state
    """
    #   if DEBUG:
    #       print("The state of the game is ", board.get_game_state())
    if board.get_game_state() == GameState.IN_PROGRESS:
        return False
    elif board.game_state == GameState.TIE:
        return True
    elif board.game_state == GameState.MAX_WIN:
        return True
    elif board.game_state == GameState.MIN_WIN:
        return True


def minimax(board, table, DEBUG):
    # print("The number of states is: ", len(table))

    if DEBUG:
        print(board.to_2d_string())
    if board in table:
        return table[board]

    elif IS_TERMINAL(board, DEBUG):
        utility = UTILITY(board, DEBUG)
        info = MinimaxInfo(utility, None)  # no action because end of the game
        table[board] = info

        return info

    elif TO_MOVE(board) == Player.MAX:
        v = float(-inf)
        best_move = None
        for action in ACTIONS(board, DEBUG):
            child_state = RESULT(board, action)
            child_info = minimax(child_state, table, DEBUG)
            v2 = child_info.value
            if v2 > v:
                v = v2
                best_move = action
        info = MinimaxInfo(v, best_move)
        table[board] = info

        print("Minimax value for this state: ", child_state, "optimal move: ", best_move)
        print("It is ", TO_MOVE(board), "'s turn!")
        print("Player chose move: ", best_move)

        if DEBUG:
            print(child_state, "->", "MinimaxInfo(value = ", info.value, ",action = ", info.action, ")")

        print("The number of states is: ", len(table))
        return info

    elif TO_MOVE(board) == Player.MIN:
        v = float(inf)
        best_move = None
        for action in ACTIONS(board, DEBUG):
            child_state = RESULT(board, action)
            child_info = minimax(child_state, table, DEBUG)
            v2 = child_info.value
            if v2 < v:
                v = v2
                best_move = action
        info = MinimaxInfo(v, best_move)
        table[board] = info

        print("Minimax value for this state: ", child_state, "optimal move: ", best_move)
        print("It is ", TO_MOVE(board), "'s turn!")
        print("Player chose move: ", best_move)

        if DEBUG:
            print(child_state, "->", "MinimaxInfo(value = ", info.value, ",action = ", info.action, ")")

        print("The number of states is: ", len(table))

        return info


def minimax_alpha_beta_pruning(board, alpha, beta, table, PRUNE, DEBUG):
    if DEBUG:
        print(board.to_2d_string())

    if board in table:
        return table[board]

    elif IS_TERMINAL(board, DEBUG):
        utility = UTILITY(board, DEBUG)
        info = MinimaxInfo(utility, None)  # no action because end of the game
        table[board] = info
        return info

    elif TO_MOVE(board) == Player.MAX:
        v = float(-inf)

        best_move = None

        for action in ACTIONS(board, DEBUG):
            child_state = RESULT(board, action)
            child_info = minimax_alpha_beta_pruning(child_state, alpha, beta, table, PRUNE, DEBUG)
            v2 = child_info.value

            if v2 > v:
                v = v2
                best_move = action
                alpha = max(alpha, v)  # returns the max for this

            if v >= beta:  # prune tree, don't store state in table
                PRUNE[0] += 1
                return MinimaxInfo(v, best_move)

            print("Minimax value for this state: ", child_state, "optimal move: ", best_move)
            print("It is ", TO_MOVE(board), "'s turn!")
            print("Player chose move: ", best_move)
            print("Number of times pruned: ", PRUNE)

        print("The number of states is: ", len(table))
        info = MinimaxInfo(v, best_move)
        table[board] = info

        if DEBUG:
            print(child_state, "->", "MinimaxInfo(value = ", info.value, ",action = ", info.action, ")")

        return info

    elif TO_MOVE(board) == Player.MIN:
        v = float(inf)
        best_move = None
        #       print("v = ", v, " & the best move is ", best_move)
        for action in ACTIONS(board, DEBUG):
            child_state = RESULT(board, action)
            child_info = minimax_alpha_beta_pruning(child_state, alpha, beta, table, PRUNE, DEBUG)
            v2 = child_info.value

            if v2 < v:
                v = v2
                best_move = action
                beta = min(beta, v)

            if v <= alpha:
                PRUNE[0] += 1
                return MinimaxInfo(v, best_move)

            print("Minimax value for this state: ", child_state, "optimal move: ", best_move)
            print("It is ", TO_MOVE(board), "'s turn!")
            print("Player chose move: ", best_move)
            print("Number of times pruned: ", PRUNE)

        print("The number of states is: ", len(table))

        info = MinimaxInfo(v, best_move)
        table[board] = info

        if DEBUG:
            print(child_state, "->", "MinimaxInfo(value = ", info.value, ",action = ", info.action, ")")

        return info


def main():
    algorithm_choose = input("Run part A, B, or C? ").upper()
    #
    print_debug = input("Include debugging info? (y/n)").upper()

    rows = int(input("Enter rows: "))
    cols = int(input("Enter columns: "))
    connect_num = int(input("Enter number in a row to win: "))

    board = Board(rows, cols, connect_num)
    table = {}

    # please play as max
    chose_player = input("Which player do you want to play as? (MAX or MIN)").upper()
    if chose_player == "MAX":
        player = Player.MAX
    elif chose_player == "MIN":
        player = Player.MIN
    print("You are player ", player)

    if print_debug == 'Y':
        DEBUG = True

    if algorithm_choose == 'A':
        opt_move = minimax(board, table, DEBUG)

    elif algorithm_choose == 'B':
        alpha = float(-inf)
        beta = float(inf)

        opt_move = minimax_alpha_beta_pruning(board, alpha, beta, table, PRUNE, DEBUG)

    while True:
        print(board.to_2d_string())

        if player == Player.MAX:
            print("It is ", player, "'s turn!")
            move = int(input("Enter move: "))
            if move not in ACTIONS(board, DEBUG):
                print("This move is invalid")
                continue
            board = RESULT(board, move)
            player = board.get_player_to_move_next()
            print(player)
        elif player == Player.MIN:
            if algorithm_choose == 'A':
                opt_move = minimax(board, table, DEBUG)
                computer_move = opt_move.action
                board = RESULT(board, computer_move)
                player = Player.MAX

            elif algorithm_choose == 'B':
                alpha = float(-inf)
                beta = float(inf)

                opt_move = minimax_alpha_beta_pruning(board, alpha, beta, table, PRUNE, DEBUG)
                computer_move = opt_move.action
                board = RESULT(board, computer_move)
                player = Player.MAX

            elif board.get_game_state() != GameState.IN_PROGRESS:
                print("Game over.")
                break


main()
