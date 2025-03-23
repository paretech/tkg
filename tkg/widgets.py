"""
Resources
- https://docs.python.org/3/library/tkinter.html
- https://tkdocs.com/
- https://tkdocs.com/shipman/
- https://www.tcl-lang.org/man/tcl8.6/TkCmd/contents.htm
- https://github.com/TomSchimansky/CustomTkinter
"""

import signal
import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self, *args, title: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide()

        self.title(title)

    def run(self):
        signal.signal(signal.SIGINT, self.close)
        # Set SIGINT signal handler
        self.show()
        self.mainloop()

    def close(self, event=None, signal=None, frame=None):
        pass

    def hide(self):
        self.withdraw()

    def show(self):
        self.after(0, self.deiconify)
