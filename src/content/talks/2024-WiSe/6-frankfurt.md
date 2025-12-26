---
title: Recent Progress in the Maker-Breaker k-Cycle Game
speakerName: Mathias Sowa
speakerAffiliation: Christian-Albrechts-Universität zu Kiel
date: 2025-01-31 14:15
city: frankfurt
---

Maker-Breaker games are sequential games with perfect information played by two players, called Maker and Breaker. For $n,q \in \mathbb{N}$ and a subgraph $C$ of the complete graph $K_n$ the Maker-Breaker $C$-game is played as follows. Alternately Maker claims an edge and thereafter Breaker claims up to $q$ edges of $K_n$ until every edge has been claimed by one of the two players. If at the end of the game the graph of Maker-edges contains a copy of $C$, Maker wins the game, otherwise Breaker wins.

Bednarska and Łuczak (1999) showed that there exists constants $c_0$ and $c_1$ such that for large enough $n$ Maker has a winning strategy if $q \leq c_0 n^{1/m(C)}$ and Breaker has a winning strategy if $q \geq c_1 n^{1/m(C)}$ where $m(C) = \max_{\substack{H \subseteq C, |V(H)| \geq 3}} \frac{|E(H)|-1}{|V(H)|-2}$. Thus the asymptotics of the game has been determined exactly, but unfortunately the constants implicitly given in the proof of Bednarska and Łuczak are magnitudes apart from each other. For example for the $C_3$ game the constant $c_0$ is smaller than $10^{-5}$ and the constant $c_1$ is larger than $10^4$.

Bednarska and Łuczak conjectured that these constants could be chosen arbitrarily close to each other. This conjecture is open for every graph $C$ which contains a cycle and for the most graphs there are not even good constants known. These constants have a significant meaning: powerful strategies lead to good constants and the smaller the gap between these constants is, the closer the players are to optimal play. In the intensively studied case where $C$ is a cycle of length 3 Chvátal and Erdős (1978) showed that Maker can win the game if $q \leq \sqrt{2}\sqrt{n}$ and Breaker can win if $q \geq 2\sqrt{n}$.

Recently Glazik and Srivastav (2022) introduced a new potential function which gives a winning strategy for Breaker if $q>\sqrt{8/3} \sqrt{n}$, which is considered a breakthrough result. We were able to generalize this potential function concept to cycles of arbitrary length, a class of games for which previously no good strategies with explicit constants were known. We also give a constructive strategy for Maker in the $C_4$-game which leads to the first good constant $c_0$ for this game.
