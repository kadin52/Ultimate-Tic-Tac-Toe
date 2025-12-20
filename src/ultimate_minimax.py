from math import inf
from copy import deepcopy
from boardclasses import GlobalBoard, LocalBoard
from time import perf_counter
COMP = 1  
HUMAN = 2

MAXIMIZING_PLAYER = True
MINIMIZING_PLAYER = False

W_GLOBAL_WIN = 10000
W_GLOBAL_THREAT = 500
LOCAL_WIN = 100       
LOCAL_OPPONENT_THREAT = 20  
LOCAL_PLAYER_THREAT = 10
GLOBAL_CENTER_CONTROL = 10
GLOBAL_SCALE = 10

def get_possible_moves(global_board: GlobalBoard):
    moves = []
    targets = []
    
    focused_boards = [i for i, lb in enumerate(global_board.local_board_list) if lb.focus and lb.playable]
    
    if focused_boards:
        targets = focused_boards
    else:
        targets = [i for i, lb in enumerate(global_board.local_board_list) if lb.playable]

    for local_board_index in targets:
        lb = global_board.local_board_list[local_board_index]
        for r in range(3):
            for c in range(3):
                if lb.board[r][c] == 0:
                    moves.append((local_board_index, r, c))
    return moves

def game_over(global_board: GlobalBoard) -> bool:
    return global_board.has_tic_tac_toe(COMP) or \
           global_board.has_tic_tac_toe(HUMAN) or \
           global_board.is_full()

def evaluate_line(line: list, player: int, opponent: int) -> int:
    score = 0
    player_marks = line.count(player)
    opponent_marks = line.count(opponent)
    empty = line.count(0)

    if player_marks == 3:
        score += LOCAL_WIN
    elif opponent_marks == 3:
        score -= LOCAL_WIN
    elif player_marks == 2 and empty == 1:
        score += LOCAL_PLAYER_THREAT
    elif opponent_marks == 2 and empty == 1:
        score -= LOCAL_OPPONENT_THREAT
    elif player_marks == 1 and empty == 2:
        score += 1
    elif opponent_marks == 1 and empty == 2:
        score -= 1
        
    return score

def evaluate_board(grid: list[list[int]], player: int) -> int:
    opponent = (player % 2) + 1
    score = 0

    for r in range(3):
        score += evaluate_line(grid[r], player, opponent)
    
    for c in range(3):
        col = [grid[r][c] for r in range(3)]
        score += evaluate_line(col, player, opponent)

    diag_1 = [grid[i][i] for i in range(3)]
    score += evaluate_line(diag_1, player, opponent)
    
    diag_2 = [grid[2-i][i] for i in range(3)]
    score += evaluate_line(diag_2, player, opponent)

    return score

def heuristic(global_board: GlobalBoard, player: int) -> float:

    total_score = 0
    opponent = (player % 2) + 1
    global_grid = global_board.board 
    
    #global board
    global_score = evaluate_board(global_grid, player) * GLOBAL_SCALE
    total_score += global_score 

    #center control
    center_val = global_grid[1][1]
    if center_val == player:
        total_score += GLOBAL_CENTER_CONTROL
    elif center_val == opponent:
        total_score -= GLOBAL_CENTER_CONTROL

    #local boards
    for r in range(3):
        for c in range(3):
            local_board_index = r * 3 + c
            local_board = global_board.local_board_list[local_board_index]
            
            if global_grid[r][c] == 0:
                local_score = evaluate_board(local_board.board, player)
                total_score += local_score * 1.0 
                
    return total_score


def simulate_move(global_board: GlobalBoard, local_board_index: int, r: int, c: int, player: int):
    local_board = global_board.local_board_list[local_board_index]
    local_board.board[r][c] = player
    
    if local_board.has_tic_tac_toe(player):
        local_board.playable = False
        global_board.mark_global_board(local_board, player)
    elif local_board.is_full():
        local_board.playable = False
        global_board.mark_global_board(local_board, -1)
        
    global_board.update_focus(r, c)

def best_value(global_board: GlobalBoard, depth: int,
          alpha: float, beta: float,
          maximizing: bool, player: int):
    
    if depth == 0 or game_over(global_board):
        return heuristic(global_board, player), None

    if maximizing:
        return max_value(global_board, depth, alpha, beta, player)
    else:
        return min_value(global_board, depth, alpha, beta, player)


def max_value(global_board: GlobalBoard, depth: int,
              alpha: float, beta: float, player: int):
    
    valid_moves = get_possible_moves(global_board)
    if not valid_moves:
        return heuristic(global_board, player), None

    best_move = None
    value = -inf

    for local_board_index, r, c in valid_moves:
        next_state = deepcopy(global_board)
        simulate_move(next_state, local_board_index, r, c, player)

        evaluation, move = best_value(next_state, depth - 1, alpha, beta,
                              MINIMIZING_PLAYER, player)

        if evaluation > value:
            value = evaluation
            best_move = (local_board_index, r, c)

        alpha = max(alpha, value)
        if beta <= alpha:
            break

    return value, best_move   

def min_value(global_board: GlobalBoard, depth: int,
              alpha: float, beta: float, player: int):
    
    valid_moves = get_possible_moves(global_board)
    if not valid_moves:
        return heuristic(global_board, player), None

    best_move = None
    value = inf
    opponent = (player % 2) + 1

    for local_board_index, r, c in valid_moves:
        next_state = deepcopy(global_board)
        simulate_move(next_state, local_board_index, r, c, opponent)

        evaluation, _ = best_value(next_state, depth - 1, alpha, beta,
                              MAXIMIZING_PLAYER, player)

        if evaluation < value:
            value = evaluation
            best_move = (local_board_index, r, c)

        beta = min(beta, value)
        if beta <= alpha:
            break

    return value, best_move

def minimax(global_board: GlobalBoard, depth: int,
            alpha: float, beta: float,
            maximizing: bool, player: int):
    return best_value(global_board, depth, alpha, beta, maximizing, player)

def bot_turn(global_board: GlobalBoard, bot_player: int):
    # start = perf_counter()

    score, move = minimax(global_board, 5, -inf, inf, MAXIMIZING_PLAYER, bot_player)
    
    # duration = perf_counter() - start
    # print(f"Minimax computed in {duration:.4f} seconds")

    if move:
        local_board_index, r, c = move
        return global_board.local_board_list[local_board_index], r, c
    return None


