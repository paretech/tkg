import abc
import tkinter as tk

from . import widgets
from . import controllers

class ViewBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, parent: tk.Misc, controller: ):
        """Must accept a tkinter-compatible parent widget."""
        pass

class Main(widgets.MainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
