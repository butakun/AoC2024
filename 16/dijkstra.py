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


def dijkstra(G, src, f_is_goal, debug_freq=-1, vis_logger=None):

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

        if debug_freq > 0:
            if iter % debug_freq == 0:
                logger.debug(f"iter {iter}: u = {u[:]}, D[u] = {D[u]}, len(pq) = {len(pq)}, {best_distance=}")
        if vis_logger:
            vis_logger.inspecting(iter, u)

        if f_is_goal(u):
            d = D[u]
            if best_distance is None or d < best_distance:
                best_distance = d
                best = u
                logger.debug(f"found best so far: {u[0]}, {u[1]} at D = {d}")
        for v in G[u]:
            if isinstance(v, tuple):
                v, weight = v
            else:
                weight = 1
            dist_v = D[u] + weight
            if dist_v < D[v]:
                D[v] = dist_v
                came_from[v] = u
                pq.push(v, priority=dist_v)
                if vis_logger:
                    vis_logger.found_better(iter, v, came_from, dist_v)

    logger.debug(f"{best_distance=}")
    path = backtrack(best, came_from)
    return path, best_distance


def a_star(G, src, f_is_goal, debug_freq=-1, vis_logger=None):
    pq = PriorityQueue()
    came_from = {src: None}

    gScore = defaultdict(lambda:math.inf)
    fScore = defaultdict(lambda:math.inf)
    
    gScore[src] = 0
    fScore[src] = G.HFunc(src)

    dest = None
    g_best = 0
    pq.push(src, priority=fScore[src])
    iter = 0
    while True:
        try:
            u = pq.pop()
        except IndexError:
            break
        iter += 1

        if debug_freq > 0 and iter % debug_freq == 0:
            logging.debug(f"iter {iter}: {g_best}, gScore[u] = {gScore[u]}, fScore[u] = {fScore[u]}")
        if vis_logger:
            vis_logger.inspecting(iter, u)

        if f_is_goal(u):
            logging.debug(f"reached dest {u}")
            dest = u
            if vis_logger:
                vis_logger.goal_reached(iter, dest, came_from, gScore[dest])
            break

        for v in G[u]:
            if isinstance(v, tuple):
                v, weight = v[0], v[1]
            else:
                weight = 1
            g_temp = gScore[u] + weight
            if g_temp < g_best:
                g_best = g_temp
            if g_temp < gScore[v]:
                f_temp = g_temp + G.HFunc(v)
                gScore[v] = g_temp
                fScore[v] = f_temp
                came_from[v] = u
                pq.push(v, priority=f_temp)
                if vis_logger:
                    vis_logger.found_better(iter, v, came_from, g_temp)

    assert dest is not None
    path = [dest]
    while True:
        prev = came_from[path[-1]]
        if prev is None:
            break
        path.append(prev)

    path.reverse()
    return path, gScore[dest]


def connected_component(G, start, debug=0):
    visited = set([start])
    Q = deque([start])
    while Q:
        u = Q.popleft()
        for v, _ in G[u]:
            if v not in visited:
                Q.append(v)
                visited.add(v)
    return set(visited)


def test():
    pq = PriorityQueue()

    pq.push("a", priority=10)
    pq.push("b", priority=1)
    pq.push("c", priority=100)
    while pq:
        print(pq.pop())

    pq.push("A", priority=10)
    pq.push("B", priority=1)
    pq.push("A", priority=0)
    pq.push("C", priority=100)
    while pq:
        print(pq.pop())


if __name__ == "__main__":
    test()
