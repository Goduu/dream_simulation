import copy
from boards_data import board
import random
from movement_functions import check_movement_possibilities, mov_player, mov_player_with_skill
import numpy as np
from player import PlayerSkillType

should_print = True



if __name__ == '__main__':
    scores = {}
    p1 = board.players[0]
    p2 = board.players[1]
    p3 = board.players[2]
    p4 = board.players[3]

    players = [p1, p2, p3, p4]

    for player in players:
        scores[player.name] = []

    for rounds in range(1000):
        round_board = copy.deepcopy(board)
        p1 = round_board.players[0]
        p2 = round_board.players[1]
        p3 = round_board.players[2]
        p4 = round_board.players[3]

        players = [p1, p2, p3, p4]


        for round in range(3):
            turn = 1
            while p1.cubes > 0 or p2.cubes > 0 or p3.cubes > 0 or p4.cubes > 0:
                if should_print:
                    print("[ROUND " + str(round) + "]")
                for player in players:
                    if should_print:
                        print("[TURN " + str(round) + "] - Player ", player.name)
                        round_board.plot_board(round,turn, player.name)
                    if (player.cubes > 0):
                        player_possibilities = check_movement_possibilities(
                            round_board,
                            player)

                        if (len(player_possibilities) > 0):
                            chosen_move = random.sample(
                                player_possibilities, 1)[0]
                            if (len(chosen_move["with_skill"]) > 0):
                                chosen_skill = random.sample(
                                    chosen_move["with_skill"], 1)[0]
                                mov_player_with_skill(round_board, from_hex=chosen_move["from_hex"],
                                                      target_hex=chosen_move["target_hex"], start_hex=player.start_point, skill=chosen_skill)
                            else:
                                mov_player(round_board, from_hex=chosen_move["from_hex"],
                                           target_hex=chosen_move["target_hex"], start_hex=player.start_point)

                            

                        else:
                            player.cubes = 0
                if (turn > 30):
                    round_board.plot_board(1,10000, player.name)
                if(turn > 31):
                    break
                turn += 1

            for player in players:
                player_score = player.get_round_score()
                # if should_print:
                #     print("[SCORE] ", player.name,
                #           " round score: ", player_score)

            round_board.new_round()
        for player in players:
            scores[player.name].append(player.score.accumulator)

    for player in players:
        print(player.name, np.mean(scores[player.name]))
