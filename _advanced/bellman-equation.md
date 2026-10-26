---
title: The Bellman equation
gloss: A problem stretching over all of time, rewritten as the same small problem faced once, again and again.
field: Dynamic optimisation
---

## The claim

A decision taken today changes what you can do tomorrow. Choosing a whole path at once — consumption in every year of a life, say — looks impossibly large.

Bellman's insight is that you do not have to. Define $V(s)$ as the best you can do from state $s$ onward. Then

$$V(s) = \max_{a} \; \Big\{ u(s, a) + \beta \, \mathbb{E}\big[V(s')\big] \Big\}$$

Today's payoff, plus the discounted value of wherever today's choice leaves you. One infinite problem becomes one finite problem, repeated.

## The principle underneath

Whatever you did to arrive at $s$, the remainder of an optimal plan must itself be optimal from $s$ onward. The past is a sunk fact; only the state matters. This is why sunk costs are irrelevant to the next decision, stated as mathematics rather than as advice.

## What it quietly assumes

That the state really does capture everything relevant about the past. Write down too small a state and the equation is simply false: the problem is no longer Markov, and today's best choice depends on history you have thrown away.

It also assumes the future is discounted ($\beta < 1$) and payoffs are bounded, which is what makes the operator a contraction and guarantees a unique $V$.

## Where it breaks

**Habits, learning and reputation** all carry the past forward. Each must be added to the state, and the state grows.

**The curse of dimensionality.** Each extra state variable multiplies the space to be searched. Problems that are elegant on paper become numerically brutal with four or five dimensions.

**Time-inconsistent preferences.** Under hyperbolic discounting, the "you" of next year disagrees with the plan the "you" of today would choose. There is no single $V$ for everyone to agree on, and the standard machinery quietly stops applying.
