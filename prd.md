---
doc: prd
status: approved
---

<!-- Approved state rests on Shannon's October 25, 2026 authorization and her locked
     concept, relayed through Bash. Prepared by her crew from her records. Product
     choices below marked as hers come from her standing rules and locked concept;
     implementation detail is the crew's and is labeled as such in spec.md. -->

# Plain Rules Reader — Product Requirements

One line: a command-line tool that reads a competition or program rules page and answers four questions in short plain sentences, for Shannon and any voice-first reader.
Source: `scope.md > The Unique Kernel`, `scope.md > The Core Loop`, `scope.md > The POC Boundary`.

## The Core Journey

1. Shannon has a rules page to check: a web address someone sent her, a page she saved, or text she copied.
2. She runs the tool with that page: a web address, a file, or pasted text.
3. The tool reads the whole page and looks for four things: what it is, a deadline, a cost or a fee, and who is eligible.
4. It prints four labeled answers, one per line, in short plain sentences.
5. Any answer the page does not contain is printed as a plain not-found line, never a guess.
6. She hears the four answers and decides whether the door is worth entering. The journey ends there; nothing is saved.

## Screens and Layout

One surface: the terminal. There is nothing to look at and nothing to navigate. Output is a short block of text made to be read aloud by a screen reader or a voice: a one-line greeting of what was read, then four labeled lines, then nothing else. Labels are fixed and always in the same order: What it is. Deadline. Cost. Who can enter.

## Look and Feel

Plain spoken English. Short sentences. The answer comes first in each line, evidence after it. No jargon, no abbreviations without expansion, no decoration, no color dependence. Dates are written out in full (October 26, 2026, not 10/26/26) so they hear correctly. This is her standing answer format from `scope.md > Inspiration & Identity`, carried into output.

## Features and Behavior

### Giving it a page

- It accepts a web address (starting http or https) and fetches the page itself.
- It accepts a saved file, either a web page file or a plain text file, and reads it.
- It accepts pasted text, read from standard input when text is piped in or when a flag asks for pasted text.
- A web page is stripped down to its readable text before any answering: navigation, scripts, and styling never reach the answers.

### Finding the four answers

- **What it is:** the page's title, cleaned of site decoration, plus the first real descriptive sentence the page offers about the program.
- **Deadline:** a date that the page ties to a deadline, a closing, or a submission end. If the page gives a time and a time zone with it, those are carried into the answer.
- **Cost:** the tool decides free or fee. Words like "no entry fee", "free to enter", or "no purchase necessary" mean free. A fee amount stated on the page means a fee, and the amount is quoted. If the page says nothing clear about cost, the answer is the not-found line.
- **Who can enter:** the page's own eligibility words, in at most two short sentences: who it is open to, age or residency or membership limits when the page states them.

### Answering plainly

- Every answer line starts with its label and gives the answer first.
- The deadline and cost lines quote the page's own words as evidence after the answer, shortened if long.
- A missing answer prints as: the label, then "I could not find this in the page." Each of the four lines is independent: three found and one missing is a normal result.
- Output is plain text only, safe to read aloud start to finish in under half a minute for a typical page.

Acceptance criteria, checked against real pages during the build:

- [ ] On the Build With AI: Basics rules page, the deadline line names October 26, 2026 and 5:00 PM Eastern, and the cost line says it is free.
- [ ] On a real prize page that charges an entry fee, the cost line says there is a fee and names the amount from the page.
- [ ] On a page with no deadline anywhere, the deadline line is the not-found line, and the other three lines still answer.
- [ ] A web address that cannot be fetched produces one plain error line telling her to paste the text instead, not a crash or a stack trace.

## States and Boundaries

- **No input at all** — the tool prints a short plain usage message: the three ways to give it a page. Nothing else happens.
- **Fetch failure** — one plain error line, and the suggestion to paste the text instead. No partial answers from a page it could not read.
- **Messy page** — if the page text is mostly navigation or the descriptive sentence cannot be found, the What it is line falls back to the page title alone rather than inventing a description.
- **Nothing is kept** — the tool stores nothing between runs: no history, no accounts, no files written. A page goes in, answers come out.

## Product Decisions

- Four fixed questions, always the same four, in the same order. Hers: these are the questions she asks of every door, and a fixed shape is what makes the answer hearable.
- Unknowns are stated, never guessed. Hers: her standing rule is exact facts only, unverified marked plainly.
- A command-line tool, not a web page. Crew recommendation she accepted through the locked concept: one function shows clearest in a terminal, and her agent workflow already lives there.
- No AI model API. Hers: her cost rule bars per-use APIs without a cost conversation. Pattern reading proves the function at zero cost.
- Dates written out in full. Hers: her answers are heard, not seen, and a spoken date must be unambiguous.

## What We're Building

The tool above, complete: three ways in (web address, file, pasted text), page cleaning, four finders, plain labeled answers with honest not-found lines, plain error handling, and automated checks against at least two real rules pages with the outputs kept as evidence.

## Deferred From the POC

- Built-in spoken audio. Deferred because her screen reader and voice tools already read plain text aloud today; audio output is a convenience, not part of proving the function.
- Batch checking of many doors. Deferred because the single-page loop is the kernel; a list runner adds bookkeeping the proof does not need.
- PDF input. Deferred because the doors she checks publish web pages or copyable text; PDF rule books are a later input kind.

## Possible Later Enhancements

A spoken summary mode that adds one line of judgment context from her own records, such as whether a fee door is already ruled out by her no pay to play rule. A save-to-inventory step that files the four answers with the door's record.

## Non-Goals

- It does not judge whether a door is worth entering. It answers four factual questions; the decision stays hers.
- It does not summarize the whole page. Four answers, not a digest.
- It does not fill in, submit, or track any application.

## Open Questions

None that block `4-spec`. The demo video hosting route (YouTube or Vimeo) is a shipping decision for October 26, outside the product.
