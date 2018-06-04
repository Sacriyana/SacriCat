#!/usr/bin/python3
#coding: utf-8

from .core import Core

import socket
import threading
import time
from sacricat.log import logging

class Challenge:
    rules = "Override it."
    win = "Override it."
    lose = "Override it."
    nbTurn = 1
    authorizedTime = 1

    def __init__(self):
        self.turn = 0
        self.challenge = ""
        self.solution = ""
        self._str = "Challenge"
        self._repr = "<Challenge>"

    def __str__(self):
        return self._str

    def __repr__(self):
        if self._repr:
            return self._repr
        else:
            return self._str

    def initTurn(self):
        pass

    def verify(self,proposition):
        if proposition == self.solution:
            return True
        return False


class AbstractServerThread(Core, threading.Thread):
    ChallengeClass = None

    def __init__(self, socket, *args, **kw ):
        threading.Thread.__init__(self)
        super().__init__(*args, **kw)
        self.challenge = self.ChallengeClass()
        self.socket = socket
        self.socket.settimeout(self.challenge.authorizedTime)
        self.kill = False
        self._logConnected('Thread created')

    def stop(self):
        self.kill = True

    def sendRules(self):
        self.send(self.challenge.rules)

    def sendWin(self):
        self.send(self.challenge.win)

    def sendLose(self):
        self.send(self.challenge.lose)

    def send(self, msg, sendPrompt=False):
        if not self.kill:
            if not super().send(msg, sendPrompt):
                self.stop()

    def recv(self, length=2048):
        if not self.kill:
            return super().recv(length)

    def play(self):
        pass

    def run(self):
        pass


class SimpleServerThread(AbstractServerThread):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def play(self):
        self.challenge.turn = 0
        while not self.kill:
            if self.challenge.turn >= self.challenge.nbTurn:
                self.sendWin()
                return True
            if self.challenge.turn < 0:
                self.sendLose()
                return False
            self.challenge.initTurn()
            self._log(repr(self.challenge),level=logging.CHALLENGE)
            self.send(self.challenge.challenge, True)
            elapsedTime = 0
            res = None
            try:
                t = time.process_time()
                playerAnswer = self.recv()
                elapsedTime = time.process_time() - t
                res = self.challenge.verify(playerAnswer)
            except Exception as e:
                self._log(str(e), level=logging.INFO)
                res = None
            if elapsedTime > self.challenge.authorizedTime or not res:
                self.sendLose()
                break
            else:
                self.challenge.turn += 1
        return False

    def run(self):
        self.sendRules()
        r = self.recv(1)
        if r:
            self.play()
        self._logDisconnected('Thread finished')


class Server:
    """ A Python server class for programming challenges inside CTFs"""
    def __init__(self, ip, port, ChallengeClass, prompt=">>> ", logLevel=logging.BASIC, ServerThreadClass=SimpleServerThread,):
        self.ip = ip
        self.port = port
        self.prompt = prompt
        ServerThreadClass.ChallengeClass = ChallengeClass
        self.ServerThreadClass = ServerThreadClass
        self.server = None
        self.logLevel = logLevel
        self.logger = logging.getLogger()
        self.logger.setLevel(self.logLevel)

    def _log(self, msg, level=logging.BASIC):
        self.logger.log(level, msg)

    def start(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self._log("[*] Server launched - %s:%s" % (self.ip, self.port))

        while True:
            self.server.listen(10)
            (clientSocket, (ip, port)) = self.server.accept()
            newThread = self.ServerThreadClass(clientSocket, ip, port, self.prompt, self.logLevel)
            newThread.start()

    def stop(self):
        self.server.close()
        self._log("[*] Server closed - %s:%s" % (self.ip, self.port))
