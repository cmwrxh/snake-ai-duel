import curses
from curses import wrapper
import time
import random

def main(stdscr):
    curses.curs_set(0)          # Hide cursor
    stdscr.nodelay(True)
    stdscr.timeout(120)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Player
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # AI
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Food

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(120)

    # Starting positions
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

        # Quit
        if key in [ord('q'), 27]:
            break

        # Player input (only change direction, don't allow reverse immediately)
        if key in [curses.KEY_UP, ord('w')] and player['dir'] != (1, 0):
            player['dir'] = (-1, 0)
        elif key in [curses.KEY_DOWN, ord('s')] and player['dir'] != (-1, 0):
            player['dir'] = (1, 0)
        elif key in [curses.KEY_LEFT, ord('a')] and player['dir'] != (0, 1):
            player['dir'] = (0, -1)
        elif key in [curses.KEY_RIGHT, ord('d')] and player['dir'] != (0, -1):
            player['dir'] = (0, 1)

        # ── Move Player ────────────────────────────────────────
        hy, hx = player['body'][0]
        ny, nx = hy + player['dir'][0], hx + player['dir'][1]

        # Player collision: wall / self / AI body
        if (ny in (0, sh-1) or nx in (0, sw-1) or
            (ny, nx) in player['body'] or
            (ny, nx) in ai['body']):
            break

        player['body'].insert(0, (ny, nx))

        ate = False
        if (ny, nx) == food:
            player['score'] += 1
            ate = True
        else:
            player['body'].pop()

        # ── AI greedy move ─────────────────────────────────────
        if ai['body']:  # only move if AI is alive
            ay, ax = ai['body'][0]
            dy, dx = food[0] - ay, food[1] - ax

            possible_dirs = [(-1,0), (1,0), (0,-1), (0,1)]
            best_dir = ai['dir']
            best_dist = abs(dy) + abs(dx)

            for d in possible_dirs:
                ty, tx = ay + d[0], ax + d[1]
                # Avoid walls, own body, and player body (basic safety)
                if (ty in (0, sh-1) or tx in (0, sw-1) or
                    (ty, tx) in ai['body'] or
                    (ty, tx) in player['body']):
                    continue
                dist = abs(food[0] - ty) + abs(food[1] - tx)
                if dist < best_dist:
                    best_dist = dist
                    best_dir = d

            ai['dir'] = best_dir

            any_, anx = ay + ai['dir'][0], ax + ai['dir'][1]

            # AI collision: wall / self
            if any_ in (0, sh-1) or anx in (0, sw-1) or (any_, anx) in ai['body']:
                ai['body'] = []  # AI dies
            else:
                ai['body'].insert(0, (any_, anx))
                if (any_, anx) == food:
                    ai['score'] += 1
                    ate = True
                else:
                    ai['body'].pop()

        # Respawn food if eaten
        if ate:
            while True:
                food = (random.randint(1, sh-2), random.randint(1, sw-2))
                if food not in player['body'] and food not in ai['body']:
                    break

        # ── Draw everything ────────────────────────────────────
        w.clear()
        w.border(0)
        w.addstr(0, 2, f" Player: {player['score']}  |  AI: {ai['score']}  |  q = quit ")

        # Optional: vertical divider for duel feel
        for y in range(1, sh-1):
            w.addch(y, sw//2, '|', curses.color_pair(3))

        # Food
        w.addch(food[0], food[1], '*', curses.color_pair(3))

        # Player snake
        for y, x in player['body']:
            w.addch(y, x, '█', curses.color_pair(player['color']))

        # AI snake (only if alive)
        if ai['body']:
            for y, x in ai['body']:
                w.addch(y, x, '█', curses.color_pair(ai['color']))

        w.refresh()

        # ── Check game over ────────────────────────────────────
        if not player['body']:
            w.addstr(sh//2, sw//2 - 15, "YOU LOST! Press any key to exit...", curses.A_BOLD)
            w.refresh()
            w.getch()
            break

        if not ai['body']:
            w.addstr(sh//2, sw//2 - 12, "AI LOST! You win! Press any key...", curses.A_BOLD)
            w.refresh()
            w.getch()
            break

if __name__ == "__main__":
    wrapper(main)
