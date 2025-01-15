from locker import Locker
class Controller:

    TOKEN="dhsjkhdsj"

    @staticmethod
    def openLocker(locker: Locker | None)->str:
        if locker is None:
            return "error"

        token = locker.controllerToken
        if token != Controller.TOKEN:
            return "error"

        return "ok"
