"""Unit tests for leonardo.py encode/decode and tattle behavior.

Run locally with:
  python3 -m unittest discover \\
    -s /Users/jack.reis/Documents/dancer/plugins/ai-agency/leonardo/skills/leonardo \\
    -p 'test_*.py' -v
"""

import importlib.util
import re
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Load leonardo.py as a module without requiring packaging.
MODULE_PATH = Path(__file__).with_name("leonardo.py")
spec = importlib.util.spec_from_file_location("leonardo", MODULE_PATH)
leonardo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(leonardo)


class DecodeRoundTripTests(unittest.TestCase):
    def test_encode_then_extract_sentinel_decodes_to_original(self):
        original = "hello world"
        encoded = leonardo.encode_text(original)
        m = re.search(leonardo.SENTINEL_RE, encoded)
        self.assertIsNotNone(m, "encoded output should contain a sentinel")
        self.assertEqual(leonardo.decode_string(m.group(1)), original)

    def test_decode_string_inverts_encode_string(self):
        self.assertEqual(leonardo.decode_string(leonardo.encode_string("hello")), "hello")


class EncodeTextTests(unittest.TestCase):
    def test_plain_text_wrapped_in_sentinel(self):
        self.assertEqual(leonardo.encode_text("secret"), "__protected__:terces:__end__")

    def test_date_prefix_kept_readable(self):
        out = leonardo.encode_text("2026-04-20 secret stuff")
        self.assertTrue(out.startswith("2026-04-20 "))
        self.assertIn("__protected__:", out)
        self.assertIn(":__end__", out)
        # The date itself must not appear reversed anywhere in the output.
        self.assertNotIn("02-40-6202", out)

    def test_iso_datetime_prefix_kept_readable(self):
        out = leonardo.encode_text("2026-04-20T14:30 payload")
        self.assertTrue(out.startswith("2026-04-20T14:30 "))
        self.assertIn("__protected__:daolyap:__end__", out)


class EncodeFilenameTests(unittest.TestCase):
    def test_extension_preserved_and_stem_reversed(self):
        out = leonardo.encode_filename("secret.md")
        self.assertTrue(out.endswith(".md"))
        self.assertIn("__protected__:terces:__end__", out)

    def test_dotless_filename_whole_name_wrapped(self):
        self.assertEqual(leonardo.encode_filename("README"), "__protected__:EMDAER:__end__")

    def test_multi_dot_filename_only_final_suffix_is_extension(self):
        # "notes.draft.md" -> stem="notes.draft" reversed="tfard.seton", ext="md"
        out = leonardo.encode_filename("notes.draft.md")
        self.assertTrue(out.endswith(".md"))
        self.assertIn("__protected__:tfard.seton:__end__", out)


class DecodeFilenameTests(unittest.TestCase):
    def test_decode_sentinel_filename_preserves_extension(self):
        self.assertEqual(
            leonardo.decode_filename("__protected__:terces:__end__.md"),
            "secret.md",
        )

    def test_decode_sentinel_filename_no_extension(self):
        self.assertEqual(
            leonardo.decode_filename("__protected__:EMDAER:__end__"),
            "README",
        )

    def test_decode_non_sentinel_filename_falls_back_to_stem_reverse(self):
        self.assertEqual(leonardo.decode_filename("terces.md"), "secret.md")


class TattleDispatchTests(unittest.TestCase):
    """Verify tattle_to_discord fires exactly once per encode/decode invocation in main()."""

    def _run_main(self, argv):
        mock_run = MagicMock(return_value=MagicMock(returncode=0))
        with patch.object(leonardo.sys, "argv", ["leonardo.py"] + argv), \
             patch.object(leonardo.subprocess, "run", mock_run):
            leonardo.main()
        return mock_run

    def test_encode_text_tattles_once(self):
        mock_run = self._run_main([
            "secret", "--mode", "encode",
            "--reason", "test", "--caller", "unittest",
        ])
        self.assertEqual(mock_run.call_count, 1)

    def test_encode_filename_tattles_once(self):
        mock_run = self._run_main([
            "secret.md", "--mode", "encode", "--kind", "filename",
            "--reason", "test", "--caller", "unittest",
        ])
        self.assertEqual(mock_run.call_count, 1)

    def test_decode_sentinel_text_tattles_once(self):
        mock_run = self._run_main([
            "__protected__:terces:__end__",
            "--reason", "test", "--caller", "unittest",
        ])
        self.assertEqual(mock_run.call_count, 1)

    def test_decode_filename_tattles_once(self):
        mock_run = self._run_main([
            "__protected__:terces:__end__.md", "--kind", "filename",
            "--reason", "test", "--caller", "unittest",
        ])
        self.assertEqual(mock_run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
