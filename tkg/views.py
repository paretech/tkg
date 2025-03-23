from . import widgets


class Main(widgets.MainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
