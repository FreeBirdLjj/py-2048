#!/usr/bin/env python3

import functools
import random


class chessboard(object):

    LENGTH = 4
    GOAL = 11       # For 2^11

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self):
        self._numpad = []
        for i in range(chessboard.LENGTH):
            self._numpad.append([0] * chessboard.LENGTH)

    def randput(self):
        spaces = list(filter(lambda x: x != 0,
                             map(lambda a, b: int(a == 0) * b,
                                 functools.reduce(list.__add__,
                                                  self._numpad,
                                                  []),
                                 range(chessboard.LENGTH ** 2))))
        randposition = spaces[random.randint(0, len(spaces) - 1)]
        col = randposition % chessboard.LENGTH
        row = randposition // chessboard.LENGTH
        randchess = 2 if random.randint(1, 6) == 6 else 1
        self._numpad[row][col] = randchess

    def move(self, direction):
        def moveline(line, d):
            def shift(l, d):
                if d:
                    return list(filter(lambda x: x != 0, l)) + [0] * l.count(0)
                else:
                    return [0] * l.count(0) + list(filter(lambda x: x != 0, l))

            def merge(l, d):
                if d:
                    f = lambda x: x
                else:
                    f = lambda x: x.__reversed__()
                for i in f(range(len(l) - 1)):
                    if l[i] != 0 and l[i] == l[i + 1]:
                        l[i] += 1
                        l[i + 1] = 0
                return l

            return shift(merge(shift(line, d), d), d)
    
        prev = self._numpad.copy()
        #if direction == chessboard.LEFT:
        #    self._numpad = list(map(lambda l: moveline(l, True),
        #                            self._numpad))
        #elif direction == chessboard.RIGHT:
        #    self._numpad = list(map(lambda l: moveline(l, False),
        #                            self._numpad))
        #elif direction == chessboard.UP:
        #    self._numpad = list(map(lambda l: list(l),
        #                            zip(*map(lambda l: moveline(l, True),
        #                                     zip(*self._numpad)))))
        #elif direction == chessboard.DOWN:
        #    self._numpad = list(map(lambda l: list(l),
        #                            zip(*map(lambda l: moveline(l, False),
        #                                     zip(*self._numpad)))))
        self._numpad = {chessboard.LEFT: list(map(lambda l: moveline(l, True),
                                                  self._numpad)),
                        chessboard.RIGHT: list(map(lambda l: moveline(l, False),
                                                   self._numpad)),
                        chessboard.UP: list(map(lambda l: list(l),
                                                zip(*map(lambda l: moveline(l, True),
                                                         zip(*self._numpad))))),
                        chessboard.DOWN: list(map(lambda l: list(l),
                                                  zip(*map(lambda l: moveline(l, False),
                                                           zip(*self._numpad)))))}[direction]
        if prev == self._numpad:
            raise ValueError

    def getchessboard(self):
        return self._numpad

    def checkwin(self):
        return functools.reduce(list.__add__,
                                self._numpad,
                                []).count(chessboard.GOAL) > 0
