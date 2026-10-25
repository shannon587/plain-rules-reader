---
doc: spec
status: approved
---

<!-- Approved state rests on Shannon's October 25, 2026 authorization and her locked
     concept. Technical choices here are crew recommendations sized to the proof of
     concept and consistent with her standing rules (zero cost, no API keys, no
     accounts). They are labeled as crew decisions in Decisions and Open Issues. -->

# Plain Rules Reader — Technical Spec

## How This Works, In Plain Language

The tool is one small Python program. You hand it a rules page in one of three ways: a web address, a saved file, or pasted text. If it is a web page, the program first washes it down to plain text, the way you would strip the menus and buttons off a page and keep only the words. Then four finders read the text. Each finder hunts for one answer: a description, a deadline date, a cost or a fee, and the eligibility words. Each finder either brings back what the page actually says, with the page's own words as evidence, or brings back nothing. A printer then lays out the four answers in fixed order, in short plain sentences, and turns any empty finder into an honest line: I could not find this in the page. Nothing is saved, nothing phones home, and there is no AI model and no key: the reading is careful pattern matching, which is why it costs nothing and works the same every time.

## The Core Journey Through the System

PRD ref: `prd.md > The Core Journey`.

1. The user runs the command with a web address, a file path, or piped text → the **Input** component decides which kind it got and produces raw content plus a source label.
2. Raw web content goes through **Page Text Cleaning**, which turns page markup into clean readable text and keeps the page title.
3. The cleaned text goes to the four finders in **The Four Finders**: Description, Deadline, Cost, Eligibility. Each returns an answer or nothing.
4. **Plain Answers** formats the four results into the fixed labeled block, writing dates out in full and quoting page evidence after the answer.
5. The user sees, or hears, the four lines. If the input could not be read at all, she gets one plain error line and the paste-it-instead suggestion instead.

## Stack

- Python 3.12, standard library only. No packages to install. Modules: `argparse`, `re`, `sys`, `urllib.request`, `urllib.error`, and `html.parser`. Documentation: https://docs.python.org/3/library/
- Tests: Python's built-in `unittest`, same documentation site. Fixtures are real saved rules pages under `tests/fixtures/`.
- Rationale: standard library only means zero cost, zero keys, zero setup for anyone who clones the repo, and the demo runs identically anywhere. Tradeoff accepted: pattern reading can miss unusual phrasing, and the tool says so instead of guessing (her rule).

## Where It Runs and How Someone Tries It

Runs locally, on the command line, anywhere Python 3 is installed. No server, no deployment.

- Web address: `python3 rules_reader.py https://example.com/rules`
- Saved page or text file: `python3 rules_reader.py page.html` or `python3 rules_reader.py rules.txt`
- Pasted text: `cat rules.txt | python3 rules_reader.py` or `python3 rules_reader.py --paste < rules.txt`
- No arguments and no piped text: prints the plain usage message and stops.

For the demo recording: run it live in a terminal on two real rules pages (saved copies, so the recording cannot be broken by a network failure), showing the four answers appearing for each. Submission needs this video plus the public repo; deployment is optional and not used.

## Look and Feel

Terminal text only. A one-line header naming what was read, then four labeled lines in fixed order, then nothing. Short sentences, dates in full, no abbreviations that read badly aloud, no color or formatting dependence. Implements `prd.md > Look and Feel`.

## Components

### Input

Decides what it was given: a web address (starts with http), an existing file path, or pasted text from standard input. Fetches a web address with a plain browser user agent and a 20 second limit. Produces raw content and a short source label ("the page at that address", "the file rules.txt", "the text you pasted"). Any failure becomes one plain error line from **Plain Answers**, not a crash.
PRD ref: `prd.md > Features and Behavior` (Giving it a page).

### Page Text Cleaning

Turns web page markup into readable text using the standard library HTML parser. Keeps the page title separately. Skips scripts, styles, and hidden elements. Collapses runs of whitespace, keeps sentence boundaries, and keeps lines long enough to be real content separate from menu fragments.
PRD ref: `prd.md > Features and Behavior` (Giving it a page).

### The Four Finders

Four small functions over the cleaned text. Shared helpers: split text into sentences, find date patterns (month-name dates, day-month-year dates, and numeric dates), and search windows of text around a match.

