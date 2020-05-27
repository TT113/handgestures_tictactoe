from engine.tick_generator import RunLoopMember


class Executor(RunLoopMember):
    def __init__(self, executed_fn):
        RunLoopMember.__init__(self)
        self.executed_fn = executed_fn

    def tick(self):
        self.executed_fn()