# src/turkey_twin/map_graph.py

from typing import List, Tuple, Dict
from heapq import heappush, heappop
import math

class MapGraph:
    """

    0 = Obstacle 
    1 = Navigable 
    """
    def __init__(self, size: int = 10):
        self.size = size

        self.grid = [[1 for _ in range(size)] for _ in range(size)]
        
    
        print("\n[MAP]: Adding obstacles to the 10x10 grid...")
        for x in range(4, 7):
            for y in range(2, 8):
                self.grid[y][x] = 0 # Mark as obstacle (0)
                
    def is_valid(self, x: int, y: int) -> bool:

        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x] == 1
        return False

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:

        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:

        if not self.is_valid(start[0], start[1]) or not self.is_valid(end[0], end[1]):
            print(f"[PATHFINDER ERROR]: Start {start} or End {end} is invalid/blocked.")
            return []

        if start == end:
            return [start]
            
      
        open_set: List[Tuple[float, float, int, int]] = []
        heappush(open_set, (0, 0, start[0], start[1]))

      
        g_cost: Dict[Tuple[int, int], float] = {start: 0}
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}

     
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while open_set:
    
            f_cost, current_g, current_x, current_y = heappop(open_set)
            current_node = (current_x, current_y)

            if current_node == end:
       
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                path.append(start)
                path.reverse()
                return path

            for dx, dy in directions:
                neighbor_x, neighbor_y = current_x + dx, current_y + dy
                neighbor_node = (neighbor_x, neighbor_y)
                
        
                if not self.is_valid(neighbor_x, neighbor_y):
                    continue

         
                new_g_cost = current_g + 1 

                if neighbor_node not in g_cost or new_g_cost < g_cost[neighbor_node]:
                    g_cost[neighbor_node] = new_g_cost
                    f_cost = new_g_cost + self.heuristic(neighbor_node, end)
                    heappush(open_set, (f_cost, new_g_cost, neighbor_x, neighbor_y))
                    came_from[neighbor_node] = current_node

        return []