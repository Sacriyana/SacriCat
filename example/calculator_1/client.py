#!/usr/bin/python3
#coding: utf-8

import sys
sys.path.append("../..")
from sacricat.client import Server, logging

class Challenge:
    def __init__(self, challenge):
        self.challenge = challenge[0:-1]
        self.solution = eval(self.challenge)

    def solve(self):
        return self.solution

def main():
    client = Server('127.0.0.1',4242, prompt=">>> ",timeout=1, logLevel=logging.SENT)
    rules = client.getRules()
    client.sendKey()

    for i in range(0,10):
        challenge = client.recv(True)
        parsedChallenge = Challenge(challenge)
        solution = parsedChallenge.solve()
        
        client.send(solution)

    win = client.recv()
    client.close()

if __name__ == '__main__':
        main()