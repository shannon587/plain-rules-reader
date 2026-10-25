# Plain Rules Reader

Plain Rules Reader reads a competition or program rules page and answers four questions in short plain sentences:

1. What it is.
2. The deadline.
3. Whether it is free, or carries a fee, and what the fee is.
4. Who can enter.

When an answer is not in the page, the tool says so plainly: "I could not find it in this page." It never guesses. It was built by Shannon Watson, a legally blind founder who works by voice, as the smallest working piece of her method: turn a dense document into plain spoken answers she can act on.

## Requirements

Python 3. Nothing to install. The tool uses only the Python standard library, so there are no packages, no accounts, and no keys.

## How to run it

Give it a rules page in one of three ways.

A web address:

```
python3 rules_reader.py https://learn-ai-basics.devpost.com/rules
```

A saved page or text file:

```
python3 rules_reader.py basics-rules.html
python3 rules_reader.py fc2-prizes.txt
```

Pasted text, piped in:

```
cat rules.txt | python3 rules_reader.py
```

Run it with nothing and it prints a short usage message in plain words.

## What the output looks like

Real output, from the FC2 prizes page (a page that charges a fee):

```
Here is what I found in the file fc2-prizes.txt, in plain words.

What it is: Prizes. The FC2 Catherine Doctorow Innovative Fiction Prize is open to writers of, from, or in the United States writing in English with at least three books published.
Deadline: The deadline is November 1, 2026. The page says: "They will close 1 November 2026."
Cost: It costs money to enter. The fee listed is $25. The page says: "Include a $25 submission fee."
Who can enter: The FC2 Catherine Doctorow Innovative Fiction Prize is open to writers of, from, or in the United States writing in English with at least three books published. Translations and previously published or self-published works are not eligible, although shorter works that have previously appeared in magazines or anthologies may be included in collections, provided that the collection as a whole is unpublished.
```

More runs, including the Build With AI: Basics rules read from a saved page and from the live address, are kept in the `evidence/` folder.

## How it reads

The tool strips a web page down to its readable text, then runs four small finders over it: one for a description, one for a deadline date (a date the page ties to a deadline or a closing), one for cost (free words, or a fee amount stated beside the word fee, decided sentence by sentence so a prize amount is never mistaken for a fee), and one for eligibility words. Each finder either brings back what the page says, with the page's own words quoted as evidence, or brings back nothing, which prints as an honest not-found line.

## Honest limits

- The reading is pattern matching, not a language model. Unusual phrasing can be missed, and a miss prints as a not-found line, never a guess.
- A numeric date such as 11/01/2026 is read in US order: month, day, year.
- Some sites refuse the fetch or show their words only through JavaScript. The tool then prints one plain error line and asks for pasted text instead.
- Nothing is stored between runs: no history, no accounts, no files written.

## Tests

```
python3 -m unittest discover -s tests
```

The checks run against real saved rules pages in `tests/fixtures/`, plus a page with none of the answers, which must produce four not-found lines.

## How it was planned and built

This project was built plan-first with the Devpost Learn Skill Pack: a scope, a product requirements document, and a technical spec were written before any code. They live in the `devpost/` folder and are mirrored at the top of this repo as `scope.md`, `prd.md`, and `spec.md`. The build checklist, with every step verified and committed, is in `devpost/checklist.md`.

## License

MIT. See `LICENSE`.
