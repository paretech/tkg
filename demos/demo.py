import queue
import threading
import tkinter as tk
from tkinter import ttk

import tkg


class TaskController:
    def __init__(self, root):
        self.model = None
        self.view = TaskView(parent=root, controller=self)
        self.progress_queue = queue.Queue()
        self.thread = None
        self._poll_queue()

    def start_task(self):
        if self.thread and self.thread.is_alive():
            return  # avoid double start
        self.thread = threading.Thread(
            target=self.model.run_task, args=(self.progress_queue,), daemon=True
        )
        self.thread.start()

    def stop_task(self):
        self.model.stop()

    def _poll_queue(self):
        try:
            while True:
                value = self.progress_queue.get_nowait()
                self.view.update_progress(value)
        except queue.Empty:
            pass
        self.view.after(100, self._poll_queue)


class TaskView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(padx=10, pady=10)

        self.start_button = tk.Button(
            self, text="Start", command=self.controller.start_task
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            self, text="Stop", command=self.controller.stop_task
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=200, mode="determinate"
        )
        self.progress.pack(side=tk.LEFT, padx=5)

    def update_progress(self, value):
        self.progress["value"] = value


class MainView(tkg.widgets.MainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller


class Controller:
    def __init__(self):
        self.model = None
        self.main_view = MainView(self)

        # Register clean shutdown method
        self.main_view.on_close(self.close)

        self.task_controller = TaskController(self.main_view)

        self.main_view.run()

    def close(self):
        print(f"{self.__class__.__name__}.close")


if __name__ == "__main__":
    app = Controller()

    True  # No op for setting breakpoint
