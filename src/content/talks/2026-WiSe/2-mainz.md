---
speakerName: Markus Blumenstock
title: Revisiting the Binary Blocking Flow Algorithm; Heuristics and Simpler Data Structures
speakerAffiliation: JGU Mainz
date: 2026-10-30 14:15
duration: 30
city: mainz
---
The binary blocking flow algorithm (BBF) of Goldberg and Rao solves the maximum flow problem with integer capacities bounded by U in O(min(sqrt(m), n^(2/3)) m log n log U) time. Despite its appealing runtime, it is not considered state-of-the-art in terms of practical performance. We introduce several heuristics for speeding up the algorithm for the 2027 DIMACS Implementation Challenge. We also test a variant of BBF by Yijie Han that discards small-capacity edges and sends a fixed amount of flow with every established path. This allows us to replace link-cut trees with the simpler Euler tour trees in the blocking flow computation.
As an even simpler alternative for finding roots of trees, we try a union-find data structure that may need repair when vertices have been deleted in backtracking. Since this data structure does not record the flow that is sent on the edges, we propose an O(m log n) postprocessing algorithm that utilizes a trie-based mergeable dictionary.
As an open research question, we consider the possibility of a theoretical runtime improvement for the blocking flow subroutine despite data structure lower bounds that seem to suggest that computing blocking flows in general might require Omega(m log n) time.

This is joint work with David Laubersheimer.
