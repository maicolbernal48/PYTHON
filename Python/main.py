import sys
import heapq
from PIL import Image, ImageDraw

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item):
        heapq.heappush(self.elements, item)

    def get(self):
        return heapq.heappop(self.elements)

def read_maze(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    maze = [list(line.strip()) for line in lines]
    return maze

def heuristic(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

def solve_maze(maze):
    start = None
    goal = None

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'A':
                start = (i, j)
            elif maze[i][j] == 'B':
                goal = (i, j)

    if start is None or goal is None:
        raise ValueError("Maze missing start or goal")

    frontier = PriorityQueue()
    start_node = Node(state=start, parent=None, action=None, cost=0, heuristic=heuristic(start, goal))
    frontier.put(start_node)

    explored = set()

    while not frontier.empty():
        node = frontier.get()

        if node.state == goal:
            break

        for action in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = node.state
            dx, dy = action
            new_x, new_y = x + dx, y + dy

            if (
                0 <= new_x < len(maze) and
                0 <= new_y < len(maze[0]) and
                maze[new_x][new_y] != '#' and
                (new_x, new_y) not in explored
            ):
                cost = node.cost + 1
                child_node = Node(state=(new_x, new_y), parent=node, action=action, cost=cost, heuristic=heuristic((new_x, new_y), goal))
                frontier.put(child_node)
                explored.add((new_x, new_y))

    return node

def draw_solution(maze, solution, output_filename):
    img = Image.new('RGB', (len(maze[0]) * 30, len(maze) * 30), color='white')
    draw = ImageDraw.Draw(img)

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            cell = maze[i][j]
            color = 'white' if cell == ' ' else 'black' if cell == '#' else 'green' if cell == 'A' else 'red' if cell == 'B' else 'white'
            draw.rectangle([j * 30, i * 30, (j + 1) * 30, (i + 1) * 30], fill=color, outline='black')

    node = solution
    while node.parent is not None:
        x1, y1 = node.state
        x2, y2 = node.parent.state
        draw.line([(y1 * 30 + 15, x1 * 30 + 15), (y2 * 30 + 15, x2 * 30 + 15)], fill='blue', width=3)
        maze[x1][y1] = '*'
        node = node.parent

    img.save(output_filename)

    for row in maze:
        print("".join(row))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py maze.txt")
        sys.exit(1)

    maze_filename = sys.argv[1]
    output_filename = maze_filename.replace('.txt', '_solution.png')

    maze = read_maze(maze_filename)
    solution = solve_maze(maze)
    draw_solution(maze, solution, output_filename)

    print("Solution found and saved to", output_filename)
