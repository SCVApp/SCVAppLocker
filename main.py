import socketio
import time
import threading
import relays
from locker import Locker
from controller import Controller

API_URL = 'https://backend.app.scv.si'
controller = Controller("omaricetoken")


def controll_relays(locker_id: str, action: str):
    relays.board_controller(locker_id, action)


def worker():
    while True:
        locker_id, action = controller.queue.get()
        try:
            controll_relays(locker_id, action)
            if action == "open":
                time.sleep(0.5)
                controll_relays(locker_id, "close")
        except Exception as e:
            print(f"[WORKER ERROR] {e}")
        finally:
            controller.queue.task_done()


worker_thread = threading.Thread(target=worker, daemon=True)


def create_sio_client():
    sio = socketio.Client(
        reconnection=True,
        reconnection_attempts=0,  # infinite attempts
        reconnection_delay=2,
        reconnection_delay_max=10,
        logger=True,
        engineio_logger=True
    )

    @sio.event(namespace='/lockers')
    def connect():
        print("[SOCKET] Connected to /lockers namespace.")

    @sio.event(namespace='/lockers')
    def connect_error(data):
        print(f"[SOCKET] Connection failed: {data}")

    @sio.event(namespace='/lockers')
    def disconnect():
        print("[SOCKET] Disconnected. Will attempt reconnection...")

    @sio.on("openLocker", namespace="/lockers")
    def openLocker(data):
        try:
            jwtToken = data
            locker = Locker.verifyToken(jwtToken)
            return controller.openLocker(locker)
        except Exception as e:
            print(f"[SOCKET EVENT ERROR] {e}")
            return "error"
    return sio


def main():
    relays.setup()
    sio = create_sio_client()

    while True:
        try:
            print("[SOCKET] Connecting...")
            sio.connect(
                API_URL,
                namespaces=['/lockers'],
                headers={"token": controller.token},
                wait_timeout=10
            )
            sio.wait()
        except Exception as e:
            print(f"[SOCKET ERROR] {e}")
            print("[SOCKET] Retrying connection in 5s...")
            time.sleep(5)


if __name__ == '__main__':
    worker_thread.start()
    main()
