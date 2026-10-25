# Smoke Test Evidence

Runs made on October 25, 2026, on the build machine, against real rules pages. Full raw outputs are in this folder.

## Test 1: Build With AI: Basics rules, saved page

File: smoke-test-1-basics-saved-page.txt. The tool read a saved copy of the event's own rules page and answered all four questions correctly:

- What it is: the event's own title and description line.
- Deadline: October 26, 2026, at 5:00 PM EDT, matching the rules.
- Cost: free, with the page's own words: "NO PURCHASE OR PAYMENT NECESSARY TO ENTER OR WIN."
- Who can enter: the rules' own eligibility words, both who is in and who is not.

## Test 2: Build With AI: Basics rules, live web address

File: smoke-test-2-basics-live-url.txt. The tool fetched the live page itself and produced the same four correct answers. An unreachable address was also tried: the tool printed one plain error line suggesting a saved page or pasted text, and stopped. No crash.

## Test 3: FC2 prizes page, a page that charges a fee

File: smoke-test-3-fc2-fee-page.txt. The page charges for entry, and the tool caught it in one line: "It costs money to enter. The fee listed is $25." It also found the closing date (November 1, 2026) and the eligibility words. This page matters because it also names a $15,000 prize. During the build, an early version of the cost finder wrongly reported the prize as the fee. The finder was rebuilt to decide fee questions sentence by sentence, and this test is the proof it now answers correctly.

## Automated checks

Eight unit tests run against the same real pages plus a page with none of the answers, which must and does produce four honest not-found lines. Run them with: python3 -m unittest discover -s tests

## Known limits, stated plainly

- The reading is pattern matching. A deadline or fee written in an unusual shape can be missed, and then the tool prints its not-found line rather than guessing.
- A numeric date like 11/01/2026 is read in US order: month, day, year.
- Some sites refuse the fetch or show their words only through JavaScript. Then the tool asks for pasted text instead.
