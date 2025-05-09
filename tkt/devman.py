import queue
import threading
from enum import IntEnum
from typing import Callable, Optional


class LockPriority(IntEnum):
    """Defines priority levels for acquiring a device lock."""

    LOW = 1  # Manual control panel
    MEDIUM = 2  # Background monitoring/logging
    HIGH = 3  # Test sequence (should preempt manual control)
    CRITICAL = 4  # Emergency override (diagnostics, firmware updates, etc.)


class ConnectionProxy:
    """A thread-safe proxy that manages device access with priority queueing."""

    _instances = {}  # Tracks active connections per device
    _global_lock = threading.Lock()  # Ensures single instance per device

    def __new__(cls, device_id, interface_driver):
        """Ensure a single instance per device_id."""
        with cls._global_lock:
            if device_id not in cls._instances:
                cls._instances[device_id] = super(ConnectionProxy, cls).__new__(cls)
                cls._instances[device_id]._init_proxy(device_id, interface_driver)
        return cls._instances[device_id]

    def _init_proxy(self, device_id, interface_driver):
        """Initialize the proxy settings."""
        self.device_id = device_id
        self.interface_driver = interface_driver
        self.locked = False
        self.priority: Optional[LockPriority] = None
        self.lock_owner: Optional[str] = None
        self.lock_lost_callback: Optional[Callable[[LockPriority], None]] = (
            None  # Optional GUI callback
        )
        self._lock = threading.Lock()

        # Queue of waiting requests (priority, requester, event)
        self.wait_queue = queue.PriorityQueue()

    def connect(self):
        """Forward connect calls to the underlying interface driver."""
        return self.interface_driver.connect()

    def close(self):
        """Safely release connection when done."""
        with self._lock:
            self.interface_driver.close()
            with ConnectionProxy._global_lock:
                del ConnectionProxy._instances[self.device_id]

    def acquire(self, priority: LockPriority, requester: str):
        """Attempts to acquire a lock at the given priority level."""
        with self._lock:
            if self.locked:
                if priority > self.priority:
                    print(
                        f"[PRIORITY] {requester} (priority {priority}) preempted {self.lock_owner} (priority {self.priority})."
                    )
                    self.force_release()
                else:
                    print(
                        f"[QUEUE] {requester} (priority {priority}) added to wait queue for {self.device_id}."
                    )
                    event = threading.Event()
                    self.wait_queue.put(
                        (-priority, requester, event)
                    )  # Use -priority to get highest first
                    return event.wait()  # Block until event is set

            self.locked = True
            self.priority = priority
            self.lock_owner = requester
            print(
                f"[INFO] {self.device_id} locked by {requester} at priority {priority}."
            )

    def force_release(self):
        """Forcefully releases the device and assigns it to the next in queue."""
        with self._lock:
            if self.lock_lost_callback:
                threading.Thread(
                    target=self.lock_lost_callback, args=(self.priority,)
                ).start()

            print(
                f"[FORCED RELEASE] {self.device_id} released from {self.lock_owner} (priority {self.priority})."
            )
            self.locked = False
            self.priority = None
            self.lock_owner = None

            self.check_queue()  # Assign to next waiting requester

    def release(self, priority: LockPriority, requester: str):
        """Releases the lock if the requester is the current owner."""
        with self._lock:
            if self.priority != priority or self.lock_owner != requester:
                raise RuntimeError(
                    f"{requester} cannot release {self.device_id} (held by {self.lock_owner} at priority {self.priority})."
                )

            print(
                f"[INFO] {self.device_id} released from {requester} (priority {priority})."
            )
            self.locked = False
            self.priority = None
            self.lock_owner = None

            self.check_queue()  # Assign to next waiting requester

    def check_queue(self):
        """Check the wait queue and assign the device to the next waiting requester."""
        if not self.wait_queue.empty():
            _, requester, event = self.wait_queue.get()
            print(
                f"[QUEUE] {requester} is now acquiring {self.device_id} from the queue."
            )
            self.locked = True
            self.lock_owner = requester
            event.set()  # Wake up the waiting requester


import threading
from tkinter import messagebox


class DeviceControlPanel:
    """GUI panel for manually controlling a device."""

    def __init__(self, device_id, root):
        self.device_id = device_id
        self.device = managed_devices.get(self.device_id)
        self.active = False
        self.root = root

        # Register callback for when lock is lost
        if self.device:
            self.device.lock_lost_callback = self.on_lock_lost

    def open(self):
        """Request access to the device for manual control at LOW priority."""
        requester = f"GUI-{self.device_id}"
        try:
            event = self.device.acquire(LockPriority.LOW, requester)
            if event:
                print(f"[INFO] {self.device_id} waiting in queue for manual control.")
                event.wait()  # Wait until it’s released by a higher priority task

            self.active = True
            print(
                f"[INFO] {self.device_id} acquired by GUI for manual control (LOW priority)."
            )
        except RuntimeError as e:
            messagebox.showerror("Device Lock Error", str(e))

    def send_command(self, command):
        """Send a command to the device if it's still locked."""
        if self.active:
            self.device.send(command)
        else:
            messagebox.showwarning(
                "Control Lost",
                f"{self.device_id} is no longer available for manual control.",
            )

    def on_lock_lost(self, previous_priority):
        """Callback when control is forcibly lost."""
        self.active = False
        self.root.after(
            0,
            lambda: messagebox.showinfo(
                "Lock Lost", f"{self.device_id} is now controlled by a test sequence."
            ),
        )

    def close(self):
        """Release the device when done."""
        if self.active:
            self.device.release(LockPriority.LOW, f"GUI-{self.device_id}")
            self.active = False
            print(f"[INFO] {self.device_id} released from manual control.")
