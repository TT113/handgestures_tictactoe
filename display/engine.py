import time

from model.input import Input


class Engine:
    def __init__(self, scene, renderer):
        self.scene = scene
        self.renderer = renderer
        # test cell occupied
        # self.actions = [Input.ENTER, Input.ENTER]

        #test move cursor
        # self.actions = [Input.ENTER, Input.RIGHT_ARROW, Input.ENTER]

        #test win X
        self.actions = [Input.ENTER, Input.RIGHT_ARROW, Input.ENTER, Input.BOTTOM_ARROW, Input.ENTER, Input.RIGHT_ARROW, Input.ENTER, Input.BOTTOM_ARROW, Input.ENTER]

    def run_loop(self):
        while True:
            time.sleep(0.2)
            model = self.scene.get_render_model()
            self.renderer.render(model)
            if len(self.actions) > 0:
                self.scene.receive_input(self.actions[0])
                self.actions = self.actions[1:]