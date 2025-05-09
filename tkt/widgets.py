"""
Resources
- https://docs.python.org/3/library/tkinter.html
- https://tkdocs.com/
- https://tkdocs.com/shipman/
- https://www.tcl-lang.org/man/tcl8.6/TkCmd/contents.htm
- https://github.com/TomSchimansky/CustomTkinter
- https://stackoverflow.com/users/7432/bryan-oakley

"""

import tkinter as tk
from tkinter import ttk  # noqa: F401


class MainWindow(tk.Tk):
    def __init__(self, *args, title: str = None, **kwargs):
        super().__init__()

        # Do not show GUI during configuration and building of widgets as to
        # hide rendering artifacts from user.
        self.hide()

        self.configure(title)

    def configure(self, title):
        """Configure window parameters"""

        self.title(title)

    def hide(self):
        """Hide window

        Commonly used in conjunction with `.show()` to hide window until
        configuration and initial rendering are complete such that visible
        artifacts are not shown to user.

        Per the Tcl/Tk 8.6 docs,

            Arranges for window to be withdrawn from the screen. This causes the
            window to be unmapped and forgotten about by the window manager. If
            the window has never been mapped, then this command causes the
            window to be mapped in the withdrawn state. Not all window managers
            appear to know how to handle windows that are mapped in the
            withdrawn state. Note that it sometimes seems to be necessary to
            withdraw a window and then re-map it (e.g. with wm deiconify) to get
            some window managers to pay attention to changes in window
            attributes such as group.
        """
        self.withdraw()

    def show(self):
        """Show window

        Commonly used in conjunction with `.hide()` to hide window until
        configuration and initial rendering are complete such that visible
        artifacts are not shown to user.

        Per the Tcl/Tk docs,

            On Windows it will raise this widget and give it the focus.
        """
        self.after(0, self.deiconify)

    def update(self):
        """Force changes to happen

        If some changes are not taking effect, this method may be useful as
        workaround for bugs that affect the operation of window manager.
        """

        self.hide()

    def elevate(self):
        """Needed so the window pops up on top on Windows..."""

        self.iconify()
        self.update()
        self.deiconify()

    def run(self):
        try:
            self.show()
            self.mainloop()
        except KeyboardInterrupt:
            self.destroy()

    def on_close(self, callback):
        """Register a callable to be executed when widget destroyed

        Often used by controller to register closing actions. Callback used
        instead of other mechanisms so that Tk related operations are purely in
        view module.

        Callback will be called if user clicks exit widget from graphical
        interface or when sending SIGINT (e.g., "ctrl + c") from command line
        interface.
        """

        # Keeping this logic in widgets prevents controllers from having to know
        # anything about Tkinter.

        # Capture `self` and `callback` via closure for future use
        def _close(event=None):
            # Without this guard, the callback would be called once for every
            # widget as it is destroyed.
            if self == event.widget:
                callback()

        self.bind(f"<{tk.EventType.Destroy.name}>", _close)
