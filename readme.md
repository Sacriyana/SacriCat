# SacriCat V1

SacriCat is a socket client/server library to help hackers in CTF both of side (creator or gamer)

### License

Creative Common BY-NC
![alt text](https://raw.githubusercontent.com/Saciryana/SacriCat/branch/master/license.png)

# Installation

This librairy only use default python import. So no requirement.

Tu use it, you can copy sacricat folder into your projet.

The setup.py creation is on the TODO list :D.

# The client

To connect to the server you have to call the sacricat.client.Server with 2 required fields:
- IP 
- port

You have 2 optionnal fields :
- prompt string, default: ">>> "
- timeout for socket, default: 2 seconds.
- log level, default: BASIC (cf "How use log ?" for more details)

The socket is started when you instantiate the object.

### Example

```python
from sacricat.client import Server

client  = Server('127.0.0.1',8080, prompt=">>> ",timeout=1, logLevel=logging.BASIC)
```

## Fonctionnalities

There is a list of avaible function :
- send(msg) : Send a message (like a normal socket)
- sendKey(key) : Send a key
- recv : wait to receive a response from the server. This function waits for a prompt or a timeout and return the response.
- getRules : retrieve rules from server if rules doesn't exist else return existing rules.

## A working client

You can find working clients inside the example folder.


# The server

SacriCat use python socket to create server and help you with some classes to define your challenge.  
There is 2 modes for server.

## Architecture

The server object from `sacricat.server.Server` need 2 required fields to work:
- the listen IP (ex: 127.0.0.1)
- the listen port (ex: 8080)
- your challenge class (which need inherit from `sacricat.server.Challenge`)

You have 3 optional fields :
- the thread class which is instantiate for each connected client, default: SimpleServerThread.
- the prompt which is added when server send the challenge, default: ">>> "
- log level, default: BASIC


### Example

```python
from sacricat.server import Server, logging

server = Server("127.0.0.1", 4242, MyChallenge, prompt=">>> ", logLevel=logging.BASIC)
```

## Challenge class

Your challenge class have to inherit from `Sacricat.server.Challenge`.
You have to declare some variables which define your challenge :
- rules message
- win message
- lose message
- number of turns
- the max authorized time to answer of your challenge

Once you have declared them, you have to override `initTurn` method which represent your game for one turn.
In this method, you have to define at least 2 instance variables: challenge whivh is your challenge in string format like you send to the player, and the solution which will be compare to the answer.

You can define \_str and \_repr if you want to have a better log.

In this method you can get `self.turn` if you want the current turn index.

### Exemple
```python
from sacricat.server import Challenge
from random import randint

class MyChallenge(Challenge):
    rules = """Your rules"""
    win = "Win message"
    lose = "Lose message"
    nbTurn = 10
    authorizedTime = 2

    def initTurn(self):
        a = randint(0,999999)
        b = randint(0,999999)
        self.challenge = "%s + %s ?" % (a, b)
        self.solution = str(a + b)
        self._str = "%s + %s = %s" % (a, b, self.solution)
        self._repr = "<Challenge(%s,%s,%s)>" % (a, b, self.solution)
```

## A working server

You can find working servers inside example folder.

# How use log ?

SacriCat is based on a modified classic logger in python to print inside terminal.

I had 3 custom level :
- BASIC : print classic WARNING logs and connection/disconnection log
- CHALLENGE : print BASIC logs and challenge log (make sens only for server, not for client)
- RECV : print CHALLENGE logs and received log
- SENT : print RECV logs and sent log

To call it, you have just to add `logging` inside your SacriCat import and use :
- logging.BASIC
- logging.CHALLENGE
- logging.RECV
- logging.SENT

```python
from sacricat.client import Server, logging
```