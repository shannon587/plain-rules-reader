"""Checks for Plain Rules Reader, run against real saved rules pages.

Run from the project root: python3 -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import rules_reader as rr

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8",
              errors="ignore") as handle:
        return handle.read()


class BasicsRulesTest(unittest.TestCase):
    """The Build With AI: Basics rules: free, deadline October 26, 2026."""

    @classmethod
    def setUpClass(cls):
        cls.title, cls.text = rr.html_to_text(load("basics-rules.html"))

    def test_deadline_found(self):
        hit = rr.find_deadline(self.text)
        self.assertIsNotNone(hit)
        self.assertIn("October 26, 2026", hit[0])
        self.assertIn("5:00 PM", hit[0])

    def test_cost_is_free(self):
        hit = rr.find_cost(self.text)
        self.assertIsNotNone(hit)
        self.assertIn("free", hit[0].lower())

    def test_description_found(self):
        hit = rr.find_description(self.title, self.text)
        self.assertIsNotNone(hit)
        self.assertTrue(len(hit[0]) > 10)

    def test_eligibility_found(self):
        hit = rr.find_eligibility(self.text)
        self.assertIsNotNone(hit)


class Fc2PrizesTest(unittest.TestCase):
    """The FC2 prizes page text: a $25 fee, closing November 1, 2026."""

    @classmethod
    def setUpClass(cls):
        cls.text = load("fc2-prizes.txt")

    def test_cost_is_the_fee(self):
        hit = rr.find_cost(self.text)
        self.assertIsNotNone(hit)
        self.assertIn("$25", hit[0])
        self.assertIn("costs money", hit[0].lower())

    def test_deadline_found(self):
        hit = rr.find_deadline(self.text)
        self.assertIsNotNone(hit)
        self.assertIn("November 1, 2026", hit[0])

    def test_eligibility_mentions_united_states(self):
        hit = rr.find_eligibility(self.text)
        self.assertIsNotNone(hit)
        self.assertIn("United States", hit[0])


class HonestMissesTest(unittest.TestCase):
    """A page with none of the answers must say so, four times."""

    def test_all_not_found(self):
        text = ("A short note about nothing in particular. "
                "It talks about the weather and a long walk by the river. "
                "Nothing here is a program, a date, a price, or a rule.")
        self.assertIsNone(rr.find_deadline(text))
        self.assertIsNone(rr.find_cost(text))
        self.assertIsNone(rr.find_eligibility(text))
        out = rr.plain_answers("the text you pasted", None, text)
        self.assertIn("I could not find a deadline in this page.", out)
        self.assertIn("I could not find the cost in this page.", out)
        self.assertIn("I could not find who can enter in this page.", out)


if __name__ == "__main__":
    unittest.main()
