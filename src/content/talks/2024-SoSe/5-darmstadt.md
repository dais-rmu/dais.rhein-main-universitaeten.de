---
speakerName: Anna Zych-Pawlewicz
title: Randomization techniques for online bipartite matching
speakerAffiliation: University of Warsaw
speakerURL: https://www.mimuw.edu.pl/~anka/
room: "Raum S3|13/30 | Schloss Kaisersaalbau, Marktplatz 15, 64283 Darmstadt"
date: 2024-07-12 13:00
city: darmstadt
mapURL: https://maps.app.goo.gl/cQd2XPLfYMWVdMAn6
---

In the online bipartite matching problem, a bipartite graph G=(S, C, E) is revealed in the online manner. While all the vertices in S, also called servers, are known to the algorithm from the beginning, the vertices of C are revealed in an online fashion one vertex at the time. Upon its arrival, the client presents all the edges that are adjacent to it. The algorithm must then either match the client to one of its neighbors, or leave it unmatched forever. The goal of the algorithm is to maximize the size of the matching even though the future is
unknown. This is a very fundamental problem with applications to online advertisement, combinatorial auctions and economy. The usual measure of performance for an online algorithm is the worst possible ratio (called the competitive ratio) of the size of the matching produced by the algorithm to the optimum offline matching. It is not hard to see that a deterministic cannot beat the ratio of 1/2 and there is a very simple deterministic algorithm achieving this ratio.

In 1990, Karp, Vazirani and Vazirani proposed the celebrated ranking algorithm for this problem. Over the years, the analysis of the ranking algorithm was gradually simplified to become a textbook example of the primal-dual analysis. The primal-dual analysis for this problem opened the toolbox that allows to attack more general variants of online bipartite matching: the edge arrival model, and the two-sided vertex arrival model. Surprisingly, the edge arrival model turns out substantially more difficult than the vertex arrival model. In this talk, we present a survey of these results and the basic techniques behind them.
