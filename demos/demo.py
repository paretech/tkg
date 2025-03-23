import queue
import threading
import time
import tkinter as tk
from tkinter import ttk

import tkg


class TaskModel:
    def __init__(self):
        self.progress = 0
        self._stop_event = threading.Event()

    def run_task(self, progress_queue):
        self._stop_event.clear()
        for i in range(101):
            if self._stop_event.is_set():
                break
            self.progress = i
            progress_queue.put(i)
            time.sleep(0.05)  # simulate work

    def stop(self):
        self._stop_event.set()


class TaskController:
    def __init__(self, root):
        self.model = TaskModel()
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


class Controller:
    def __init__(self):
        self.model = None
        self.view = tkg.views.Main(self)

        # Register clean shutdown method
        self.view.on_close(self.close)

        self.task = TaskController(self.view)

        self.view.run()

    def close(self):
        # Demonstration of `view.on_close` callback
        print(f"{self.__class__.__name__}.close")


if __name__ == "__main__":
    app = Controller()

    True  # No op for setting breakpoint
