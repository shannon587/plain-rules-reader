---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast — chosen by the crew under Shannon's October 25, 2026 authorization. She does not operate the terminal herself; her hands-on checkpoints are the presentation session with Bash on October 26, 2026, where she hears the results and gives feedback before anything submits. Mechanical verification and commits still happen at every slice, and her boxes below stay unchecked until she has actually done them.

## Slices

- [x] **1. Give it a saved rules page and hear the four answers**
  Becomes usable: The tool reads a saved rules page (web page file or text file) and prints the four labeled answers in plain sentences, with honest not-found lines.
  Why now: This is the kernel, first: page in, four plain answers out. The saved-page path also becomes the test bed every later slice relies on, and it cannot be broken by a network failure during the demo.
  PRD ref: `prd.md > The Core Journey`, `prd.md > Features and Behavior`
  Spec ref: `spec.md > Components`, `spec.md > File Structure`
  Build: Create rules_reader.py with Page Text Cleaning, The Four Finders, and Plain Answers; wire the file-input path from Input. Save two real rules pages as test fixtures. Add unittest checks against the fixtures.
  Verify (mechanical): Run the unit tests; run the tool on the Build With AI: Basics rules fixture and confirm the deadline line names October 26, 2026 with 5:00 PM Eastern and the cost line says free; run it on the fee-charging prize fixture and confirm the cost line names the fee.
  Learner check: At the October 26 presentation, hear the four answers for both fixture pages and say whether they sound like answers she can act on.
  Commit: `Read a saved rules page and answer four plain questions`

- [x] **2. Give it a live web address**
  Becomes usable: The tool fetches a rules page from a web address itself and answers from what it fetched; an unreachable address produces one plain error line and the paste suggestion.
  Why now: The web address is how doors actually reach her, so the loop is not real until this works. It is also the riskiest path (sites refuse fetches), so it goes second while the saved-page path is already proven underneath it.
  PRD ref: `prd.md > Features and Behavior` (Giving it a page), `prd.md > States and Boundaries`
  Spec ref: `spec.md > Components` (Input), `spec.md > Important Failure Modes`
  Build: Add the web-address path to Input: fetch with a browser user agent and a 20 second limit, hand the result to Page Text Cleaning, and route every fetch failure to the single plain error line.
  Verify (mechanical): Run the tool on a live rules page address and confirm four answers or one plain error line, never a crash; run it on an unreachable address and confirm the plain error line.
  Learner check: At the presentation, hear the live-address result and the failure result read aloud.
  Commit: `Fetch a rules page from a web address`

- [x] **3. Paste text straight in**
  Becomes usable: Text piped or pasted in gets the same four answers, and running the tool with nothing gives the short plain usage message.
  Why now: Pasted text is the fallback for every page the fetch cannot read, so it completes the loop the failure modes promise. It is small and safe to add last.
  PRD ref: `prd.md > Features and Behavior` (Giving it a page), `prd.md > States and Boundaries`
  Spec ref: `spec.md > Components` (Input, Plain Answers)
  Build: Add standard-input reading (piped text, or the --paste flag) and the no-input usage message in Plain Answers.
  Verify (mechanical): Pipe fixture text in and confirm the four answers; run with no input and confirm the usage message and a clean exit.
  Learner check: At the presentation, hear the usage message read aloud and confirm it tells her the three ways in, in plain words.
  Commit: `Accept pasted text and print plain usage`

## Hands-on Checkpoints

- [ ] Early usable behavior explored — combined with the final review at the October 26 presentation session with Bash (single session for a three-slice build; she hears slice results there and gives feedback before any submission)
- [ ] Final kick-the-tires exploration and feedback completed — October 26 presentation session

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship (scheduled: October 26 presentation with Bash; nothing submits before this box can honestly be checked)

Crew mechanical final verification runs at the end of the build session and is recorded under Revisions if anything deviates. Learner confirmation is separate and still owed.

## Code Tour and App Map

- [ ] Learning activity complete — focused alternative for an experienced plan-first learner: trace one question (the deadline) from input to printed line through the code
- [ ] Optional edit and transfer reflection addressed — offered at the October 26 presentation; personal reflection, if any, belongs in the ignored learner profile
- [x] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: focused alternative, worked from the build's one real failure. The first version of the cost finder answered the FC2 prizes page with its $15,000 prize as the entry fee. The written acceptance criterion in `prd.md > Features and Behavior` (on a fee page, the cost line names the fee) and the automated check against the real page (`tests/test_rules_reader.py`, Fc2PrizesTest.test_cost_is_the_fee) caught it. The finder was rebuilt to decide fees sentence by sentence (`rules_reader.py`, find_cost); the same check now passes, and `evidence/smoke-test-3-fc2-fee-page.txt` shows the correct $25 answer. The interactive walkthrough of this trace with Shannon is scheduled for the October 26 presentation, so the learning activity box stays unchecked until then.
Route and stops: reference route in `devpost/app-map.html`: `read_source` and `fetch_url` (input), `find_cost` (the fee decision), `plain_answers` (the four lines), in rules_reader.py.
Edit outcome: not applicable (no learner edit made; one is offered at the presentation).
Reflection: offered at the October 26 presentation; not yet answered.
Activity mode: focused alternative (experienced plan-first learner; crew-built under her authorization).

## Revisions
