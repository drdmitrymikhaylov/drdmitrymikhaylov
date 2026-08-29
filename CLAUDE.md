# CLAUDE.md

Guidance for Claude Code (claude.ai/code) and other AI assistants working in this repository.

## What this repository is

`drdmitrymikhaylov/drdmitrymikhaylov` is a **GitHub profile repository**. Because the repository
name matches the account name, GitHub renders its root `README.md` at the top of
https://github.com/drdmitrymikhaylov — it is the first thing anyone visiting the profile sees.

It is **not a software project.** There is no source code, no package manifest, no build system, no
test suite, no CI, and no dependencies. The entire tracked content is:

```
README.md    # the profile page rendered on github.com/drdmitrymikhaylov
CLAUDE.md    # this file
```

Everything below follows from that: the "codebase" is one public-facing Markdown document about a
real person, and the main risks are factual (wrong claim about someone's career) and presentational
(a change that renders badly on the profile), not functional.

## Working rules

1. **Content is biographical and public.** Titles, affiliations, publication counts, citation
   metrics, patent counts and links describe a real person and are visible to employers,
   collaborators and press. Do not invent, embellish, round up, or "improve" any of them. Change a
   fact only when the user states the new value, or when a source they point to states it.
2. **Metrics go stale.** Publication/citation/h-index numbers come from Google Scholar and change
   over time. If asked to refresh them, get the numbers from the user or from the linked profile —
   never estimate or extrapolate from the existing figures.
3. **Preserve the existing voice.** The README is deliberately plain, first-person, understated and
   dense with specifics. It has no badges, no emoji, no images, no animated GIFs, no GitHub-stats
   widgets, no visitor counters, no "🚀 Passionate about..." phrasing. Do not add any of these,
   even as a "nice touch" — the absence is the style.
4. **Match the surrounding formatting exactly** (see the next section) rather than reformatting to
   generic Markdown conventions.
5. **Keep edits scoped.** Editing one bullet means touching that bullet, not restructuring the
   document. Do not add tooling (linters, formatters, GitHub Actions, `.editorconfig`, license
   files) unless explicitly asked — a profile repo needs none of it, and each addition shows up in
   the repository's public file list.
6. **Verify links before adding them.** Every URL in the README is a live identity link (LinkedIn,
   Substack, Google Scholar, ORCID, Wikidata). A broken or wrong link on a profile page is worse
   than a missing one.

## README conventions (derived from the current file)

Follow these when editing; they are what the file actually does, not general Markdown advice.

- **Headings:** one `#` H1 for the name at the top; `###` for every section (`Current`,
  `Research focus`, `Selected output`, `Elsewhere`). `##` is not used at all — do not introduce it.
- **Section dividers:** a `---` horizontal rule after the intro block and before `Elsewhere`.
  Sections are otherwise separated by blank lines only.
- **Header block:** H1 name, then a bold one-line descriptor of roles separated by ` · `, then the
  location on its own line, then a short first-person prose paragraph. Hard-wrapped at roughly
  110 characters; no trailing double-space line breaks.
- **Role entries** (`Current`) use `- **<Role>**, <Organization>` — bold role, comma, plain
  organization. Parenthetical country/entity qualifiers follow the organization name.
- **`Research focus`** is a two-column Markdown table with the header `| Area | What I work on |`
  and the separator `|---|---|` (no alignment colons, no padding to align pipes). Left cell is a
  short domain label; right cell is a sentence fragment, no terminal period.
- **`Selected output`** is a bullet list; multiple statistics on one line are joined with ` · `
  (space, U+00B7 middle dot, space), not commas or pipes.
- **`Elsewhere`** uses bare URLs in the form `- <Name> — <url>`, with an em dash (—) separator and
  **no** Markdown link syntax. Keep it that way for new entries.
- **Punctuation:** em dashes (—) and middle dots (·) are used as-is, not as HTML entities. The file
  is UTF-8 and ends with a single trailing newline.
- **No terminal periods** on list items, table cells, or the header block lines; full prose
  sentences in the intro paragraph do take periods.

## Development workflow

There is nothing to install, build, run, or test. The workflow is: edit `README.md`, verify it
renders, commit, push.

```bash
# See the change
git diff

# Preview the rendered result (any Markdown previewer; GitHub's own renderer is the ground truth)
# At minimum, re-read the raw file and check table pipes and list markers are intact.
```

**Verification before committing** — since there is no test suite, these are the checks:

- The table's header/separator/body rows all have the same number of `|` delimiters.
- No accidental smart-quote or hyphen substitution for the ` · ` and ` — ` separators.
- Every added or edited URL resolves.
- The file still ends with exactly one newline.

**Git conventions:**

- Existing history uses short, imperative, GitHub-web-style subjects (`Create README.md`,
  `Update README.md`). Keep commit subjects short and imperative; a slightly more descriptive
  subject (e.g. `Update citation metrics`) is fine and preferable when the change has a specific
  purpose.
- Default branch is `main`. Work on a feature branch and push with
  `git push -u origin <branch-name>`; do not push directly to `main` without being asked.
- Do not open a pull request unless the user explicitly asks for one.

## When asked to "add a project" or expand the profile

Common requests on a profile repo are to feature pinned projects, add a publications section, or
link out to work. Prefer adding a section that matches the existing conventions above (a `###`
heading plus a list or two-column table) over importing a template from another profile README.
Ask the user for the actual content — project names, links, descriptions — rather than filling a
section with plausible-sounding placeholders.
