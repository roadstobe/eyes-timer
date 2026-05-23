import subprocess

SOUNDS_DIR = "/System/Library/Sounds"


def _notify(message: str):
    script = f'display notification "{message}" with title "Eyes Timer"'
    subprocess.run(['osascript', '-e', script])


def _play(sound: str):
    subprocess.Popen(['afplay', f'{SOUNDS_DIR}/{sound}'])


def notify_break():
    _play("Glass.aiff")
    _notify("Time for a break! Look 20 feet away.")


def notify_break_done():
    _play("Ping.aiff")
    _notify("20 seconds done! Start working when ready.")
