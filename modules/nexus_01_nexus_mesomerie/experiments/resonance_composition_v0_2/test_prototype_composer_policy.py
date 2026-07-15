#!/usr/bin/env python3
import random
import unittest

import prototype_composer_policy as policy


class SameWordComposerPolicyTests(unittest.TestCase):
    def test_proxy_is_lowercase_inside_a_line(self):
        proxy = policy.WishRoleProxy("first-trace", "the first trace", 1)
        self.assertEqual(
            policy._proxy_for_template("Rain leaves room for {wish_word}", proxy),
            "the first trace",
        )

    def test_proxy_is_capitalised_at_line_start(self):
        proxy = policy.WishRoleProxy("first-trace", "the first trace", 1)
        self.assertEqual(
            policy._proxy_for_template("{wish_word} crosses the frame", proxy),
            "The first trace",
        )

    def test_same_word_detection_is_case_insensitive(self):
        self.assertTrue(policy.words_are_identical("Return", "return"))
        self.assertFalse(policy.words_are_identical("Return", "Returning"))

    def test_proxy_choice_is_reproducible(self):
        first = policy.choose_wish_role_proxy(
            policy.DEFAULT_PROXIES, rng=random.Random(9)
        )
        second = policy.choose_wish_role_proxy(
            policy.DEFAULT_PROXIES, rng=random.Random(9)
        )
        self.assertEqual(first, second)

    def test_exact_duplicate_line_is_rejected(self):
        with self.assertRaises(policy.SameWordPolicyError):
            policy.validate_exact_line_repetition(["Open path", "Open path"])


if __name__ == "__main__":
    unittest.main()
