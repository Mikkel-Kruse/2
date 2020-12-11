from move.setup_move import MovePlayer
from move.loop_make_player_move_controle import move_player_controle

move_player_controle()
move_player = MovePlayer()
player_man_movement = [0, 0]

def move_player_physics(move_player):

    if move_player.moving_right:
        player_man_movement[0] += 2
    if move_player.moving_left:
        player_man_movement[0] -= 2
    player_man_movement[1] += move_player.player_y_momentum
    move_player.player_y_momentum += 0.2
    if move_player.player_y_momentum > 3:
        move_player.player_y_momentum = 3
    return player_man_movement
