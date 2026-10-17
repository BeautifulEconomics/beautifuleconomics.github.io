# Beautiful Economics

The website behind beautifuleconomics.in. Static site, built by GitHub Pages
from the files in this repository. No server, no database, no monthly bill.

Everything you write lives as a plain text file. If you ever leave GitHub,
you take these files with you and nothing is lost.

---

## 1. Point beautifuleconomics.in at it

The site is already live at https://beautifuleconomics.github.io

Your domain currently forwards to Facebook. You will replace that forwarding
with real DNS records, at whoever you bought the domain from (BigRock,
GoDaddy, Namecheap, Hostinger — look for "DNS", "Manage DNS" or "Name Server
settings").

**First remove** any existing forwarding/redirect rule, and any A or CNAME
record on `@` and `www`. They will conflict.

**Then add these.** Source: GitHub's own documentation, linked at the bottom.

| Type  | Name / Host | Value                          |
|-------|-------------|--------------------------------|
| A     | `@`         | `185.199.108.153`              |
| A     | `@`         | `185.199.109.153`              |
| A     | `@`         | `185.199.110.153`              |
| A     | `@`         | `185.199.111.153`              |
| AAAA  | `@`         | `2606:50c0:8000::153`          |
| AAAA  | `@`         | `2606:50c0:8001::153`          |
| AAAA  | `@`         | `2606:50c0:8002::153`          |
| AAAA  | `@`         | `2606:50c0:8003::153`          |
| CNAME | `www`       | `beautifuleconomics.github.io` |

The CNAME value has no `https://` and no repository name.

DNS takes anywhere from ten minutes to a few hours. Once GitHub shows a green
tick under Settings to Pages, tick **Enforce HTTPS**. Do not skip that —
without it the padlock is missing and browsers will warn people.

## 2. Write an article

Make a new file in `_posts/`. The filename must be
`YYYY-MM-DD-some-words.md` — Jekyll reads the date from the name, so a wrong
filename means the post silently does not appear.

```markdown
---
title: "What inflation actually is"
standfirst: "One sentence under the headline. Shown on the homepage too."
date: 2026-11-02 09:00:00 +0530
reading: "5 min"
---

Write normally. Blank line between paragraphs.

## A heading looks like this

**Bold**, *italic*, and [a link](https://example.com).
```

Commit it. The homepage, the Writing page, the RSS feed and the sitemap all
update themselves.

## 3. Add a concept

Same idea, in `_concepts/`. No date in the filename — the filename becomes the
web address, so `price-elasticity.md` lives at `/concepts/price-elasticity/`.

```markdown
---
title: Price elasticity
gloss: How much the quantity people buy responds when the price moves.
field: Microeconomics
---

## The claim
...
## The assumption underneath
...
## Where it stops working
...
```

Keep those three headings. They are what makes this different from every other
economics glossary on the internet — most tell you what an idea says, almost
none tell you where it fails.

The homepage picks one concept per day automatically. Add more and the rotation
gets longer on its own.

## 4. Add a PDF

1. Put the file in `assets/library/`.
2. Add an entry to `_data/library.yml`:

```yaml
- title: "Game theory in one sitting"
  file: /assets/library/game-theory-in-one-sitting.pdf
  pages: 14
  size: "1.2 MB"
  note: "One or two sentences on what is inside."
```

Keep files under about 25 MB.

## 5. Switch on the newsletter

The signup form is already built and currently shows a reminder instead. To
make it live, pick a provider and paste its form address into
`newsletter_action` in `_config.yml`.

**Buttondown** — simplest, free to 100 subscribers. Sign up, then
Settings to Embedding. Use:

```yaml
newsletter_action: "https://buttondown.email/api/emails/embed-subscribe/YOURNAME"
newsletter_field: "email"
```

**MailerLite** — free to 1,000 subscribers, better for a larger list. Create an
embedded form, copy the `action="..."` URL out of the code it gives you, and
set `newsletter_field` to the matching field name (usually `fields[email]`).

Whichever you pick, **export your subscriber list every few months** and keep
the file. That list is the only asset here that cannot be rebuilt.

---

## What this cannot do

No accounts, no login, no paid membership, no private area. GitHub Pages serves
files; it does not run code and has no database. There is no plugin or trick
that changes this.

When you genuinely need those — meaning people are asking for them, not before
— the move is **Ghost**. It does blogging, memberships, login and email
newsletters in one piece of software, imports Markdown files and subscriber
lists directly, and costs roughly 400 to 900 rupees a month self-hosted. Your
domain and all of this writing carry over untouched.

## Things that will break, and why

- **A post does not appear.** The filename is wrong. It must be
  `YYYY-MM-DD-title.md`, with real hyphens.
- **The whole site goes blank after an edit.** You broke the block between the
  two `---` lines at the top of a file. Colons and apostrophes inside a title
  need the title wrapped in "double quotes".
- **The custom domain stops working.** Check the `CNAME` file still exists in
  the repository. Some editors delete it.
- **A plugin does not work.** GitHub Pages only runs a fixed list of plugins.
  This site uses three that are on it: jekyll-feed, jekyll-sitemap,
  jekyll-seo-tag. Adding others will fail the build.

## Where things are

```
_config.yml        site-wide settings — title, links, newsletter
_posts/            articles
_concepts/         the concepts dictionary
_data/library.yml  the list of downloadable PDFs
_layouts/          page skeletons
_includes/         reused fragments, including the hero plot
assets/css/        the single stylesheet
assets/library/    PDF files
CNAME              your domain. Do not delete.
```

Sources: [Managing a custom domain for your GitHub Pages site](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) and [Securing your GitHub Pages site with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
