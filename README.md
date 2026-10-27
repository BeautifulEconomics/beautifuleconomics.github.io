# Running Beautiful Economics

This page is your manual. It is not part of the website — only you see it,
and it is here every time you open this repository.

**The one address to remember:**

```
github.com/BeautifulEconomics/beautifuleconomics.github.io
```

Bookmark it. Everything below starts from there.

---

## The rule that never changes

Whatever you are doing — adding, editing, deleting — it is always the same
three steps:

1. **Open the file** (or start a new one).
2. **Type.**
3. **Scroll down and press the green `Commit changes` button**, then confirm.

Wait about a minute and the change is live on beautifuleconomics.in.

That is it. There is nothing else to learn. The rest of this page is just
*which* file, for *which* job.

---

## Where everything lives

When you open the repository you see a list of folders. This is what they are:

| Folder | What is inside |
| --- | --- |
| `_concepts` | One file per concept. The Concepts page builds itself from these. |
| `_advanced` | One file per Advanced Economics entry. |
| `_posts` | One file per piece of writing. |
| `_data` | The word list, the thought list, the Library listing. |
| `assets/library` | The actual PDF files. |
| `_config.yml` | Site settings: your links, the newsletter, the shop. |
| `about.md` | The About page. |

Ignore every other folder. You will never need to touch them.

---

## Add a new concept

1. Open the repository.
2. Click the **`_concepts`** folder.
3. Click **`Add file`** (top right) → **`Create new file`**.
4. In the filename box type the name, lower case, hyphens instead of spaces,
   ending in `.md` — for example `price-elasticity.md`.
5. Paste this in and write over it:

```
---
title: Price elasticity
gloss: How much people change what they buy when the price moves.
field: Microeconomics
---

## The claim

What the idea says, in plain language.

## What it assumes

The thing the idea quietly takes for granted.

## Where it breaks

The case where it stops working.
```

6. Press **`Commit changes`**.

The three lines between the `---` marks are settings, not writing:

- **title** — shown everywhere on the site.
- **gloss** — the one-line summary. Keep it to one sentence.
- **field** — the topic. Type anything; it creates that topic. Keep the
  spelling consistent, because `Macroeconomics` and `macroeconomics` would
  count as two different topics.

**The filename becomes the web address.** `price-elasticity.md` becomes
`beautifuleconomics.in/concepts/price-elasticity/`. Choose it carefully —
changing it later breaks every link anyone has shared.

---

## Add an Advanced Economics entry

Exactly the same, but click the **`_advanced`** folder instead of `_concepts`.

Advanced entries can contain mathematics. Write it between dollar signs:

- Inside a sentence: `$x^2 + y^2 = z^2$`
- On its own line: `$$V(s) = \max_a \{ u(s,a) + \beta V(s') \}$$`

It is turned into proper typeset mathematics automatically. This only works
in `_advanced`, which is why it exists as its own section.

---

## Write a new piece

1. Click the **`_posts`** folder.
2. **`Add file`** → **`Create new file`**.
3. **The filename must start with the date**: `YYYY-MM-DD-some-title.md`,
   for example `2026-11-03-why-prices-are-information.md`.
4. Paste this in:

```
---
title: "Why prices are information"
standfirst: "One sentence that makes someone want to read on."
date: 2026-11-03 09:00:00 +0530
reading: "6 min"
---

Your first paragraph.

Your second paragraph.

## A heading partway through

More writing.
```

5. **`Commit changes`**.

Notes:

- The date in the filename and the date inside must match. Leave `+0530` alone.
- Writing below the second `---` is ordinary text. Blank line between
  paragraphs. `## ` starts a heading. `**bold**`, `*italic*`,
  `[the words](https://the-address.com)` for a link.
- **A piece dated in the future stays hidden until that date arrives.** Use
  this on purpose: write three on Sunday, date them across the week, and they
  publish themselves.

---

## Put a PDF in the Library

This is the only job that takes **two** steps.

**Step one — upload the file.**

1. Click **`assets`**, then **`library`**.
2. **`Add file`** → **`Upload files`**.
3. Drag the PDF in. Give it a simple lower-case name with hyphens, like
   `game-theory-in-one-sitting.pdf`.
4. **`Commit changes`**.

**Step two — tell the site about it.**

