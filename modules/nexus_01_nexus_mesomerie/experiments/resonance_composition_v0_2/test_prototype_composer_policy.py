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

    def test_first_trace_is_weighted_as_default(self):
        self.assertGreater(
            policy.DEFAULT_PROXIES[0].weight,
            policy.DEFAULT_PROXIES[1].weight,
        )

    def test_exact_duplicate_line_is_rejected(self):
        with self.assertRaises(policy.SameWordPolicyError):
            policy.validate_exact_line_repetition(["Open path", "Open path"])

    def test_all_supported_relation_echoes_have_six_words(self):
        for text, _echo_id in policy.SUPPORTED_RELATION_ECHOES.values():
            with self.subTest(text=text):
                self.assertEqual(policy.base._word_count(text), 6)

    def test_all_supported_remainder_echoes_have_four_words(self):
        for text, _echo_id in policy.SUPPORTED_REMAINDER_ECHOES.values():
            with self.subTest(text=text):
                self.assertEqual(policy.base._word_count(text), 4)

    def test_proxy_echo_movements_keep_line_two_at_four_words(self):
        proxy = policy.WishRoleProxy("first-trace", "the first trace", 1)
        for movement in policy.PROXY_MOVEMENT_BY_WISH_BLOCK.values():
            text = f"{proxy.text} {movement}"
            with self.subTest(text=text):
                self.assertEqual(policy.base._word_count(text), 4)

    def test_each_supported_wish_block_has_a_distinct_echo_movement(self):
        self.assertEqual(
            set(policy.PROXY_MOVEMENT_BY_WISH_BLOCK.values()),
            {"crosses", "waits", "enters", "follows"},
        )

    def test_selected_role_lookup_returns_exact_block_id(self):
        block = policy.base._SelectedBlock(
            role="relation",
            data={"id": "relation.direction.02"},
            rendered_text="Their separate currents share one direction",
        )
        self.assertEqual(
            policy._selected_id_for_role((block,), "relation"),
            "relation.direction.02",
        )

    def test_selected_role_lookup_rejects_missing_role(self):
        with self.assertRaises(policy.base.PrototypeCompositionError):
            policy._selected_id_for_role((), "relation")


if __name__ == "__main__":
    unittest.main()
