import socketio
import time
import threading
import relays
from locker import Locker
from controller import Controller

API_URL:str = 'https://backend.app.scv.si'

controller = Controller("omaricetoken")

def controll_relays(locker_id:str, action:str):
    relays.board_controller(locker_id, action)

def worker():
    while True:
        locker_id, action = controller.queue.get()
        controll_relays(locker_id, action)
        if action == "open":
            time.sleep(1)
            controll_relays(locker_id, "close")
        controller.queue.task_done()

worker_thread = threading.Thread(target=worker, daemon=True)

def main():
    relays.setup()
    sio = socketio.Client()

    @sio.on("openLocker", namespace="/lockers")
    def openLocker(data):
        jwtToken = data
        locker = Locker.verifyToken(jwtToken)
        return controller.openLocker(locker)

    sio.connect(API_URL, namespaces=['/lockers'], headers={"token": controller.token})
    sio.wait()

if __name__ == '__main__':
    worker_thread.start()
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(5)
