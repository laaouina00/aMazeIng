def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config = parse_config(sys.argv[1])

    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    seed = config.get("SEED", None)
    perfect = config["PERFECT"].lower() == "true"
    entry = tuple(map(int, config["ENTRY"].split(",")))
    exit_ = tuple(map(int, config["EXIT"].split(",")))
    output_file = config["OUTPUT_FILE"]

    maze = MazeGenerate(width, height)
    maze.draw_42()
    maze.remove_walls(seed)

    if not perfect:
        maze.add_extra_paths(entry, exit_)

    start = maze.maze[entry[1]][entry[0]]
    end = maze.maze[exit_[1]][exit_[0]]
    path = maze.bfs(start, end)

    write_output(maze, path, entry, exit_, output_file)

    maze_array = build_maze_array(maze)
    print_maze_curses(maze, maze_array)


if __name__ == "__main__":
    main()