1. Go back to the top, click **`_data`**, then **`library.yml`**.
2. Click the **pencil icon** (top right) to edit.
3. Add this at the bottom, keeping the two-space indents exactly:

```
- title: "Game theory in one sitting"
  file: /assets/library/game-theory-in-one-sitting.pdf
  pages: 14
  size: "1.2 MB"
  note: "What a dominant strategy is, and why the prisoner's dilemma is not about prisoners."
```

4. **`Commit changes`**.

The `file:` line must match the uploaded filename exactly. A file uploaded but
not listed will not appear. A listing with no file gives a broken download.

---

## Edit something that already exists

1. Click the folder, then click the file.
2. Click the **pencil icon** at the top right.
3. Change what you want.
4. **`Commit changes`**.

That works for every file on this page — a concept, a piece, the About page,
the word list, the settings.

---

## Delete something

1. Click the folder, then the file.
2. Click the **`...`** button at the top right.
3. Choose **`Delete file`**.
4. **`Commit changes`**.

It disappears from the site in about a minute. Anyone who had the link will
get a "page not found", so think before deleting something you have shared.

---

## Add more words and thoughts

These are the two pools the site draws from each day. Adding to them means you
never have to write anything *on* the day.

**Word of the day** — `_data` → `words.yml`, pencil icon, add at the bottom:

```
- term: "Seigniorage"
  meaning: "The profit a government makes simply by creating money."
```

If the word already has a concept page, add a third line and a link to it
appears automatically:

```
  link: "opportunity-cost"
```

**Thought of the day** — `_data` → `thoughts.yml`:

```
- text: "Two or three sentences. Plain words. One idea."
  who: "Whose idea it is"
  what: "economist"
  source: "The book or essay, and the year"
```

**The `source` line is not optional.** An entry without one is silently
skipped and never shown. That is deliberate: it means you cannot accidentally
publish a claim you cannot back up.

---

## Change the settings

`_config.yml`, pencil icon. The things you are likely to want:

| Line | What it does |
| --- | --- |
| `facebook:` `instagram:` `youtube:` | The links in the footer. Empty hides that one. |
| `email:` | Your contact address. Leave empty until it actually receives mail. |
| `newsletter_action:` | Paste your email provider's form address here and the subscribe box appears everywhere. |
| `shop:` and `shop_label:` | A link to a shop, for when you sell something. |

---

## What you never have to touch

These change on their own, for ever:

- **Word of the day**, **Thought of the day**, **Concept of the day** — daily,
  at each reader's own midnight, wherever they are in the world.
- **Newly published research** — every Monday, from the American Economic
  Review and Econometrica.
- The greeting, dark mode, the date in the footer, the sitemap.

You never edit these. You only add to the pools they draw from.

---

## The four things that break it

Almost every problem is one of these.

**1. A colon in an unquoted line.** The most common by far.
`title: Inflation: a short history` breaks the build. Wrap it in quotes:
`title: "Inflation: a short history"`.

**2. Wrong indentation in `_data` files.** The first line of an entry starts
with `- ` and every line under it starts with exactly **two spaces**. Tabs are
not spaces.

**3. A missing `---` line.** Every concept, Advanced entry and piece needs
`---` above and below its settings. Three hyphens, nothing else on the line.

**4. A piece whose filename has no date.** It silently never appears.

### How you will know

If your change does not show up, click the **`Actions`** tab at the top of the
repository.

- **Green tick** — it published.
- **Red cross** — the build failed. Click it, and the error names the file and
  the line number.

**A failed build never takes the site down.** The last good version stays live.
A mistake means "my change did not appear", never "my site is gone".

---

## Checking it worked

Wait a minute, then open the site with a number on the end so your browser
does not show you an old copy:

```
beautifuleconomics.in/?x=1
```

Change the number each time you check.

---

## Undoing anything

Every change you have ever made is saved with its date, and any of it can be
reversed.

1. Click **`Commits`** (or the clock icon) on the repository home page.
2. Click the change you want to undo.
3. Press the **`...`** button at the top right and choose **`Revert`**.

That creates a new change putting things back. Nothing is lost, and you can
undo the undo.

**There is nothing you can type into these files that cannot be reversed in
under a minute.** Edit freely. The worst case is that a change does not appear
and the previous version stays up.
