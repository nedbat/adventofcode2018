"""An A* implementation."""

from abc import ABCMeta, abstractmethod
import heapq
import itertools
import time
from typing import Iterator, Tuple


class PriorityQueue:
    """A priority queue, with fast containment."""

    # Basically, this as a class:
    # https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes

    REMOVED = object()

    def __init__(self):
        self.q = []
        self.counter = itertools.count()
        self.items = {}

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def add(self, item, priority):
        if item in self:
            self.remove(item)
        entry = [priority, next(self.counter), item]
        self.items[item] = entry
        heapq.heappush(self.q, entry)

    def remove(self, item):
        entry = self.items.pop(item)
        entry[2] = self.REMOVED

    def pop(self):
        while self.q:
            _, _, item = heapq.heappop(self.q)
            if item is not self.REMOVED:
                del self.items[item]
                return item
        raise IndexError("Pop from empty priority queue")

    def empty(self):
        return not self.items


class State(metaclass=ABCMeta):
    """Abstract interface for a State for AStar."""

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def is_goal(self) -> bool:
        """Is this state a goal state? Are we done?"""

    @abstractmethod
    def next_states(self, cost) -> Iterator[Tuple['State', float]]:
        """Produce a series of next states: (new_state, new_cost), ... """

    @abstractmethod
    def guess_completion_cost(self) -> float:
        """Guess at the cost to reach the goal. Must not overestimate."""

    def summary(self) -> str:
        """A short summary of the state, for progress logging."""
        return ""


class OnceEvery:
    """An object whose .now() method is true once every N seconds."""
    def __init__(self, seconds):
        self.delta = seconds
        self.last_true = 0

    def now(self):
        ret = time.time() > self.last_true + self.delta
        if ret:
            self.last_true = time.time()
        return ret


class AStar:
    def __init__(self):
        self.candidates = PriorityQueue()
        self.costs = {}
        self.visited = set()
        self.came_from = {}

    def add_candidate(self, state, cost):
        guess = state.guess_completion_cost()
        assert guess >= 0
        self.costs[state] = cost
        self.candidates.add(state, cost + guess)

    def search(self, start_state, log=False):
        inf = float('inf')
        should_log = OnceEvery(seconds=5)
        self.add_candidate(start_state, 0)
        self.came_from[start_state] = None
        try:
            while True:
                try:
                    best = self.candidates.pop()
                except IndexError:
                    raise Exception("No solution") from None
                cost = self.costs[best]
                if best.is_goal():
                    return cost
                if log and should_log.now():
                    print(f"cost {cost}; {len(self.visited):,d} visited, {len(self.candidates):,d} candidates, {best.summary()}")
                self.visited.add(best)
                for nstate, ncost in best.next_states(cost):
                    if nstate in self.visited:
                        continue
                    old_cost = self.costs.get(nstate, inf)
                    if ncost < old_cost:
                        self.add_candidate(nstate, ncost)
                        self.came_from[nstate] = best
        finally:
            if log:
                print(f"{len(self.visited):,d} visited, {len(self.candidates):,d} candidates remaining")


def search(start_state, log=False):
    """Search a state space, starting with `start_state`. Returns the cost to reach the goal."""
    return AStar().search(start_state, log)
