# Stubs for networkx.algorithms.centrality.current_flow_closeness (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

from networkx.algorithms.centrality.flow_matrix import *

def current_flow_closeness_centrality(
    G, weight: Optional[Any] = ..., dtype: Any = ..., solver: str = ...
): ...

information_centrality = current_flow_closeness_centrality