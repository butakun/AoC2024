import logging
import math
import heapq
from collections import defaultdict, deque
import itertools

logger = logging.getLogger(__name__)


class PriorityQueue(object):
    
    def __init__(self):
        self._pq = []
        self._tasks = {}
        self._counter = itertools.count()
        self._removed_marker = "REMOVED"

    def push(self, task, priority):
        if task in self._tasks:
            self.remove_task(task)
        count = next(self._counter)
        entry = [priority, count, task]
        self._tasks[task] = entry
        heapq.heappush(self._pq, entry)

    def remove_task(self, task):
        entry = self._tasks.pop(task)
        entry[-1] = self._removed_marker

    def pop(self):
        while self._pq:
            priority, count, task = heapq.heappop(self._pq)
            if task is not self._removed_marker:
                del self._tasks[task]
                return task
        raise IndexError("priority queue is empty")

    def __len__(self):
        return len(self._pq)


def backtrack(dest, came_from):
    path = [dest]
    while True:
        prev = came_from[path[-1]]
        if prev is None:
            break
        path.append(prev)
    return path


def dijkstra(G, src, f_is_goal, debug_freq=-1):

    D = defaultdict(lambda:math.inf)
    D[src] = 0
    came_from = {src: None}

    pq = PriorityQueue()
    pq.push(src, priority=D[src])

    best_distance = None
    best = None

    dest = None
    iter = 0
    while True:
        try:
            u = pq.pop()
        except IndexError:
            break
        iter += 1
        assert u is not None

        if f_is_goal(u):
            d = D[u]
            if best_distance is None or d < best_distance:
                best_distance = d
                best = u
                logger.debug(f"found best so far: {u[0]}, {u[1]} at D = {d}")
        for v, weight in G[u]:
            dist_v = D[u] + weight
            if dist_v < D[v]:
                D[v] = dist_v
                came_from[v] = u
                pq.push(v, priority=dist_v)

    logger.debug(f"{best_distance=}")
    path = backtrack(best, came_from)
    return path, best_distance, D
