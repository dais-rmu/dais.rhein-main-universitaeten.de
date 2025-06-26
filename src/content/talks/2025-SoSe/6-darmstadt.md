---
speakerName: Jan van den Brand
title: The Structural Complexity of Matrix-Vector Multiplication
speakerAffiliation: Georgia Institute of Technology
date: 2025-07-11 14:15
duration: 30
city: darmstadt
---
Computing sequential matrix-vector products is one of the most 
fundamental subroutines underlying efficient algorithms for learning, 
optimization, computational geometry, online algorithms, and many other 
fields. We consider the problem of preprocessing an $n\times n$ matrix 
$M$, and then supporting queries that for any vector $v$ returns the 
matrix-vector product $Mv$ faster than naive matrix-vector-multiplication.
This problem has been extensively studied in both theory and practice, 
revealing a gap in our complexity understanding: on one side, 
practitioners have developed algorithms that are highly efficient in 
practice, whereas on the other side, theoreticians have proven that the 
problem cannot be solved faster than naive multiplication in the 
worst-case. This lower bound holds even in the average-case, implying 
that the existing typical average-case analyses cannot explain this gap 
between theory and practice. Hence, we study the problem for 
\emph{structured} matrices.
We show that for $n\times n$ matrices of VC-dimension $d$, the 
matrix-vector multiplication problem can be solved with $\tilde{O}(n^2)$ 
preprocessing and $\tilde{O}(n^{2-1/d})$ query time.  Given the low 
constant VC-dimensions observed in most real-world data, our results 
posit an explanation for why the problem can be solved so much faster in 
practice.
Joint work with: Emile Anand and Rose McCarty

