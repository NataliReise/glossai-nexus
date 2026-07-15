import random
import unittest

from same_word_policy import (
    SameWordPolicyError,
    WishRoleProxy,
    choose_wish_role_proxy,
    validate_exact_line_repetition,
    words_are_identical,
)


class SameWordPolicyTests(unittest.TestCase):
    def test_casefold_identity(self):
        self.assertTrue(words_are_identical("Return", "return"))
        self.assertTrue(words_are_identical("Nähe", "NÄHE"))
        self.assertFalse(words_are_identical("Return", "Returning"))

    def test_proxy_choice_is_reproducible(self):
        proxies = [
            WishRoleProxy("first-trace", "the first trace", 3),
            WishRoleProxy("opening-trace", "the opening trace", 1),
        ]
        first = choose_wish_role_proxy(proxies, rng=random.Random(12))
        second = choose_wish_role_proxy(proxies, rng=random.Random(12))
        self.assertEqual(first, second)

    def test_empty_proxy_pool_rejected(self):
        with self.assertRaises(SameWordPolicyError):
            choose_wish_role_proxy([])

    def test_exact_duplicate_rejected(self):
        with self.assertRaises(SameWordPolicyError):
            validate_exact_line_repetition("one line\none line")

    def test_explicit_reprise_allowed(self):
        validate_exact_line_repetition(
            "one line\none line", explicit_reprises=["one line"]
        )

    def test_parallel_nonidentical_lines_allowed(self):
        validate_exact_line_repetition(
            "Distance begins to answer\nDistance continues to answer"
        )

    def test_blank_lines_ignored(self):
        validate_exact_line_repetition("one line\n\nanother line")


if __name__ == "__main__":
    unittest.main()
