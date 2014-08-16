#!/usr/bin/env python3

from chessboard import *
import curses
import functools
import random


def finalize():
    curses.endwin()
    exit(0)


if __name__ == "__main__":

    # Initialize
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(1)
    curses.cbreak()

    # Prepare
    itemw = ((chessboard.GOAL // 3) + 1) << 1
    winw = (itemw + 3) * chessboard.LENGTH + 3
    winh = chessboard.LENGTH * 3 + 2
    win = stdscr.subwin(winh, winw, 0, 0)
    win.box()
    form = []
    for x in range(chessboard.LENGTH):
        form.append([])
        for y in range(chessboard.LENGTH):
            form[x].append(stdscr.subwin(3, itemw + 2, 3 * y + 1, (itemw + 3) * x + 2))
            form[x][y].box()
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    cb = chessboard()
    cb.randput()

    # Loop
    while True:
        cb.randput()
        numpad = cb.getchessboard()
        for x in range(chessboard.LENGTH):
            for y in range(chessboard.LENGTH):
                form[x][y].addstr(1, 1, "".join(map(lambda c: ' ' + c,
                                                    "%4d" % ((int(numpad[y][x] != 0)) * (0x1 << numpad[y][x])))))
                form[x][y].refresh()
        stdscr.refresh()
        if cb.checkwin():
            winwin = stdscr.subwin(9, 3, winh >> 1, winw >> 1)
            winwin.box()
            winwin.addstr(1, 1, "You win!")
            break
        while True:
            ch = stdscr.getch()
            try:
                if ch == ord('w'):
                    cb.move(chessboard.UP)
                    break
                elif ch == ord('s'):
                    cb.move(chessboard.DOWN)
                    break
                elif ch == ord('a'):
                    cb.move(chessboard.LEFT)
                    break
                elif ch == ord('d'):
                    cb.move(chessboard.RIGHT)
                    break
                elif ch == ord('q'):
                    finalize()
            except ValueError:
                continue

    finalize()
