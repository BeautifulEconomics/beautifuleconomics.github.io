---
title: The envelope theorem
gloss: When you are already optimising, small changes to the thing you chose cost you nothing to first order.
field: Microeconomic theory
---

## The claim

Suppose you have chosen $x$ to maximise $f(x, a)$, where $a$ is some parameter you do not control — a price, a tax rate, a wage. Call the best value you can achieve $V(a) = \max_x f(x, a)$.

The envelope theorem says that to work out how $V$ responds to a small change in $a$, you can ignore the fact that your optimal $x$ will also shift:

$$\frac{dV}{da} = \frac{\partial f}{\partial a}\bigg|_{x = x^*(a)}$$

Only the direct effect matters. The indirect effect — through the adjustment of $x$ itself — vanishes.

## Why it vanishes

Because you were already at an optimum. At $x^*$, the derivative $\partial f/\partial x$ is zero. So when $x$ shifts a little, $f$ changes by (zero) × (the shift), which is zero to first order. You were standing at the top of the hill; stepping slightly sideways costs nothing measurable.

## What it quietly assumes

That $x^*$ really is an interior optimum where the first-order condition holds with equality, and that $f$ is differentiable there. Both fail more often than textbooks suggest.

## Where it breaks

At a **corner solution** the first-order condition does not hold — you are at the edge of the feasible set, pressed against a constraint, and the derivative is not zero. The indirect effect no longer disappears.

It also gives you only a *first-order* result. For a large change in $a$, the adjustment of $x$ matters a great deal, and the envelope approximation drifts away from the truth.

## Why it is worth knowing

It is the reason Shephard's lemma, Hotelling's lemma and Roy's identity all work, and the reason the derivative of a value function in dynamic programming is tractable at all. Once you see it, a dozen separate results collapse into one idea.
