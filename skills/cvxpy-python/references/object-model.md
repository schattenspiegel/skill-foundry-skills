# Symbolic and curvature model

Expressions have shape, sign, and curvature. CVXPY's analyzer composes known
atoms under a ruleset; mathematically convex code can be rejected when its form
does not prove curvature. Rewrite to an equivalent recognized atom instead of
assuming the analyzer is wrong.

DCP accepts minimization of a convex expression or maximization of a concave
expression. Equality constraints are affine on both sides; inequality direction
must compare convex to concave in the allowed orientation. Other disciplines
such as DGP and DQCP have separate construction and solve flags—use them only
when the problem actually belongs to that class.

Scalar shape is `()`. `(n,)` and `(n, 1)` are not interchangeable at every
boundary. CVXPY follows many NumPy shape rules but bans some broadcasting. Use
`.shape`, `.ndim`, `.size`, and tests around matrix/vector interfaces.

Attributes can inform sign/curvature analysis and reduce representation. An
equivalent explicit constraint records a dual; an attribute does not. Choose
based on analysis and downstream evidence, not terseness.
