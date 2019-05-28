#!/usr/bin/python3
#coding: utf-8

from .core import Core
from .log import logging
import socket
import re

__all__ = ['Server','logging']

class Server(Core):
    def __init__(self, ip, port, prompt=">>> ", timeout=5, logLevel=logging.BASIC):
        super(Server, self).__init__(ip, port, prompt, logLevel)
        self.timeout = timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.socket.settimeout(timeout)
        self._logConnected()

    def sendLine(self, msg = None):
        if not msg:
            msg = '\n'
        if msg[-1] != '\n':
            msg += '\n'
        self.send(msg)

    def _clean(self, msg, clean):
        if type(clean) == int:
            msg = msg[:-clean]
        else:
            if type(clean) != str:
                clean = self.prompt
            if msg.endswith(clean):
                msg = msg[:-len(clean)].strip()
        return msg

    def recv(self, length, clean=None):
        serverRecv = ''
        try:
            serverRecv = super().recv(length)
        except Exception as e:
            self._log(str(e), level=logging.ERROR)
        if clean:
            serverRecv = self._clean(serverRecv, clean)
        return serverRecv

    def recvUntil(self, until = None, clean = None):
        if not until:
            until = self.prompt
        if not until:
            self._log("until (and your prompt parameter) is empty.", level=logging.ERROR)
            return None
        serverRecv = ''
        while until not in serverRecv:
            recv = None
            try:
                recv = super().recv()
            except Exception as e:
                self._log(str(e), level=logging.ERROR)
            if recv:
                serverRecv += recv
            else:
                break
        if clean:
            serverRecv = self._clean(serverRecv, clean)
        return serverRecv

    def recvUntilRegex(self, regex, clean = None):
        regex = re.compile(regex)
        serverRecv = ''
        while not regex.search(serverRecv):
            recv = None
            try:
                recv = super().recv()
            except Exception as e:
                self._log(str(e), level=logging.ERROR)
            if recv:
                serverRecv += recv
            else:
                break
        if clean:
            serverRecv = self._clean(serverRecv, clean)
        return serverRecv
