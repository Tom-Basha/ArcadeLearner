import random

class Ghost:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def move(self, pacman_position, blinky_position=None):
        if self.name == "Blinky":
            self.blinky_strategy(pacman_position)
        elif self.name == "Pinky":
            self.pinky_strategy(pacman_position)
        elif self.name == "Inky":
            self.inky_strategy(pacman_position, blinky_position)
        elif self.name == "Clyde":
            self.clyde_strategy(pacman_position)

    def blinky_strategy(self, pacman_position):
        if self.is_in_line_of_sight(pacman_position):
            self.move_toward(pacman_position)
        else:
            self.move_randomly()

    def pinky_strategy(self, pacman_position):
        target_position = (pacman_position[0] + 4, pacman_position[1] + 4)
        if self.is_reachable(target_position):
            self.move_toward(target_position)
        else:
            self.move_randomly()

    def inky_strategy(self, pacman_position, blinky_position):
        target_position = (pacman_position[0] * 2 - blinky_position[0],
                           pacman_position[1] * 2 - blinky_position[1])
        self.move_toward(target_position)

    def clyde_strategy(self, pacman_position):
        distance = self.distance(pacman_position, self.position)
        if distance > 8:
            self.move_randomly()
        else:
            self.move_away_from(pacman_position)

    def is_in_line_of_sight(self, pacman_position):
        return pacman_position[0] == self.position[0] or pacman_position[1] == self.position[1]

    def is_reachable(self, position):
        # Check if the position is within the game grid and not a wall
        return 0 <= position[0] < grid_width and 0 <= position[1] < grid_height and game_grid[position] != '#'

    def move_toward(self, target_position):
        possible_moves = self.get_possible_moves()
        min_distance = float('inf')
        best_move = None

        for move in possible_moves:
            new_position = (self.position[0] + move[0], self.position[1] + move[1])
            distance = self.distance(target_position, new_position)
            if distance < min_distance:
                min_distance = distance
                best_move = move

        self.position = (self.position[0] + best_move[0], self.position[1] + best_move[1])

    def move_away_from(self, pacman_position):
        possible_moves = self.get_possible_moves()
        max_distance = 0
        best_move = None

        for move in possible_moves:
            new_position = (self.position[0] + move[0], self.position[1] + move[1])
            distance = self.distance(pacman_position, new_position)
            if distance > max_distance:
                max_distance = distance
                best_move = move

        self.position = (self.position[0] + best_move[0], self.position[1] + best_move[1])

    def move_randomly(self):
        random_move = random.choice(self.get_possible_moves())
        self.position = (self.position[0] + random_move[0], self.position[1] + random_move[1])


    def get_possible_moves(self):
        possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_moves = []

        for move in possible_moves:
            new_position = (self.position[0] + move[0], self.position[1] + move[1])
            if self.is_reachable(new_position):
                valid_moves.append(move)

        return valid_moves

    @staticmethod
    def distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# You should define the game grid, grid_width, and grid_height to use the is_reachable function
game_grid = []  # 2D array representing the game grid
grid_width = len(game_grid[0]) if game_grid else 0
grid_height = len(game_grid)

# Create the ghost instances and set their initial positions
blinky = Ghost("Blinky", (5, 5))
pinky = Ghost("Pinky", (5, 6))
inky = Ghost("Inky", (6, 5))
clyde = Ghost("Clyde", (6, 6))

# Example usage
pacman_position = (7, 7)
blinky.move(pacman_position)
pinky.move(pacman_position)
inky.move(pacman_position, blinky.position)
clyde.move(pacman_position)


# linky (Red Ghost): Blinky always tries to move towards Pac-Man's current position. If Pac-Man is not in his line of sight, Blinky will move randomly.
#
# Pinky (light purple Ghost): Pinky tries to move to a point four spaces ahead of Pac-Man's current position, on the same horizontal or vertical axis. If that position is not reachable, Pinky will move randomly.
#
# Inky (Cyan Ghost): Inky's movement is a bit more complex. He uses Pac-Man's position and Blinky's position to calculate a new target position, which is a point on the opposite side of Pac-Man from Blinky. Inky then tries to move towards this target position.
#
# Clyde (green Ghost): Clyde's movement is also a bit random. If Pac-Man is far away, Clyde will move randomly. But if Pac-Man gets too close, Clyde will move away from him.