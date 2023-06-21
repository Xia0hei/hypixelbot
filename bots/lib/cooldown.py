import time
from . import langs
from .bot_error import BotException


class Cooldown:

    def __init__(self, interval=-1.0):
        self.last_call = 0.0
        self.interval = interval

    def wait(self, cooldown=-1.0):
        time_now = time.time()
        if cooldown < 0.0:
            cooldown = self.interval
        if time_now - self.last_call >= cooldown:
            self.last_call = time_now
        else:
            raise BotException(langs.ERROR_COOLDOWN)
