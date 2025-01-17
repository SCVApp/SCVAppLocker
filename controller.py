from locker import Locker
import queue

class Controller:
    token:str = ""
    queue = queue.Queue()

    def __init__(self, token:str):
        self.token = token


    def openLocker(self, locker: Locker | None)->str:
        if locker is None:
            return "error"

        token = locker.controllerToken
        if token != self.token:
            return "error"

        self.queue.put((locker.lockerId, "open"))

        return "ok"
