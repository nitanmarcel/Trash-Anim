import threading
import time

from functools import wraps
from trashguy import TrashGuy


class Anim:
    def __init__(self, text: str = 'Loading', speed: int = 0.2):
        self.text: str = text
        self.speed: int = speed

        self.thread: threading.Thread = threading.Thread()
        self.trash_anim: TrashGuy = TrashGuy(self.text)
        self.frame_list: list = list(self.trash_anim)

        self.animate: bool = True

    def _start(self):
        for frame in self.frame_list:
            if self.animate:
                print(frame, end='', flush=True)
                time.sleep(self.speed)
                print(f'\x1b[1K\x1b[{len(frame) ** 2}D',
                      end='')
                self.frame_list.pop(0)
            else:
                continue
        return

    def _get_last_frame(self):
        return self.frame_list[0] if len(self.frame_list) != 0 else []

    def start(self):
        self.thread = threading.Thread(target=self._start)
        self.thread.start()
        return

    def stop(self):
        self.animate = False
        return

def animate(text: str = 'LOADING', speed: int = 0.02):
    """Decorator for adding trashguy animation to long running
    functions.
    Args:
        text (str): String reference to trash items
        speed (float): Number of seconds each cycle of animation.

    Examples:
        import trash_anim

        @trash.anim.animate(text='LOADING', speed=1)
        def test():
            import time
            time.sleep(10)
            print('\nDone')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            anim = Anim(text=text, speed=speed)
            anim.start()
            try:
                ret = func(*args, **kwargs)
            finally:
                anim.stop()
            return ret
        return wrapper
    return decorator




