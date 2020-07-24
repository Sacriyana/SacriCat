#coding: utf-8

import socket
from sacricat.log import logging


class Core:
    """ Abstract class to define core functions"""
    length_bytes = 128
    def __init__(self, ip, port, prompt, logLevel=logging.BASIC):
        self.ip = ip
        self.port = port
        self.prompt = prompt
        self.socket = None
        self.logLevel = logLevel
        self.logger = logging.getLogger()
        self.logger.setLevel(self.logLevel)

    def _log(self, log, heading=True, level=logging.BASIC):
        if heading:
            log = "[*] %s:%s - " % (self.ip, self.port) + log
        self.logger.log(level,log)

    def _logConnected(self, msg=''):
        log = "[+] %s:%s - Connected" % (self.ip, self.port)
        if msg:
            log += " - " + msg
        self._log(log, heading=False)

    def _logDisconnected(self, msg=''):
        log = "[-] %s:%s - Disconnected" % (self.ip, self.port)
        if msg:
            log += " - " + msg
        self._log(log, heading=False)

    def close(self):
        res = self.socket.close()
        self._logDisconnected()
        return res

    def recv(self, length=None, recv_bytes = None, encoding='latin-1'):
        if not length:
            length = self.length_bytes
        if length < 1:
            raise Exception("Length < 1")
        r = self.socket.recv(length)
        if recv_bytes is None:
            recv_bytes = self.recv_bytes 
        if not recv_bytes:
            r = r.decode(encoding)
        self._log("Received - "+repr(r), level=logging.RECV)
        return r

    def send(self, msg, sendPrompt=False):
        if type(msg) == str:
            if sendPrompt:
                msg += '\n'+self.prompt
            msg = msg.encode()
        try:
            self.socket.sendall(msg)
        except socket.error as e:
            self._log("Socket Error - "+str(e), level=logging.ERROR)
            return False
        else:
            self._log("Sent - "+repr(msg), level=logging.SENT)
            return True