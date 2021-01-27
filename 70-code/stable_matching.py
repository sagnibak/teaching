from __future__ import annotations
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Optional, Tuple

@dataclass(init=False)
class Proposer:
    name: str
    preferences: List[Rejector]
    
    def __init__(self, name: str) -> None:
        self.name = name

    def set_preferences(self, preferences: List[Rejector]) -> None:
        self.preferences = list(reversed(preferences))  # we want to pop from the end
    
    def propose_to_favorite(self) -> None:
        self.preferences[-1].add_proposal(self)
    
    def be_salty(self) -> None:
        """Be salty because you got rejected and reject the rejector."""
        self.preferences.pop()
    
    def __str__(self) -> str:
        return f"Proposer({self.name})"
    
@dataclass(init=False)
class Rejector:
    name: str
    preferences: List[Proposer]
    proposals: PriorityQueue
    favorite_so_far: Optional[Proposer]

    def __init__(self, name: str) -> None:
        self.name = name
        self.proposals = PriorityQueue()
        self.favorite_so_far = None
    
    def set_preferences(self, preferences: List[Proposer]) -> None:
        self.preferences = list(reversed(preferences))  # we want to pop from the end
    
    def add_proposal(self, proposer: Proposer) -> None:
        """The priority of a proposer is the index of the proposer in this rejector's
        preference list. PriorityQueue.get will return the proposer with lowest weight
        so this does exactly what you'd think it does.
        """
        self.proposals.put((self.preferences.index(proposer), proposer))
    
    def get_match(self) -> Proposer:
        """This must be called after calling `get_rejections`."""
        return self.favorite_so_far  # type: ignore
    
    def get_rejections(self) -> List[Proposer]:
        rank, self.favorite_so_far = self.proposals.get(block=False) if not self.proposals.empty() else (None, None)
        
        rejections = []
        while not self.proposals.empty():
            rejections.append(self.proposals.get(block=False)[1])
        
        # self.proposals.put((rank, self.favorite_so_far))
        
        return rejections

    def __str__(self) -> str:
        return f"Rejector({self.name})"
    
Matching = Tuple[Proposer, Rejector]

def gale_shapley(proposers: List[Proposer], rejectors: List[Rejector]) -> List[Matching]:
    """The Gale-Shapley propose-and-reject algorithm. Note that `proposers`
    and `rejectors` must have the same length. For the sake of avoiding boilerplate,
    I am not checking for that.
    """
    num_matches = 0
    while num_matches < len(proposers):
        # Every morning each proposer proposes to their favorite rejector.
        for proposer in proposers:
            proposer.propose_to_favorite()
        
        # Every afternoon each rejector rejects all but their favorite proposer.
        # rejections = [rejection for rejector in rejectors for rejection in rejector.get_rejections()]
        rejections = []
        for rejector in rejectors:
            rejections.extend(rejector.get_rejections())
        
        num_matches = len(proposers) - len(rejections)
        # Every evening the rejected proposers remove their favorite rejector from their list.
        for rejected_proposer in rejections:
            rejected_proposer.be_salty()
        print(num_matches)
        
    return [(r.get_match(), r) for r in rejectors]
