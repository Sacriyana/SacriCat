#!/usr/bin/python3
#coding: utf-8

from random import randint
import sys
sys.path.append("../..")
from sacricat.server import Server, Challenge, logging

MAX_RANDOM = 99999

class MyChallenge(Challenge):
    rules = """
    Example 1

    You have to solve 10 equations from server.
    Example : For "1 ADD 2", you send "3"

    (press touch to start)
    """
    win = "Congrats ! flag:sacricat\{win_for_example_1\}"
    lose = "Sorry, you missed the challenge. Try again :)"
    nbTurn = 10
    authorizedTime = 2

    def initTurn(self):
        a = randint(0,MAX_RANDOM)
        b = randint(0,MAX_RANDOM)
        self.challenge = "%s + %s ?" % (a, b)
        self.solution = str(a + b)
        self._str = "%s + %s = %s" % (a, b, self.solution)
        self._repr = "<Challenge(%s,%s,%s)>" % (a, b, self.solution)


server = Server("127.0.0.1", 4242, MyChallenge, prompt=">>> ", logLevel=logging.BASIC)
try:
    server.start()
except KeyboardInterrupt:
    pass
server.stop()
sys.exit(0)
