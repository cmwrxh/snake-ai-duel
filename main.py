import curses
from curses import wrapper
import time
import random

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(120)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Player
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # AI
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Food

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(120)

    player = {
        'body': [(sh//2, sw//2 + i) for i in range(5, 0, -1)],
        'dir': (0, 1),
        'color': 1,
        'score': 0
    }

    ai = {
        'body': [(sh//2, sw//4)],
        'dir': (0, -1),
        'color': 2,
        'score': 0
    }

    food = (random.randint(1, sh-2), random.randint(1, sw-2))

    while True:
        key = w.getch()
        if key in [ord('q'), 27]: break

        # Player direction change
        if key in [curses.KEY_UP, ord('w')]:    player['dir'] = (-1, 0)
        elif key in [curses.KEY_DOWN, ord('s')]: player['dir'] = (1, 0)
        elif key in [curses.KEY_LEFT, ord('a')]: player['dir'] = (0, -1)
        elif key in [curses.KEY_RIGHT, ord('d')]: player['dir'] = (0, 1)

        # Move player
        hy, hx = player['body'][0]
        ny = hy + player['dir'][0]
        nx = hx + player['dir'][1]

        # Simple collision (wall / self)
        if ny in (0, sh-1) or nx in (0, sw-1) or (ny, nx) in player['body']:
            break

        player['body'].insert(0, (ny, nx))

        # Eat food?
        if (ny, nx) == food:
            player['score'] += 1
            food = (random.randint(1, sh-2), random.randint(1, sw-2))
        else:
            player['body'].pop()

        w.clear()
        w.border(0)
        w.addstr(0, 2, f" Player: {player['score']}  |  AI: {ai['score']}  |  q = quit ")

        # Draw food
        w.addch(food[0], food[1], '*', curses.color_pair(3))

        # Draw player
        for y, x in player['body']:
            w.addch(y, x, '█', curses.color_pair(player['color']))
        # --- AI simple greedy logic ---
        ay, ax = ai['body'][0]
        dy, dx = food[0] - ay, food[1] - ax

        possible_dirs = [
            (-1, 0), (1, 0), (0, -1), (0, 1)
        ]

        best_dir = ai['dir']
        best_dist = abs(dy) + abs(dx)

        for d in possible_dirs:
            ny, nx = ay + d[0], ax + d[1]
            if (ny, nx) in ai['body'] or ny in (0, sh-1) or nx in (0, sw-1):
                continue
            new_dist = abs(food[0] - ny) + abs(food[1] - nx)
            if new_dist < best_dist:
                best_dist = new_dist
                best_dir = d

        ai['dir'] = best_dir

        # Move AI
        any, anx = ay + ai['dir'][0], ax + ai['dir'][1]
        ai['body'].insert(0, (any, anx))

        if (any, anx) == food:
            ai['score'] += 1
            food = (random.randint(1, sh-2), random.randint(1, sw-2))
        else:
            ai['body'].pop()

        # Draw AI
        for y, x in ai['body']:
            w.addch(y, x, '█', curses.color_pair(ai['color']))
        w.refresh()

if __name__ == "__main__":
    wrapper(main)
