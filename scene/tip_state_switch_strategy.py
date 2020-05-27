
from collections import namedtuple
from model.tip_model import UIState

UITimingEntry = namedtuple('UITimingEntry', ['begin_seconds', 'end_seconds', 'tip_state'])


class ShowUIStrategyFromData:
    def __init__(self, data):
        self.data = data

    def get_ui_state(self, timing):
        for entry in self.data:
            if entry.begin_seconds < timing < entry.end_seconds:
                return entry

        return None
