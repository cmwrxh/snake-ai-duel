import curses
from curses import wrapper
import time
import random

def main(stdscr):
    curses.curs_set(0)          # Hide cursor
    stdscr.nodelay(True)        # Non-blocking input
    stdscr.timeout(100)         # Refresh ~10 fps

    # Colors
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Player
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # AI
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Food

    # Game state (to be filled later)
    height, width = stdscr.getmaxyx()
    player = {'body': [(10, 10)], 'dir': (0, 1), 'color': 1}
    ai = {'body': [(height-10, width-20)], 'dir': (0, -1), 'color': 2}
    food = (random.randint(1, height-2), random.randint(1, width-2))

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

        stdscr.clear()
        stdscr.addstr(0, 0, "Snake AI Duel - Press q to quit")
        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    wrapper(main)
