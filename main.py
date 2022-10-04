from boards import board
import random

from functions import play_log

if __name__ == '__main__':

    p1 = board.players[0]
    p2 = board.players[1]
    p3 = board.players[2]
    p4 = board.players[3]
    interaction = 1
    while p1.cubes > 0 or p2.cubes > 0 or p3.cubes > 0 or p4.cubes > 0:
        print("[ROUND " + str(interaction) + "]")
        if (p1.cubes > 0):
            p1_possibilities = board.check_movement_possibilities(p1)
            if (len(p1_possibilities) > 0):
                chosen_coord = random.sample(p1_possibilities, 1)[0]
                board.mov_player(from_coord=chosen_coord["from_coord"],
                                 target_coord=chosen_coord["target_coord"], start_coord=p1.start_point)
                board.plot_board(interaction, p1.name)
            else:
                p1.cubes = 0
        if (p2.cubes > 0):
            p2_possibilities = board.check_movement_possibilities(p2)
            if (len(p2_possibilities) > 0):
                chosen_coord = random.sample(p2_possibilities, 1)[0]
                board.mov_player(from_coord=chosen_coord["from_coord"],
                                 target_coord=chosen_coord["target_coord"], start_coord=p2.start_point)
                board.plot_board(interaction, p2.name)
            else:
                p2.cubes = 0
        if (p3.cubes > 0):
            p3_possibilities = board.check_movement_possibilities(p3)
            if (len(p3_possibilities) > 0):
                chosen_coord = random.sample(p3_possibilities, 1)[0]
                board.mov_player(from_coord=chosen_coord["from_coord"],
                                 target_coord=chosen_coord["target_coord"], start_coord=p3.start_point)
                board.plot_board(interaction, p3.name)
            else:
                p3.cubes = 0
        if (p4.cubes > 0):
            p4_possibilities = board.check_movement_possibilities(p4)
            if (len(p4_possibilities) > 0):
                chosen_coord = random.sample(p4_possibilities, 1)[0]
                board.mov_player(from_coord=chosen_coord["from_coord"],
                                 target_coord=chosen_coord["target_coord"], start_coord=p4.start_point)
                board.plot_board(interaction, p4.name)
            else:
                p4.cubes = 0

        interaction += 1
