---
speakerName: Alexander Leonhardt
title: Fine-Grained Complexity of a Reduction Scheme for Domination
speakerAffiliation: Goethe-Universität Frankfurt
date: 2025-12-05 14:15
duration: 30
city: darmstadt
---
The Dominating Set_k problem asks whether a graph G = (V, E) contains a set D of size at most k such that every node is either in D or has at least one neighbor in D.
This talk explores the fine-grained complexity of applying the classical reduction Rule $1$ introduced by Alber, Fellows and Niedermeier [JACM '04] and its generalization, Rule $k$ [SOFSEM '06].
These reductions are key tools used in practical solvers and for obtaining kernels on restricted graph classes.
    
Along the way, we first identify a subproblem for which a solution is necessary in order to apply Rule k, and prove almost tight upper and lower bounds for it.

Additionally, we show that the recently proposed |V| + |E| time algorithm for Rule 1 [ALENEX '26] admits high parallelization, including a constant-time parallel algorithm that is work-optimal for dense graphs if one has access to n^2 processors in a CRCW PRAM model.
