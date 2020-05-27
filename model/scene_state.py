class SceneState:
    def __init__(self,
                 cursor_position,
                 tip_timing_entry,
                 game_begin_timestamp,
                 winner):
        self.cursor_position = cursor_position
        self.ui_timing_entry = tip_timing_entry
        self.game_begin_timestamp = game_begin_timestamp
        self.winner = winner
