import rumps
from enum import Enum, auto

from constants.time import WORK_SECONDS, BREAK_SECONDS
from utils.notification import notify_break, notify_break_done


class State(Enum):
    IDLE = auto()         # not started yet
    WORKING = auto()      # work countdown running
    PAUSED = auto()       # work countdown paused
    BREAK_ALERT = auto()  # work done, blinking, waiting for user to start break
    BREAKING = auto()     # break in progress, counting up
    BREAK_DONE = auto()   # >= 20s break done, waiting for user to start next cycle


class EyesTimerApp(rumps.App):
    def __init__(self):
        super().__init__("👁 20:00")
        self._state = State.IDLE
        self._work_remaining = WORK_SECONDS
        self._break_elapsed = 0
        self._blink = False

        self._action_btn = rumps.MenuItem("▶ Start", callback=self.on_action)
        self._reset_btn = rumps.MenuItem("Reset", callback=self.reset)
        self.menu = [self._action_btn, self._reset_btn]

    @rumps.timer(1)
    def tick(self, _):
        if self._state == State.WORKING:
            self._work_remaining -= 1
            self._refresh_title()
            if self._work_remaining <= 0:
                self._enter_break_alert()

        elif self._state == State.BREAK_ALERT:
            self._blink = not self._blink
            self.title = "🔴 LOOK AWAY!" if self._blink else "  LOOK AWAY!"

        elif self._state in (State.BREAKING, State.BREAK_DONE):
            self._break_elapsed += 1
            mins, secs = divmod(self._break_elapsed, 60)
            self.title = f"🌿 {mins:02d}:{secs:02d}"
            if self._state == State.BREAKING and self._break_elapsed == BREAK_SECONDS:
                self._enter_break_done()

    def on_action(self, _):
        if self._state == State.IDLE:
            self._start_work()
        elif self._state == State.WORKING:
            self._pause()
        elif self._state == State.PAUSED:
            self._resume()
        elif self._state == State.BREAK_ALERT:
            self._start_break()
        elif self._state in (State.BREAKING, State.BREAK_DONE):
            self._start_work()

    def reset(self, _):
        self._state = State.IDLE
        self._work_remaining = WORK_SECONDS
        self._break_elapsed = 0
        self._blink = False
        self._action_btn.title = "▶ Start"
        self._refresh_title()

    def _start_work(self):
        self._state = State.WORKING
        self._work_remaining = WORK_SECONDS
        self._break_elapsed = 0
        self._action_btn.title = "⏸ Pause"
        self._refresh_title()

    def _pause(self):
        self._state = State.PAUSED
        self._action_btn.title = "▶ Resume"

    def _resume(self):
        self._state = State.WORKING
        self._action_btn.title = "⏸ Pause"

    def _enter_break_alert(self):
        self._state = State.BREAK_ALERT
        self._action_btn.title = "👁 Start Break"
        notify_break()

    def _start_break(self):
        self._state = State.BREAKING
        self._break_elapsed = 0
        self._action_btn.title = "✓ Done Looking Away"

    def _enter_break_done(self):
        self._state = State.BREAK_DONE
        self._action_btn.title = "▶ Start Working"
        notify_break_done()

    def _refresh_title(self):
        mins, secs = divmod(self._work_remaining, 60)
        self.title = f"👁 {mins:02d}:{secs:02d}"
