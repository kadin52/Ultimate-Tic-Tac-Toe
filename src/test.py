import random
from ultimate_minimax import bot_turn, game_over, get_possible_moves, simulate_move
from boardclasses import GlobalBoard, LocalBoard


def random_bot_turn(global_board, bot_player):
    moves = get_possible_moves(global_board)
    if moves:
        local_board, row, col = random.choice(moves)
        return global_board.local_board_list[local_board], row, col
    return None

def bot_test(total_games, outside_bot_turn: callable):

    minimax_wins_player_x = 0
    minimax_wins_player_o = 0
    outside_wins_player_x = 0
    outside_wins_player_o = 0
    draws = 0

    minimax_bot = 1
    outside_bot = 2

    for game in range(total_games):
        global_board = GlobalBoard()

        if game < total_games // 2:
            minimax_bot = 1
            outside_bot = 2
        else:
            minimax_bot = 2
            outside_bot = 1

        current_player = 1

        while True:
            if game_over(global_board):
                if global_board.has_tic_tac_toe(minimax_bot):
                    if minimax_bot == 1:
                        minimax_wins_player_x += 1
                    else:
                        minimax_wins_player_o += 1
                elif global_board.has_tic_tac_toe(outside_bot):
                    if outside_bot == 1:
                        outside_wins_player_x += 1
                    else:
                        outside_wins_player_o += 1
                else:
                    draws += 1
                break
            
            if current_player == minimax_bot:
                result = bot_turn(global_board, minimax_bot)
                local_board, row, col =  result
                simulate_move(global_board, local_board.index, row, col, minimax_bot)
            else:
                result = outside_bot_turn(global_board, outside_bot)
                local_board, row, col =  result
                simulate_move(global_board, local_board.index, row, col, outside_bot)

            if current_player == 2:
                current_player = 1
            else:
                current_player = 2
        
    print(f"After {total_games} games:")
    print(f"Minimax wins as X: {minimax_wins_player_x}")
    print(f"Minimax wins as O: {minimax_wins_player_o}")
    print(f"Outside wins as X:  {outside_wins_player_x}")
    print(f"Outside wins as O:  {outside_wins_player_o}")
    print(f"Draws:             {draws}")
    

if __name__ == "__main__":
    total_games = 10
    bot_test(total_games, random_bot_turn)