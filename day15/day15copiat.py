from heapq import *

grid = [[*map(int, l.strip())] for l in open("day15/input.txt")]
next = lambda r,c:[(r-1,c),(r+1,c),(r,c-1),(r,c+1)]

def grow(grid):
  R, C = len(grid), len(grid[0])
  return [[(grid[r%R][c%C] + c//C + r//R - 1)%9 + 1
          for c in range(5*C)] for r in range(5*R)]

def find(grid):
  R, C = len(grid), len(grid[0])
  exit = (R-1, C-1)
  seen = set()
  todo = [(0, (0,0))]
  while todo:
    risk, pos = heappop(todo)

    if pos == exit: return risk
    if pos in seen: continue
    seen.add(pos)

    for r, c in next(*pos):
      if 0 <= r < R and 0 <= c < C:
        heappush(todo, (risk + grid[r][c], (r, c)))

print(find(grid), find(grow(grid)))