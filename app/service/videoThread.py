import threading
import time

class VideoThread(threading.Thread):
    def __init__(self, func, args=()):
        super(VideoThread, self).__init__()
        self.func = func
        self.args = args
        self.result = []

    def run(self):
        time.sleep(1)
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
