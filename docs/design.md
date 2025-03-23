# Startup and Shutdown 
One of the first things I tried to do when creating my first Tkinter GUI
application was to ensure that the Window starts and stops from a variety of use
cases. This turned out to be a little more difficult than expected.


There are a couple of scenarios that need to be considered for clean shutdown of
application.

- User clicks graphical interface to close (e.g. "X" in title bar)
- User launched from command line and hits "ctrl+c"

There are also a couple of ways to accomplish part of these. Care must be taken
in how these are applied as there is risk of double calling or not calling at
all under certain circumstances.

- Binding a "<Destroy>" event to a callable
- Register with TK Window Manager (WM) Protocol (e.g.,
    `root.protocol("WM_DELETE_WINDOW", <callable>)`). See
    https://www.tcl-lang.org/man/tcl8.6/TkCmd/wm.htm for more details.
- Try/finally block around tk.mainloop
- Register Signal handler, (e.g., `signal.signal(signal.SIGINT,
    self.handle_sigint)`)
- Use the `atexit` package

Per https://www.tcl-lang.org/man/tcl8.6/TkCmd/destroy.htm, "This [destroy]
command deletes the windows given by the window arguments, plus all of their
descendants. If a window “.” is deleted then all windows will be destroyed and
the application will (normally) exit. The windows are destroyed in order, and if
an error occurs in destroying a window the command aborts without destroying the
remaining windows."

If the Tkinter front end is not doing anything such that it is waiting for next
event, then known of the above methods will do anyting until the main thread
stops blocking. Is scenario is observable on Windows OS when user launches GUI
from command window (CMD), the app opens, user changes focus back to the CMD
window and issues a "ctrl+c". Assuming that the correct signal handler or
exception handlers are in place, nothing will happen until the Tkinter event
loop resumes. If nothing is happening in the Window, this might not be until the
usr changes focus back to the Tkinter GUI. Once focus is back on GUI or some
other mechanism triggers event loop, then window will close.