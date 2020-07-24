#!/usr/bin/python3
#coding: utf-8

from .core import Core
from .log import logging
import socket
import re

__all__ = ['Server','logging']

class Server(Core):
    def __init__(self, ip, port, prompt=">>> ", timeout=5, logLevel=logging.BASIC, recv_bytes = False):
        super(Server, self).__init__(ip, port, prompt, logLevel)
        self.timeout = timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.socket.settimeout(timeout)
        self._logConnected()
        self.recv_bytes = recv_bytes
        self.buffer = None

    def _initRecv(data, recv_bytes, encoding):
        serverRecv = ''
        if recv_bytes:
            serverRecv = b''
            if type(data) == str:
                data = data.encode(encoding)
            if self.buffer :
                self._log("Insert existing data in buffer :" + str(self.buffer), level=logging.RECV)
                if type(self.buffer) == str:
                    serverRecv = self.buffer.encode(encoding)
                else:
                    serverRecv = self.buffer
        else:
            if type(data) == bytes:
                data = data.decode(encoding)
            if self.buffer and type(self.buffer) == bytes:
                self._log("Insert existing data in buffer :" + str(self.buffer), level=logging.RECV)
                if type(self.buffer) == bytes:
                    serverRecv = self.buffer.decode(encoding)
                else:
                    serverRecv = self.buffer

        return (data, serverRecv)

    def recv(self, length, recv_bytes=None,encoding='latin-1'):
        a, serverRecv = self._initRecv(None,recv_bytes,encoding)
        lenServerRecv = len(serverRecv)

        if lenServerRecv < length:
            self.buffer = ''
            try:
                serverRecv += super().recv(length - lenServerRecv, recv_bytes, encoding)
            except Exception as e:
                self._log(str(e), level=logging.ERROR)
        else:
            self.buffer = serverRecv[length:]
            serverRecv = serverRecv[:length]

        return serverRecv

    def recvUntil(self, until = None, recv_bytes=None, encoding='latin-1'):
        if not until:
            until = self.prompt
        if not until:
            raise Exception("until (and your prompt parameter) is empty.", level=logging.ERROR)

        until, serverRecv = self._initRecv(until,recv_bytes,encoding)

        while until not in serverRecv:
            recv = None
            try:
                recv = super().recv(recv_bytes=recv_bytes, encoding=encoding)
            except Exception as e:
                self._log(str(e), level=logging.ERROR)
            if recv:
                serverRecv += recv
            else:
                break

        serverRecv = serverRecv.split(until)
        self.buffer = serverRecv[1]
        serverRecv = serverRecv[0] + until

        return serverRecv

    def recvUntilRegex(self, regex, recv_bytes=None):
        regex, serverRecv = self._initRecv(regex,recv_bytes,encoding)
        regex = re.compile(regex)

        while not regex.search(serverRecv):
            recv = None
            try:
                recv = super().recv(recv_bytes=recv_bytes)
            except Exception as e:
                self._log(str(e), level=logging.ERROR)
            if recv:
                serverRecv += recv
            else:
                break

        end = regex.search(serverRecv).end()
        self.buffer = serverRecv[end:]
        serverRecv = serverRecv[:end]

        return serverRecv

    def sendLine(self, msg = None):
        if not msg:
            msg = '\n'
        if msg[-1] != '\n':
            msg += '\n'
        self.send(msg)
