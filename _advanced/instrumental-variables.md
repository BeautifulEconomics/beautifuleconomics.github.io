---
title: Instrumental variables
gloss: A way to recover a causal effect when the thing you care about is tangled up with what you cannot see.
field: Econometrics
---

## The problem it solves

You want the causal effect of $X$ on $Y$. You run a regression and get a number. The number is wrong, because something unobserved moves both — ability affects both schooling and wages, so the schooling coefficient is contaminated.

## The claim

Find a variable $Z$ that moves $X$ but affects $Y$ through no other route. Then the part of $X$ that $Z$ explains is clean of the contamination, and regressing $Y$ on *that* part recovers the causal effect.

## The two conditions

1. **Relevance.** $Z$ genuinely shifts $X$. This is testable, and you should test it.
2. **Exclusion.** $Z$ affects $Y$ *only* through $X$. This is **not testable**. It is an assumption you argue for, in words, and your reader is entitled to disbelieve you.

## Where it breaks

**A weak instrument is worse than none.** If $Z$ barely moves $X$, the estimator is badly biased — biased *towards* the ordinary regression you were trying to escape — and the standard errors mislead you about how little you know. The first-stage F-statistic is not a formality.

**The exclusion restriction usually fails quietly.** Distance to the nearest college shifts schooling, but it also tracks what kind of place you grew up in, which affects earnings directly. Nothing in the data will tell you this. Only an argument will.

**You are not estimating the average effect.** With heterogeneous effects, what comes back is a local average treatment effect — the effect on the people whose behaviour the instrument actually changed. That may not be the group the policy question is about.

## The honest summary

Instrumental variables do not remove the need for an untestable assumption. They relocate it, from one you cannot defend to one you can argue about in the open. That is a real gain, and it is smaller than it is often made to sound.
