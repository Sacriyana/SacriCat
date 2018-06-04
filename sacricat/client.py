#!/usr/bin/python3
#coding: utf-8

from .core import Core
from .log import logging
import socket

class Server(Core):
    def __init__(self, ip, port, prompt=">>> ", timeout=5, logLevel=logging.BASIC):
        super(Server, self).__init__(ip, port, prompt, logLevel)
        self.rules = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self._logConnected()
        self.socket.settimeout(timeout)

    def getRules(self):
        if not self.rules:
            self.rules = self.recv()
        return self.rules

    def sendKey(self, key=None):
        if not key:
            self.send('\n')
        else:
            self.send(key[0])

    def recv(self, clean=False):
        serverRecv = super().recv()
        while self.prompt not in serverRecv:
            try:
                recv = super().recv()
                if recv == '':
                    self._log("recv is empty", level=logging.INFO)
                    break
                serverRecv += recv
            except Exception as e:
                self._log(str(e), level=logging.INFO)
                break
        if clean:
            if serverRecv.endswith(self.prompt):
                serverRecv = serverRecv[:-len(self.prompt)]
            serverRecv = serverRecv.strip()
        return serverRecv
