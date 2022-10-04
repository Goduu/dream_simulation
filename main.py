from boards import board
import random
from functions import play_log

if __name__ == '__main__':

    p1 = board.players[0]
    p2 = board.players[1]
    p3 = board.players[2]
    p4 = board.players[3]

    players = [p1, p2, p3, p4]

    should_print = False

    interaction = 1
    while p1.cubes > 0 or p2.cubes > 0 or p3.cubes > 0 or p4.cubes > 0:
        print("[ROUND " + str(interaction) + "]")
        for player in players: 
            if(player.cubes >0):
                player_possibilities = board.check_movement_possibilities(player)
                if (len(player_possibilities) > 0):
                    chosen_coord = random.sample(player_possibilities, 1)[0]
                    board.mov_player(from_coord=chosen_coord["from_coord"],
                                    target_coord=chosen_coord["target_coord"], start_hexagon=player.start_point)
                    if should_print == True: board.plot_board(interaction, player.name) 
                else:
                    player.cubes = 0    
        interaction += 1
    board.plot_board(10000, player.name)

    for player in players:
        print("[SCORE] ", player.name, " final score: ", player.get_round_score())

