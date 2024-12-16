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
    Q = [dest]
    H = set()
    while Q:
        u = Q.pop()
        H.add(u)
        prevs = came_from[u]
        logger.debug(f"  {u} -> {prevs}")
        if prevs:
            Q.extend(prevs)
    return H


def dijkstra(G, src, f_is_goal, debug_freq=-1, vis_logger=None):

    D = defaultdict(lambda:math.inf)
    D[src] = 0
    came_from = {src: None}

    pq = PriorityQueue()
    pq.push(src, priority=D[src])

    best_distance = None
    best = set()

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
            if best_distance is None or d <= best_distance:
                best_distance = d
                if d == best_distance:
                    best.add(u)
                else:
                    best = set([u])
                logger.debug(f"found best so far: {u} at D = {d}")
        for v in G[u]:
            if isinstance(v, tuple):
                v, weight = v
            else:
                weight = 1
            dist_v = D[u] + weight
            if dist_v <= D[v]:
                if D[v] == dist_v:
                    came_from[v].add(u)
                else:
                    came_from[v] = set([u])
                D[v] = dist_v
                pq.push(v, priority=dist_v)
                if vis_logger:
                    vis_logger.found_better(iter, v, came_from, dist_v)

    logger.debug(f"{best_distance=}")
    all_nodes = set()
    for goal in best:
        logger.debug(f"{goal=}")
        nodes = backtrack(goal, came_from)
        all_nodes |= nodes
    return all_nodes, best_distance
