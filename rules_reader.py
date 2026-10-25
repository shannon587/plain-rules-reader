#!/usr/bin/env python3
"""Plain Rules Reader.

Reads a competition or program rules page and answers four questions in
short plain sentences: what it is, the deadline, whether it is free or
carries a fee, and who can enter. When an answer is not in the page, the
tool says so plainly instead of guessing.

Python standard library only. No accounts, no keys, no cost.
"""

import re
import sys
from html.parser import HTMLParser


# ---------------------------------------------------------------------------
# Page text cleaning
# ---------------------------------------------------------------------------

class _TextExtractor(HTMLParser):
    """Pulls readable text and the title out of a web page."""

    BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr",
             "br", "section", "article", "header", "footer", "nav", "ul",
             "ol", "table", "blockquote", "pre"}
    SKIP = {"script", "style", "noscript", "svg"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.title_parts = []
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        if tag == "title":
            self._in_title = True
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
        if tag == "title":
            self._in_title = False
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        elif not self._skip:
            self.parts.append(data)


def html_to_text(html):
    """Returns (title, text) for a web page, with markup stripped."""
    parser = _TextExtractor()
    parser.feed(html)
    title = " ".join("".join(parser.title_parts).split())
    lines = []
    for line in "".join(parser.parts).split("\n"):
        line = " ".join(line.split())
        if line:
            lines.append(line)
    return title or None, "\n".join(lines)


def flow(text):
    """One flowing string for sentence-level searching."""
    return " ".join(text.split())


def sentences_of(text):
    """Splits text into sentences, line by line, keeping real ones only.

    Line by line matters: headings sit on their own lines, and flowing the
    whole page into one string would glue headings onto the next sentence.
    """
    found = []
    for line in text.split("\n"):
        line = " ".join(line.split())
        if len(line) < 25:
            continue
        for part in re.split(r"(?<=[.!?])\s+", line):
            part = part.strip()
            if len(part) >= 25:
                found.append(part)
    return found


def evidence_for(sentences, needle):
    """The shortest clean sentence containing a phrase, as evidence."""
    cands = [s for s in sentences
             if needle.lower() in s.lower()
             and "Log in" not in s and "Sign up" not in s]
    if not cands:
        return None
    short = [s for s in cands if len(s) <= 320] or cands
    return shorten(min(short, key=len))


def shorten(text, limit=220):
    """Trims a quote to a hearable length, ending cleanly."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text.rfind(" ", 0, limit)
    return text[:cut].rstrip(",;:") + "."


# ---------------------------------------------------------------------------
# Shared date machinery
# ---------------------------------------------------------------------------

MONTHS = {
    "january": "January", "jan": "January",
    "february": "February", "feb": "February",
    "march": "March", "mar": "March",
    "april": "April", "apr": "April",
    "may": "May",
    "june": "June", "jun": "June",
    "july": "July", "jul": "July",
    "august": "August", "aug": "August",
    "september": "September", "sep": "September", "sept": "September",
    "october": "October", "oct": "October",
    "november": "November", "nov": "November",
    "december": "December", "dec": "December",
}

_MONTH_RE = (r"(?:January|February|March|April|May|June|July|August|"
             r"September|October|November|December|Jan\.?|Feb\.?|Mar\.?|"
             r"Apr\.?|Jun\.?|Jul\.?|Aug\.?|Sep\.?|Sept\.?|Oct\.?|Nov\.?|Dec\.?)")

DATE_RE = re.compile(
    r"\b(?:" + _MONTH_RE + r"\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}"
    r"|\d{1,2}(?:st|nd|rd|th)?\s+" + _MONTH_RE + r"\s+\d{4}"
    r"|\d{1,2}/\d{1,2}/\d{4})\b"
)

TIME_RE = re.compile(r"\b(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))\b")

ZONE_WORDS = ["Eastern", "Pacific", "Mountain", "Central", "Alaska", "Hawaii",
              "EST", "EDT", "CST", "CDT", "MST", "MDT", "PST", "PDT",
              "ET", "PT", "MT", "CT", "GMT", "UTC"]


def plain_date(raw):
    """Writes a found date out in full: October 26, 2026."""
    raw = raw.strip().rstrip(",")
    m = re.match(r"([A-Za-z]+\.?)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})$", raw)
    if m:
        month = MONTHS.get(m.group(1).lower().rstrip("."), m.group(1))
        return "%s %d, %s" % (month, int(m.group(2)), m.group(3))
    m = re.match(r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+\.?)\s+(\d{4})$", raw)
    if m:
        month = MONTHS.get(m.group(2).lower().rstrip("."), m.group(2))
        return "%s %d, %s" % (month, int(m.group(1)), m.group(3))
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})$", raw)
    if m:  # US order: month, day, year.
        names = list(MONTHS.values())
        month = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November",
                 "December"][int(m.group(1)) - 1]
        return "%s %d, %s" % (month, int(m.group(2)), m.group(3))
    return raw


# ---------------------------------------------------------------------------
# The four finders. Each returns (answer, evidence) or None.
# ---------------------------------------------------------------------------

BOILERPLATE = ("eligible", "entrants", "representative", "collectively",
               "reserve the right", "sponsor and administrator")


def find_description(title, text):
    program_words = ("hackathon", "competition", "prize", "program",
                     "programme", "challenge", "grant", "contest",
                     "fellowship", "award", "scholarship", "residency")
    verb_words = (" is ", " are ", " invites ", " seeks ", " offers ",
                  " open to ", " supports ", " funds ")
    clean_title = None
    if title:
        clean_title = re.split(r"\s+[|\-–—]\s+", title)[0].strip().rstrip(".")
        if clean_title.lower() in ("devpost", "submittable", "home"):
            clean_title = None
    if clean_title and len(clean_title) >= 60:
        # A long title already describes the program on its own.
        return (clean_title + ".", None)
    best = None
    for sent in sentences_of(text):
        low = " " + sent.lower() + " "
        if not 40 <= len(sent) <= 280:
            continue
        if any(b in low for b in BOILERPLATE):
            continue
        if any(w in low for w in program_words) and \
                any(v in low for v in verb_words):
            best = sent
            break
    if clean_title and best:
        return ("%s. %s" % (clean_title, best), None)
    if best:
        return (best, None)
    if clean_title:
        return (clean_title + ".", None)
    return None


DEADLINE_STRONG = ("deadline",)
DEADLINE_MEDIUM = ("close", "submit by",
                   "submissions end", "submission period ends", "due by",
                   "entries end", "applications close")
DEADLINE_WEAK = ("ends on", "end date", "last day", "no later than", "due")


def find_deadline(text):
    full = flow(text)
    best = None  # (score, date_match, window)
    for match in DATE_RE.finditer(full):
        start = max(0, match.start() - 220)
        end = min(len(full), match.end() + 140)
        window = full[start:end]
        low = window.lower()
        score = 0
        if any(w in low for w in DEADLINE_STRONG):
            score += 3
        if any(w in low for w in DEADLINE_MEDIUM):
            score += 2
        if any(w in low for w in DEADLINE_WEAK):
            score += 1
        if score and (best is None or score > best[0]):
            best = (score, match, window)
    if best is None:
        return None
    _, match, window = best
    answer = "The deadline is %s" % plain_date(match.group(0))
    tail = full[match.end():match.end() + 80]
    time_match = TIME_RE.search(tail)
    if time_match:
        spoken_time = re.sub(r"\s*(AM|PM)$", r" \1",
                             time_match.group(1).upper())
        answer += ", at %s" % spoken_time
        zone_tail = tail[time_match.end():time_match.end() + 30]
        for zone in ZONE_WORDS:
            if re.search(r"\b" + zone + r"\b", zone_tail):
                answer += " %s time" % zone if zone in (
                    "Eastern", "Pacific", "Mountain", "Central") else " " + zone
                break
    answer += "."
    evidence = evidence_for(sentences_of(text), match.group(0))
    return (answer, evidence if evidence else shorten(window))


FREE_SIGNALS = ("no entry fee", "no submission fee", "no reading fee",
                "no application fee", "no fee to enter", "no fee is required",
                "no fee", "free to enter", "free entry", "entry is free",
                "no purchase necessary", "no purchase or payment necessary",
                "no cost to enter", "there is no fee", "without charge")

FEE_PATTERNS = (
    re.compile(r"([$€£]\s?\d[\d,]*(?:\.\d{2})?)\s*"
               r"(?:submission |entry |reading |application )?fee", re.I),
    re.compile(r"fee[^.!?]{0,30}?([$€£]\s?\d[\d,]*(?:\.\d{2})?)", re.I),
)


def find_cost(text):
    """Free or fee, decided sentence by sentence.

    A fee counts only when an amount and the word fee live in the same
    sentence, so a prize amount near someone else's fee words can never
    be mistaken for the cost of entering.
    """
    sentences = sentences_of(text)
    for sent in sentences:
        low = sent.lower()
        if any(signal in low for signal in FREE_SIGNALS):
            continue
        for pattern in FEE_PATTERNS:
            match = pattern.search(sent)
            if match:
                amount = match.group(1).replace(" ", "")
                answer = ("It costs money to enter. "
                          "The fee listed is %s." % amount)
                return (answer, shorten(sent))
    for signal in FREE_SIGNALS:
        evidence = evidence_for(sentences, signal)
        if evidence:
            return ("It is free to enter.", evidence)
    return None


ELIGIBILITY_STRONG = ("open to", "may enter", "anyone can", "anyone is")
ELIGIBILITY_WORDS = ("eligible", "eligibility", "must be at least",
                     "years of age", "age of majority", "residents of",
                     "reside in", "students", "must be a", "must be an")


def _blocks(text):
    """Heading lines joined with the lines that follow them.

    Rules pages often put a heading like "The Hackathon IS open to:" on
    its own line, with the real words in the list underneath it.
    """
    lines = [" ".join(line.split()) for line in text.split("\n")]
    blocks = []
    for i, line in enumerate(lines):
        if line.endswith(":") and 0 < len(line) <= 80:
            joined = (line + " " + " ".join(lines[i + 1:i + 4])).strip()
            blocks.append(joined)
    return blocks


def find_eligibility(text):
    units = sentences_of(text) + _blocks(text)
    scored = []
    for order, unit in enumerate(units):
        if len(unit) < 40:
            continue
        low = unit.lower()
        score = 0
        if any(w in low for w in ELIGIBILITY_STRONG):
            score += 3
        if any(w in low for w in ELIGIBILITY_WORDS):
            score += 2
        if "not eligible" in low or "are excluded" in low:
            score += 1
        if score:
            scored.append((score, order, unit))
    if not scored:
        return None
    scored.sort(key=lambda item: (-item[0], item[1]))
    chosen = []
    for _, _, unit in scored:
        if any(unit in kept or kept in unit for kept in chosen):
            continue
        chosen.append(unit)
        if len(chosen) == 2:
            break
    answer = " ".join(shorten(unit, 300) for unit in chosen)
    return (answer, None)


# ---------------------------------------------------------------------------
# Plain answers
# ---------------------------------------------------------------------------

NOT_FOUND = {
    "description": "I could not find a description in this page.",
    "deadline": "I could not find a deadline in this page.",
    "cost": "I could not find the cost in this page.",
    "eligibility": "I could not find who can enter in this page.",
}

LABELS = {
    "description": "What it is",
    "deadline": "Deadline",
    "cost": "Cost",
    "eligibility": "Who can enter",
}


def plain_answers(source_label, title, text):
    """Builds the spoken block of four answers."""
    found = {
        "description": find_description(title, text),
        "deadline": find_deadline(text),
        "cost": find_cost(text),
        "eligibility": find_eligibility(text),
    }
    lines = ["Here is what I found in %s, in plain words." % source_label, ""]
    for key in ("description", "deadline", "cost", "eligibility"):
        hit = found[key]
        if hit is None:
            lines.append("%s: %s" % (LABELS[key], NOT_FOUND[key]))
            continue
        answer, evidence = hit
        line = "%s: %s" % (LABELS[key], answer)
        if evidence:
            line += ' The page says: "%s"' % evidence
        lines.append(line)
    return "\n".join(lines)


USAGE = (
    "Plain Rules Reader. Give me a rules page in one of three ways.\n"
    "One: a web address, starting with http.\n"
    "Two: a saved page or text file, by its file name.\n"
    "Three: pasted text, piped in.\n"
    "I will answer four questions in plain words: what it is, the "
    "deadline, whether it is free, and who can enter."
)


def _split_content(raw, name):
    """Turns raw content into (title, text), cleaning web pages."""
    if name.lower().endswith((".html", ".htm")) or \
            "<html" in raw[:500].lower():
        return html_to_text(raw)
    first_line = raw.strip().split("\n", 1)[0].strip()
    title = None
    if first_line and len(first_line) <= 80 and "." not in first_line:
        title = first_line
    return title, raw


def fetch_url(url):
    """Fetches a public web page. Raises ValueError on any failure."""
    import urllib.error
    import urllib.request
    from urllib.parse import urlparse
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (Plain Rules Reader)"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8", errors="ignore")
    except (urllib.error.URLError, OSError, ValueError) as err:
        raise ValueError("fetch failed") from err
    title, text = _split_content(raw, url)
    return title, text, "the page at %s" % urlparse(url).netloc


def read_source(source):
    """Input: a web address or a saved file.

    Returns (title, text, source_label). Raises ValueError when the page
    cannot be read at all, so the caller can answer with one plain line.
    """
    import os
    if source.startswith(("http://", "https://")):
        return fetch_url(source)
    if not os.path.isfile(source):
        raise ValueError("not a file")
    with open(source, "r", encoding="utf-8", errors="ignore") as handle:
        raw = handle.read()
    title, text = _split_content(raw, source)
    return title, text, "the file %s" % os.path.basename(source)


def main(argv):
    raw_args = argv[1:]
    paste = "--paste" in raw_args
    args = [a for a in raw_args if a != "--paste"]
    if paste or (not args and not sys.stdin.isatty()):
        pasted = sys.stdin.read()
        if pasted.strip():
            title, text = _split_content(pasted, "pasted text")
            print(plain_answers("the text you pasted", title, text))
            return 0
        print(USAGE)
        return 2
    if not args:
        print(USAGE)
        return 2
    try:
        title, text, label = read_source(args[0])
    except (ValueError, OSError):
        print("I could not read that page. Please give me a saved page, "
              "a web address, or pasted text instead.", file=sys.stderr)
        return 2
    print(plain_answers(label, title, text))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
