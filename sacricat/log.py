#coding: utf-8
#Thanks to @initbrain for his help

import logging
import sys
import os

BASIC = 24
CHALLENGE = 23
RECV = 22
SENT = 21

class ScLogger(logging.Logger):
    def _basic(self, message, *args, **kws):
        if self.isEnabledFor(BASIC):
            self._log(BASIC, message, args, **kws)

    def _challenge(self, message, *args, **kws):
        if self.isEnabledFor(CHALLENGE):
            self._log(BASIC, message, args, **kws)

    def _recv(self, message, *args, **kws):
        if self.isEnabledFor(RECV):
            self._log(VERBOSE, message, args, **kws)

    def _sent(self, message, *args, **kws):
        if self.isEnabledFor(SENT):
            self._log(VERBOSE_PLUS, message, args, **kws)


class ColorFormatter(logging.Formatter):
    """
    A logging formatter that colors messages depending on their level.
    """
    _color_map = {
        'DEBUG': '\033[22;32m',
        'INFO': '\033[01;34m',
        'SENT': '\033[38;5;78m',
        'RECV': '\033[38;5;34m',
        'CHALLENGE': '\033[38;5;75m',
        'BASIC': '\033[38;5;51m',
        'WARNING': '\033[22;35m',
        'ERROR': '\033[22;31m',
        'CRITICAL': '\033[01;31m',
    }

    def _colorize(self, level, message):
        if os.name == 'nt':
            return message
        else:
            return '{0}{1}\033[0;0m'.format(self._color_map[level],message)

    def format(self, record):
        """
        Overrides the default :func:`logging.Formatter.format` to add colors to
        the :obj:`record`'s :attr:`levelname` and :attr:`name` attributes.
        """
        s = super().format(record)
        return self._colorize(record.levelname, s)



def addLevel(value, name):
    logging.addLevelName(value, name)
    setattr(logging, name, value)


addLevel(BASIC, "BASIC")
addLevel(CHALLENGE, "CHALLENGE")
addLevel(RECV, "RECV")
addLevel(SENT, "SENT")

logging.setLoggerClass(ScLogger)

# prepare formatters
console_formatter = ColorFormatter(
    fmt='\r[%(asctime)s]%(message)s',
    #fmt='\r%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# prepare handlers
handlers = []

## console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(console_formatter)
handlers.append(console_handler)

# configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(BASIC)
for handler in handlers:
    root_logger.addHandler(handler)