import random, heapq
import streamlit as st

# ----------------------------
# Maze generation and solving
# ----------------------------

EMPTY = '⬜'
WALL = '⬛'
START = '🚩'
END = '🏁'

def generate_maze(width, height, seed=1, loops=40):
    random.seed(seed)
    maze = {(x, y): WALL for x in range(width) for y in range(height)}

    def visit(x, y):
        maze[(x, y)] = EMPTY
        while True:
            neighbors = []
            if y > 1 and (x, y - 2) not in visited:
                neighbors.append((x, y - 2, x, y - 1))
            if y < height - 2 and (x, y + 2) not in visited:
                neighbors.append((x, y + 2, x, y + 1))
            if x > 1 and (x - 2, y) not in visited:
                neighbors.append((x - 2, y, x - 1, y))
            if x < width - 2 and (x + 2, y) not in visited:
                neighbors.append((x + 2, y, x + 1, y))

            if not neighbors:
                return
            nx, ny, wx, wy = random.choice(neighbors)
            maze[(wx, wy)] = EMPTY
            visited.add((nx,ny))
            visit(nx, ny)

    visited = {(1,1)}
    visit(1,1)

    # Add loops for multiple paths
    for _ in range(loops):
        x = random.randrange(1, width - 1)
        y = random.randrange(1, height - 1)
        if maze[(x, y)] == WALL:
            maze[(x, y)] = EMPTY

    return maze


# BFS solver
def bfs(maze, start, goal, width, height):
    from collections import deque
    queue = deque([start])
    parents = {start: None}
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height and maze[(nx, ny)] != WALL and (nx, ny) not in parents:
                parents[(nx, ny)] = (x, y)
                queue.append((nx, ny))
    path = []
    node = goal
    while node:
        path.append(node)
        node = parents.get(node)
    return path[::-1]


# DFS solver
def dfs(maze, start, goal, width, height):
    stack = [start]
    parents = {start: None}
    while stack:
        x, y = stack.pop()
        if (x, y) == goal:
            break
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height and maze[(nx, ny)] != WALL and (nx, ny) not in parents:
                parents[(nx, ny)] = (x, y)
                stack.append((nx, ny))
    path = []
    node = goal
    while node:
        path.append(node)
        node = parents.get(node)
    return path[::-1]


# A* solver
def astar(maze, start, goal, width, height):
    open_set = [(0, start)]
    g = {start: 0}
    parents = {start: None}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            break
        x, y = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height and maze[(nx, ny)] != WALL:
                new_cost = g[current] + 1
                if (nx, ny) not in g or new_cost < g[(nx, ny)]:
                    g[(nx, ny)] = new_cost
                    f = new_cost + abs(nx - goal[0]) + abs(ny - goal[1])
                    heapq.heappush(open_set, (f, (nx, ny)))
                    parents[(nx, ny)] = current
    path = []
    node = goal
    while node:
        path.append(node)
        node = parents.get(node)
    return path[::-1]


# Render maze as text grid
def render_maze(maze, width, height, path=None, start=None, goal=None):
    grid = ""
    for y in range(height):
        for x in range(width):
            if path and (x, y) in path and (x, y) not in (start, goal):
                grid += "🟩"   # solution path
            elif (x, y) == start:
                grid += START
            elif (x, y) == goal:
                grid += END
            elif maze[(x, y)] == WALL:
                grid += WALL
            else:
                grid += EMPTY
        grid += "\n"
    return grid

### Streamlit App

import streamlit as st

st.set_page_config(
    page_title="Maze Generator & Solver",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': 'mailto:youremail@example.com',
        'About': "### 🌀 Maze Generator & Solver\nCreated with Streamlit!"
    }
)

st.title("🌀 Maze Generator & Solver (Multi-Algorithm)")

# --- Explanation Section ---
st.markdown("""
### 🧩 Maze Legend
- ⬛ **Wall** → Blocks movement, cannot pass through  
- ⬜ **Empty space** → Free path  
- 🚩 **Start** → The entry point of the maze (top-left corner)  
- 🏁 **End** → The exit point of the maze (bottom-right corner)  
- 🟩 **Solution path** → The path found by the solving algorithm
""")

# Inputs
width = st.slider("Maze Width (odd number)", 9, 61, 39, step=2)
height = st.slider("Maze Height (odd number)", 9, 41, 19, step=2)
loops = st.slider("Extra loops (for multiple solutions)", 0, 200, 60)
seed = st.number_input("Random Seed", min_value=0, value=1, step=1)

if st.button("Generate & Solve Maze"):
    maze = generate_maze(width, height, seed, loops)
    start, goal = (1,1), (width-2, height-2)

    # Solve with all three algorithms
    bfs_path = bfs(maze, start, goal, width, height)
    dfs_path = dfs(maze, start, goal, width, height)
    astar_path = astar(maze, start, goal, width, height)

    # Show results stacked vertically
    st.subheader("🟠 DFS Solution")
    st.text(render_maze(maze.copy(), width, height, dfs_path, start, goal))

    st.subheader("🔵 BFS Solution")
    st.text(render_maze(maze.copy(), width, height, bfs_path, start, goal))

    st.subheader("🟢 A* Solution")
    st.text(render_maze(maze.copy(), width, height, astar_path, start, goal))
