"""Log Viewer Assembly"""


import tkinter as tk
import tkinter.scrolledtext
import queue

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
        controller=LogViewerController()
        view=LogViewerView()
        model=LogViewerModel()
        return cls(controller=controller, view=view, model=model)


class LogViewerController():
    def __init__(self, )


class LogViewerView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent)
        self.controller = controller

    def create_widgets(self):
        self.scrolled_text = tkinter.scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.scrolled_text.pack(expand=True, fill=tk.BOTH)

    def _append(self, message: str):
        self.scrolled_text.insert(tk.END, f"{message}\n")
        self.scrolled_text.see(tk.END)

    def append(self, message: str, delay=0):
        self.after(delay, self._append, message)


class LogViewerModel:
    pass