- **Description finder:** page title, cleaned of site suffixes, plus the first sentence long enough to be real content that talks about the program (mentions a hackathon, competition, prize, program, challenge, grant, or similar word).
- **Deadline finder:** every date on the page is a candidate; candidates near deadline words (deadline, closes, closing, due, submit by, submissions end, last day) score highest. Carries a stated time and time zone into the result when the page prints them beside the date.
- **Cost finder:** decides free or fee. Free signals: "no entry fee", "no fee", "free to enter", "no purchase necessary", "no cost to enter". Fee signals: a money amount near the words fee, entry, enter, submit, or cost. A stated fee amount wins over free signals only when it is clearly an entry fee; a prize amount is never a fee (prize words near the amount disqualify it).
- **Eligibility finder:** sentences containing open-to or eligible language, age limits, residency, student or membership limits. At most two sentences, the most direct ones.

Each finder returns the answer plus the page's own evidence words, or nothing.
PRD ref: `prd.md > Features and Behavior` (Finding the four answers).

### Plain Answers

Formats the four results in fixed label order: What it is. Deadline. Cost. Who can enter. Writes dates out in full. Quotes shortened evidence after the answer. Turns an empty result into the not-found line for that label. Also owns the usage message and the single plain error line for unreadable input.
PRD ref: `prd.md > Features and Behavior` (Answering plainly), `prd.md > States and Boundaries`.

## Data Model

No stored data. In memory only, for the length of one run:

- `source_label`: short words for where the page came from.
- `title`: the cleaned page title, or nothing.
- `text`: the cleaned full text.
- `answers`: four slots (description, deadline, cost, eligibility), each either a pair of (plain answer, evidence) or empty.

When the run ends, everything is gone.

## File Structure

```
plain-rules-reader/
├── rules_reader.py          # the whole tool: input, cleaning, finders, answers
├── tests/
│   ├── fixtures/            # real saved rules pages used as test evidence
│   └── test_rules_reader.py # built-in unittest checks against the fixtures
├── evidence/                # kept run outputs from the smoke tests on real pages
├── devpost/                 # planning workspace: profile (private, ignored), scope, prd, spec, checklist, app map
├── scope.md                 # mirror of devpost/scope.md for the submission repo
├── prd.md                   # mirror of devpost/prd.md
├── spec.md                  # mirror of devpost/spec.md
├── README.md
├── LICENSE                  # MIT
└── .gitignore
```

## External Services and Dependencies

None. The only outward act is fetching the public web page the user names, over HTTPS, with no key, no account, and no cost. Pasted text and files need no network at all.

## Important Failure Modes

- **The page refuses the fetch or needs JavaScript to show its words** → one plain error line and the suggestion to paste the text instead. No partial answers from an unread page.
- **A deadline is written in a shape the patterns do not know** → the deadline line is the honest not-found line. A missed date is a known limit of pattern reading, named in the README.
- **A prize amount sits near fee words and fools the cost finder** → guarded by the prize-word disqualifier in the cost finder; the smoke tests include a fee page and a free page to keep this honest.

## What Was Simplified and Why

- **Pattern reading** instead of an AI model — her cost rule bars a per-use API without a cost conversation, and patterns prove the function at zero cost. The fuller version would call a model for the reading, at per-use cost, and would still need the same honest not-found behavior.
- **One file** instead of a package — the whole tool is one function deep; one file keeps the demo and the code tour to a single place. The fuller version would split components into modules once a second function exists.
- **Standard library HTML cleaning** instead of a readability library — no dependencies to install or break. The fuller version would use a dedicated extractor for messier pages.

## Decisions and Open Issues

- Crew decision: Python standard library only, one file, command line first. Reason: zero cost, zero setup, clearest one-function demo. Tradeoff: pattern reading misses some phrasings; accepted, and the tool names a miss instead of guessing.
- Her decisions carried in, not reopened: the four fixed questions, the plain-sentence output with named unknowns, no AI model API, dates in full. Sources: `prd.md > Product Decisions`.
- One genuine uncertainty, and how it gets checked: whether careful pattern reading answers honestly enough on real, messy rules pages. Investigation agreed for the build: smoke-test on at least two real rules pages (one free event, one fee-charging prize), keep the raw outputs in `evidence/`, and let the results either confirm the approach or name its limits in the README.
- Open at ship time, not a build blocker: the demo video hosting route (YouTube or Vimeo) is chosen when Shannon approves the package on October 26.
