---
speakerName: Annika Jäger
title: Handling Symmetry while Preserving Problem Structure for Mixed-Binary Linear Problems
speakerAffiliation: TU Darmstadt
date: 2026-03-20 14:15
duration: 30
city: darmstadt
---
In highly symmetric instances of optimization problems, symmetry creates large classes of equivalent solutions that all get explored separately when symmetry is disregarded.
Symmetry handling aims to eliminate this inefficiency by reducing the size of these equivalence classes.

In this talk, a symmetry handling method for mixed-binary linear problems is presented that ensures that no two remaining solutions are symmetric.
This method consists of a presolving routine that iteratively applies operations derived from so-called Schreier-Sims tables.
Throughout the talk, the maximum stable set problem serves as a running example to illustrate the presolving routine.
One advantage of handling symmetry via a presolving routine is that it does not interfere with the subsequent solving process.
Moreover, this particular presolving also preserves the problem structure, thereby enabling existing black-box solvers to be applied directly.

This is joint work with Marc Pfetsch. 
