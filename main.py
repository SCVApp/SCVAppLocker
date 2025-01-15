import socketio
import time
from locker import Locker
from controller import Controller

API_URL:str = 'http://localhost:5050'


def main():
    sio = socketio.Client()

    @sio.on("openLocker", namespace="/lockers")
    def openLocker(data):
        jwtToken = data
        locker = Locker.verifyToken(jwtToken)
        return Controller.openLocker(locker)

    sio.connect(API_URL, namespaces=['/lockers'], headers={"token": Controller.TOKEN})
    sio.wait()

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(5)
