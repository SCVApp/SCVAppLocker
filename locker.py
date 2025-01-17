import jwt
import time

class Locker:
    controllerToken:str = None
    lockerId:str = None

    PUBLIC_KEY:str = "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAkPdF2W7SpSTm5oaaMPynOdiBB2L62UY+bX+prOZp4yWiDk7/Bo2NPbZcVAUT+fhp417zfPmdkxHaO5wqcQ926EMXmWyM/DHxPm/O/le/h+gY/TOAyd3zY3nu5QylINf2PApavMkN8jEOQ3YglwQdGmjXErDKmX67JSCADybbOoNkELthinW1tza8627KAj9oDEtq5dvrBXQvMPFat2XiVis34Kay0Sk12PNRrxPv0FXbA1wlwNlytAnAfnrGYjslRVwI1PMRSOamgpVZwUs3ujKu0hM0+RWQb2U8ndlwwHQEGK0Xl98CSdySI9rFdYulYnmvtARS/hvuo8Y70jIP1+tRk6+Q101HKKm9N3AAzp1gKkCXOypqSiW3+sAV637biNnUS4RK4L6CX1FoEkkUWJBqtH2ExdYBtZahfuaAfyfZ3qg+/+mMf0k2FCEnErOxKoxXZwNfW7KBHW+TYFfxiZX8rzQ6KXSefKLJDeU+nJoKTmlp6gIKMt2epN0UmAGb97Ed1YeekETrzCitq+Rau+4/TRXLCqjqGcCkP2BmyhuwQ9bSt/DoL9IWDfmWHjtkJ95GORjBTXNDgGZawcjBNKpbNicxQ6hMAmpzyMwABlsMv6pAemY+LzKYKnr4I8LjWDdbRfNbjMq5EkskrnWrwPeDtKs14VuM9q3ZwYQWOpMCAwEAAQ==\n-----END PUBLIC KEY-----"

    def __init__(self, controllerToken:str, lockerId:str):
        self.controllerToken = controllerToken
        self.lockerId = lockerId

    @staticmethod
    def verifyToken(token:str) -> "Locker | None":
        try:
            decoded = jwt.decode(token,Locker.PUBLIC_KEY, algorithms=["RS256"])
            exp = decoded["exp"]
            lockerId = decoded["lockerId"]
            controllerToken = decoded["controllerToken"]

            if exp < time.time():
                return None

            return Locker(controllerToken, lockerId)
        except Exception:
            return None
