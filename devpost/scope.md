---
doc: scope
status: approved
---

<!-- Approved state rests on Shannon's October 25, 2026 authorization: this is the
     concept she locked, word for word, relayed through Bash. Prepared by her crew
     from her records. Her approval gate for the actual Devpost submission stands. -->

# Plain Rules Reader

One line: a small tool that reads a competition or program rules page and answers four questions in short plain sentences.

## The Unique Kernel

It answers the way Shannon works: short plain sentences, the answer first, and when an answer is not in the page it says so plainly instead of guessing. Plenty of tools summarize. This one is built on her rule: exact facts only, and an honest "I could not find it" beats a smooth invention. The kernel is plain speech plus named unknowns.

## Who It's For

Shannon herself. A legally blind founder who works by voice and enters competitions, grants, fellowships, and programs constantly: her October 2026 inventory holds dozens of live doors. Today, checking one rules page means listening to a long, dense page read top to bottom, or asking an agent and trusting its summary. What she needs is the same four answers every time, in seconds: what is this, when is it due, is it free, and can I enter. Second user: anyone who works by voice or finds dense rules pages hard going.

## The Core Loop

She hands the tool a rules page, either a web address or pasted text. It reads the page and prints four short labeled answers. She hears them and decides on the spot whether the door is worth her time. She comes back because every new door asks the same four questions, and the loop takes seconds instead of a full page read.

## Inspiration & Identity

Her own standing answer format: short plain sentences, lead with the answer, unknowns named out loud. The tone is calm, plain, and spoken, like a good paralegal's memo read aloud. No jargon, no decoration, nothing to look at: the output is the interface, and it is built to be heard.

## Why This Matters to the Learner

This is her accommodation method at its smallest scale. Her project, in her own framing, is AI assistance as a disability accommodation, and her standing need is documents turned into plain spoken answers she can act on. A rules reader is the tool she reaches for at the start of every entry she makes. Building it plan-first, by voice, is also the demonstration: the method is the message.

## What "Working" Looks Like

She runs it on a real rules page and hears four answers she can trust. The proof moment: run it on a page with a hidden entry fee and it says, in one line, that there is a fee and what the fee is. Run it on the Build With AI: Basics rules themselves and it answers with that event's own deadline, its free entry, and who may enter. A page missing one of the four answers gets a plain "I could not find it in this page" for that line, never a guess.

## The POC Boundary

One function, end to end: one rules page in, four plain answers out. Input is a web address, a saved page, or pasted text. Runs as a command-line tool in Python, standard library only, no accounts, no keys, no cost. The four questions are fixed. That is the whole proof of concept.

## Later

- Spoken audio output built in, so the answers are read aloud without a separate step.
- Checking a whole list of doors at once and keeping the answers with her entry inventory.
- Reading PDF rule books as well as web pages.

## Explicitly Cut

- A web page interface. Cut because the terminal is the clearer demo for one function, and her agent workflow already lives there. One function, honestly shown, is the point.
- An AI model API for the reading. Cut under her cost rule: no per-use API without a cost conversation first. Careful pattern reading proves the same function at zero cost, and where a pattern misses, the tool says so.
- Accounts, saved history, and settings. Cut because the loop needs none of them; a page goes in, answers come out, nothing is kept.
