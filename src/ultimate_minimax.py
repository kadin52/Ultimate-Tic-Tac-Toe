from  boardclasses import TicTacToeBoard, LocalBoard, GlobalBoard

import math

player_x = 1
player_o = 2
total_moves_possible = 81
local_win_score = 10000
center_score = 50
defense_score = 10
has_tic_tac_toe_score = 100
def get_empty_cells(state: TicTacToeBoard) -> list[tuple[int]]:

    cells = []
    for row_index, row in enumerate(state.board):
        for col_index, cell in enumerate(row):
            if cell == 0:
                cells.append((row_index, col_index))
    return cells

def get_valid_moves(global_board):
    focus = False
    targets = []
    valid_moves = []
    for board in global_board.local_board_list:
        if board.focus:
            targets.append(board)
            focus = True
            break
    if not focus:
        for board in global_board.local_board_list:
            if board.playable:
                targets.append(board)
    for lb in targets:
        for row, col, in get_empty_cells(board):
            valid_moves.append((board,row,col))
    return valid_moves

def has_threat(local_board, player) -> int:
    threat_count = 0
    
    for x in range(3):
 
        row = local_board.board[x]
        if row.count(player) == 2 and row.count(0) == 1:
            threat_count += 1
        col = [local_board.board[y][x] for y in range(3)]
        if col.count(player) == 2 and col.count(0) == 1:
            threat_count += 1
    

    diag1 = [local_board.board[i][i] for i in range(3)]
    if diag1.count(player) == 2 and diag1.count(0) == 1:
        threat_count += 1
    
    diag2 = [local_board.board[2-i][i] for i in range(3)]
    if diag2.count(player) == 2 and diag2.count(0) == 1:
        threat_count += 1
    
    return threat_count
        

def heuristic(global_board, player, moves_played) -> float:
    if player == player_x:
        opponent = player_o
    else:
        opponent = player_x
    if global_board.has_tic_tac_toe(player):
        return has_tic_tac_toe_score
    if global_board.has_tic_tac_toe(opponent):
        return -1 * has_tic_tac_toe_score
    
    progress = moves_played / total_moves_possible
    
    weight_center = center_score * (1 - progress)

    weight_threat = defense_score + (190 * progress)

    score= 0
    for index, board in enumerate(global_board.local_board_list):
        if board.playable:
            opponent_threats = has_threat(board, opponent)
            player_threats = has_threat(board, player)

            score -= weight_threat * opponent_threats
            score += (weight_threat * .5) * player_threats

            if index == 4:
                score += weight_center
    return score



        
        
        
                    

def find_value(global_board, depth, alpha, beta, maximizing_player, player):
    if depth == 0:
        return heuristic(global_board, player), None
    if maximizing_player:
        return max_value(global_board, depth, alpha, beta, player)
    else:
        return min_value(global_board, depth, alpha, beta, player)
    
def max_value(global_board, depth, alpha, beta, player):
    value = float('inf')
    best_move = None
    moves = get_valid_moves(global_board)
    if not moves:
        return heuristic(global_board,player),None
    for move in moves:
        local_board, row, col = move
        local_board.board[row][col] = player

        score,_ = find_value(global_board, depth - 1, alpha, beta, False, player)
        local_board.board[row][col] = 0  
        if score > value:
            value = score
            best_move = move
        alpha = max(alpha, value)
        if beta <= alpha:
            return value, best_move
    return value, best_move

def min_value(global_board, depth, alpha, beta, player):
    value = float('-inf')
    best_move = None
    moves = get_valid_moves(global_board)
    if not moves:
        return heuristic(global_board,player),None
    for move in moves:
        local_board, row, col = move
        local_board.board[row][col] = player

        score,_ = find_value(global_board, depth - 1, alpha, beta, True, player)
        local_board.board[row][col] = 0  
        if score < value:
            value = score
            best_move = move
        beta = min(beta, value)
        if beta <= alpha:
            return value, best_move
    return value, best_move

def minimax(global_board, depth, alpha, beta, maximizing_player, player):
    return find_value(global_board, depth, alpha, beta, maximizing_player, player)

def bot_turn(global_board, bot):
    


if __name__ == "__main__":
    gb = GlobalBoard()
 # Test 1: Get a move on empty board
    print("\nTest 1: First move on empty board")
    move = bot_turn(global_board, player=1)
    if move:
        lb, row, col = move
        print(f"Bot chose: Local Board {global_board.local_board_list.index(lb)}, Position ({row}, {col})")
    else:
        print("ERROR: No move returned")
    
    # Test 2: Make some moves and get bot response
    print("\nTest 2: Making some moves...")
    # Player 1 takes center of board 4
    global_board.local_board_list[4].board[1][1] = 1
    global_board.local_board_list[4].playable = True
    
    # Player 2's turn
    move = bot_turn(global_board, player=2)
    if move:
        lb, row, col = move
        print(f"Bot (Player 2) chose: Local Board {global_board.local_board_list.index(lb)}, Position ({row}, {col})")
    else:
        print("ERROR: No move returned")
    
    # Test 3: Check heuristic value
    print("\nTest 3: Heuristic evaluation")
    score = heuristic(global_board, player=1)
    print(f"Board score for Player 1: {score}")
    
    print("\n" + "=" * 50)
    print("Tests complete!")