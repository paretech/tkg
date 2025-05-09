import abc
import tkinter as tk

from . import views

class ControllerBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, view: views.ViewBase):
        pass