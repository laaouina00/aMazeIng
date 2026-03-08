import curses


def build_maze_array(maz):
    height = maz.height
    width = maz.width
    maze_array = [[1 for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)]
    for r in range(height):
        for c in range(width):
            cell = maz.maze[r][c]
            maze_r = r * 2 + 1
            maze_c = c * 2 + 1
            maze_array[maze_r][maze_c] = 0
            if not cell.right and c < width - 1:
                maze_array[maze_r][maze_c + 1] = 0
            if not cell.down and r < height - 1:
                maze_array[maze_r + 1][maze_c] = 0
    maze_array[1][0] = 0
    maze_array[height * 2 - 1][width * 2] = 0
    return maze_array


def print_maze_curses(maz, maze_array):

    def draw(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE,   curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK,   curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED,     curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_YELLOW,  curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_GREEN,   curses.COLOR_GREEN) 
        def safe_addstr(r, c, ch, attr):
            try:
                stdscr.addstr(r, c, ch, attr)
            except curses.error:
                pass
        def redraw():
            term_rows, term_cols = stdscr.getmaxyx()
            stdscr.clear()
            for r, row in enumerate(maze_array):
                if r >= term_rows:
                    break
                for c, val in enumerate(row):
                    if c >= term_cols:
                        break
                    if val == 1:
                        safe_addstr(r, c, "█", curses.color_pair(1))
                    else:
                        is_solution_corridor = False
                        if not (r % 2 == 1 and c % 2 == 1):
                            if r % 2 == 1 and c % 2 == 0 and 0 < c < len(row) - 1:
                                left_r, left_c   = (r - 1) // 2, (c - 2) // 2
                                right_r, right_c = (r - 1) // 2, c // 2
                                if (0 <= left_c < maz.width and 0 <= right_c < maz.width):
                                    if (maz.maze[left_r][left_c].solution and
                                            maz.maze[right_r][right_c].solution):
                                        is_solution_corridor = True
                            elif r % 2 == 0 and c % 2 == 1 and 0 < r < len(maze_array) - 1:
                                top_r, top_c    = (r - 2) // 2, (c - 1) // 2
                                bot_r, bot_c    = r // 2,        (c - 1) // 2
                                if (0 <= top_r < maz.height and 0 <= bot_r < maz.height):
                                    if (maz.maze[top_r][top_c].solution and
                                            maz.maze[bot_r][bot_c].solution):
                                        is_solution_corridor = True
                        if r % 2 == 1 and c % 2 == 1:
                            cell_r = (r - 1) // 2
                            cell_c = (c - 1) // 2
                            cell = maz.maze[cell_r][cell_c]

                            if cell.blocked:
                                safe_addstr(r, c, "▓", curses.color_pair(3))
                            elif cell.solution:
                                safe_addstr(r, c, "·", curses.color_pair(4))
                            else:
                                safe_addstr(r, c, " ", curses.color_pair(2))
                        else:
                            if is_solution_corridor:
                                safe_addstr(r, c, "·", curses.color_pair(5))
                            else:
                                safe_addstr(r, c, " ", curses.color_pair(2))
            stdscr.refresh()
        redraw()
        while True:
            key = stdscr.getch()
            if key == curses.KEY_RESIZE:
                redraw()
            else:
                break
    curses.wrapper(draw)