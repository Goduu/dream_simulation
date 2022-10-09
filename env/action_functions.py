from classes import Player, PlayerSkillType,Hex


def use_reset_skill(from_player: Player, target_player: Player, target_player_hex: Hex):
    from_player.use_skill(PlayerSkillType.RESET)
    reset_player(player=target_player, hex=target_player_hex)


def reset_player(player: Player, hex: Hex):
    hex.player_occupation = []
    player.occupied_hexagons.remove(hex)
    player.occupied_hexagons.append(player.start_point)
    player.start_point.player_occupation.append(player)
    player.cubes += 1
    player.partialScore.sub_score(targetHex=hex)





