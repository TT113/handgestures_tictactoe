class SceneState:
    def __init__(self,
                 cursor_position,
                 should_render_start_tip,
                 should_render_calibration_tip,
                 game_begin_timestamp,
                 winner):
        self.cursor_position = cursor_position
        self.should_render_start_tip = should_render_start_tip
        self.game_begin_timestamp = game_begin_timestamp
        self.winner = winner
        self.should_render_calibration_tip = should_render_calibration_tip
