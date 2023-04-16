import sys


def run_game_code(path):
    with open(path, 'r') as f:
        code = f.read()
        return exec(code, globals())


if __name__ == "__main__":
    print(1)
    if len(sys.argv) > 1:
        print(2)
        game_path = sys.argv[1]
        game = run_game_code(game_path)
        print(game.GameSnake.score)
    else:
        print("Please provide the game path as an argument.")
