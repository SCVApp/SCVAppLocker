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
worker_thread.start()

# --- Create a single persistent Socket.IO client ---
sio = socketio.Client(
    reconnection=True,
    reconnection_attempts=0,       # infinite retries
    reconnection_delay=2,
    reconnection_delay_max=10,
    logger=False,
    engineio_logger=False,
    ssl_verify=True
)

# --- Socket event handlers ---
@sio.event(namespace='/lockers')
def connect():
    print("[SOCKET] Connected to /lockers")

@sio.event(namespace='/lockers')
def connect_error(data):
    print(f"[SOCKET] Connection failed: {data}")

@sio.event(namespace='/lockers')
def disconnect():
    print("[SOCKET] Disconnected. Reconnecting...")

@sio.on("openLocker", namespace="/lockers")
def openLocker(data):
    try:
        jwtToken = data
        locker = Locker.verifyToken(jwtToken)
        return controller.openLocker(locker)
    except Exception as e:
        print(f"[SOCKET EVENT ERROR] {e}")
        return "error"


# --- Connection watchdog ---
def connection_watchdog():
    """Keep connection alive; reconnect if dead."""
    while True:
        if not sio.connected:
            try:
                print("[WATCHDOG] Socket disconnected. Attempting reconnect...")
                sio.connect(
                    API_URL,
                    namespaces=['/lockers'],
                    headers={"token": controller.token},
                    wait_timeout=5
                )
            except Exception as e:
                print(f"[WATCHDOG ERROR] {e}")
        time.sleep(5)


def main():
    relays.setup()

    try:
        sio.connect(
            API_URL,
            namespaces=['/lockers'],
            headers={"token": controller.token},
            wait_timeout=10
        )
    except Exception as e:
        print(f"[SOCKET INIT ERROR] {e}")

    # Start watchdog to ensure reconnection
    threading.Thread(target=connection_watchdog, daemon=True).start()

    # Keep main thread alive
    while True:
        time.sleep(60)


if __name__ == '__main__':
    main()
