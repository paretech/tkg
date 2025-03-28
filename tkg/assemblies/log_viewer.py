class LogViewerAssy:
    def __init__(
        self,
        controller: "LogViewerController",
        view: "LogViewerView",
        model: "LogViewerModel",
    ):
        self.model = model
        self.controller = controller
        self.view = view

    @classmethod
    def from_defaults(cls):
        return cls(
            controller=LogViewerController(),
            view=LogViewerView(),
            model=LogViewerModel(),
        )


class LogViewerController:
    pass


class LogViewerView:
    pass


class LogViewerModel:
    pass
