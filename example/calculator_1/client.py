#!/usr/bin/python3
#coding: utf-8

import sys
sys.path.append("../..")
from sacricat.client import Server, logging

class Challenge:
    def __init__(self, challenge):
        self.challenge = challenge[0:-1]
        print(self.challenge)
        self.solution = eval(self.challenge)

    def solve(self):
        return self.solution

def main():
    client = Server('127.0.0.1',4242, prompt=">>> ",timeout=5, logLevel=logging.SENT)
    rules = client.recvUntil('start)\n')
    client.sendLine()
    print('titi')

    for i in range(0,10):
        challenge = client.recv(128,clean=True)
        parsedChallenge = Challenge(challenge)
        solution = parsedChallenge.solve()
        
        client.send(solution)

    win = client.recvUntilRegex('sacricat{.*}')
    client.close()

if __name__ == '__main__':
        main()