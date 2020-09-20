import time


def transform(x):
    if x == 0:
        return 'o'
    if x == 1:
        return 'x'
    return ' '


class TicTacToe:
    def __init__(self):
        self.mode = 'hotsit'
        self.size = 5
        self.row = 5
        self.state = [[2 for _ in range(self.size)] for _ in range(self.size)]
        self.field = ('{} | ' * (self.size - 1) + '{}' + '\n' + '----' * (self.size - 1) + '-' + '\n') * (
                self.size - 1) + '{} | ' * (self.size - 1) + '{}'
        self.turner = 1

    def show_field(self):
        s = [self.state[x // self.size][x % self.size] for x in range(self.size ** 2)]
        print(self.field.format(*list(map(transform, s))))

    def turn(self, y, x):
        if self.state[x][y] != 2:
            print("Try another place)")
            return False
        self.state[x][y] = self.turner % 2
        self.turner += 1
        if self.check():
            print('The winner is {} player'.format('first' if self.turner % 2 == 0 else 'second'))
            return True
        if self.tie():
            print("Oh, game ended no one wins((")
            return True

    def checker(self, arr):
        for i in range(1, self.row):
            if arr[i-1] != arr[i] or arr[i] == 2:
                return False
        return True

    def check(self):
        # Horizontal
        for i in range(self.size):
            for j in range(self.size - self.row + 1):
                if self.checker(self.state[i][j:j+self.row]):
                    return True

        # Vertical
        for i in range(self.size - self.row + 1):
            for j in range(self.size):
                if self.checker([self.state[x][j] for x in range(self.row)]):
                    return True

        # Diagonal 1
        for i in range(self.size - self.row + 1):
            for j in range(self.size - self.row + 1):
                if self.checker([self.state[i+k][j+k] for k in range(self.row)]):
                    return True

        # Diagonal 2
        for i in range(self.size - self.row + 1):
            for j in range(self.row - 1, self.size):
                if self.checker([self.state[i+k][j-k] for k in range(self.row)]):
                    return True

        return False

    def check_winner(self):
        # Horizontal
        for i in range(self.size):
            for j in range(self.size - self.row + 1):
                if self.checker(self.state[i][j:j+self.row]):
                    return -10 if self.state[i][j] == 1 else 10

        # Vertical
        for i in range(self.size - self.row + 1):
            for j in range(self.size):
                if self.checker([self.state[x][j] for x in range(self.row)]):
                    return -10 if self.state[i][j] == 1 else 10

        # Diagonal 1
        for i in range(self.size - self.row + 1):
            for j in range(self.size - self.row + 1):
                if self.checker([self.state[i+k][j+k] for k in range(self.row)]):
                    return -10 if self.state[i][j] == 1 else 10

        # Diagonal 2
        for i in range(self.size - self.row + 1):
            for j in range(self.row - 1, self.size):
                if self.checker([self.state[i+k][j-k] for k in range(self.row)]):
                    return -10 if self.state[i][j] == 1 else 10
        if self.tie():
            return 0

        return None

    def tie(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 2:
                    return False
        return True

    def new_game(self):
        print("Choose game mode: hotsit, vsAI, simulation. Just number 1-3")
        self.mode = int(input())
        print("Choose size of playing field")
        self.size = int(input())
        print("Choose size of row to collect to win")
        self.row = int(input())
        self.state = [[2 for _ in range(self.size)] for _ in range(self.size)]
        self.field = ('{} | ' * (self.size - 1) + '{}' + '\n' + '----' * (self.size-1) + '-' + '\n') * (
                    self.size - 1) + '{} | ' * (self.size - 1) + '{}'
        self.turner = 1
        print("Let's start! Remember axis of x,y go right and down, start point is left upper corner. Put x and y "
              "separated by space. Good luck!")
        while True:
            if self.mode == 2:
                if self.turner % 2 == 0:
                    arg = self.AI()
                    if self.turn(arg[1], arg[0]):
                        break
                    else:
                        continue

            if self.mode == 1 or self.mode == 2:
                self.show_field()
                print('Put x and y')
                if self.turn(*list(map(int, input().split()))):
                    break

            if self.mode == 3:
                arg = self.AI()
                if self.turn(arg[1], arg[0]):
                    break
                else:
                    self.show_field()
                    time.sleep(2)
                    continue

        print('Do you want to play again? y/n')
        if input() == 'y':
            self.new_game()

    def AI(self):
        best_move = []
        depth = 0
        best_score = -100000
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 2:
                    self.state[i][j] = self.turner % 2
                    score = self.minimum_and_maximum(False, depth)
                    self.state[i][j] = 2
                    if score > best_score:
                        best_score = score
                        best_move = [i, j]
        return best_move

    def minimum_and_maximum(self, is_max, depth):
        result = self.check_winner()
        if result is not None:
            if self.turner % 2 == 1:
                result *= -1
            return result
        if depth == 3:
            return 0
        if is_max:
            best_score = -100000
            for i in range(self.size):
                for j in range(self.size):
                    if self.state[i][j] == 2:
                        self.state[i][j] = self.turner % 2
                        score = self.minimum_and_maximum(False, depth + 1)
                        self.state[i][j] = 2
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 100000
            for i in range(self.size):
                for j in range(self.size):
                    if self.state[i][j] == 2:
                        self.state[i][j] = (self.turner+1) % 2
                        score = self.minimum_and_maximum(True, depth + 1)
                        self.state[i][j] = 2
                        best_score = min(score, best_score)
            return best_score


game = TicTacToe()
game.new_game()
