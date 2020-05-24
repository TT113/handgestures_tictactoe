class AiPlayer:
    def __init__(self, input_controller, strategy, player, scene):
        self.input_controller = input_controller
        self.strategy = strategy
        self.player = player
        self.scene_controller = scene

    def update(self, scene_state):
        print("receive state update", scene_state.game_state.turn, scene_state.scene_state.cursor_position)
        if scene_state.game_state.turn == self.player:
            best_move_coordinate = self.strategy.get_best_move(scene_state.game_state)
            print("ai makes move ", best_move_coordinate)
            if best_move_coordinate is not None:
                self.scene_controller.instant_move(best_move_coordinate)