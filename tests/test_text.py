import unittest

from fake_sublime import load_plugin, support

load_plugin()
text = support("text")


class TextTransformTest(unittest.TestCase):
	def test_local_macro(self):
		self.assertEqual(text.local_macro("x"), "`x'")

	def test_global_macro_toggles(self):
		self.assertEqual(text.toggle_global_macro("x"), "${x}")  # issue #37: one letter
		self.assertEqual(text.toggle_global_macro("${x}"), "x")
		self.assertEqual(text.toggle_global_macro("${xy}"), "xy")
		self.assertEqual(text.toggle_global_macro("$"), "${$}")
		self.assertEqual(text.toggle_global_macro(""), "${}")

	def test_block_comment_toggles(self):
		self.assertEqual(text.toggle_block_comment("x"), "/* x */")  # issue #37
		self.assertEqual(text.toggle_block_comment("/* x */"), "x")
		self.assertEqual(text.toggle_block_comment("/*x*/"), "x")
		self.assertEqual(text.toggle_block_comment("/**/"), "")
		self.assertEqual(text.toggle_block_comment("/*/"), "/* /*/ */")
		self.assertEqual(text.toggle_block_comment(""), "/*  */")

	def test_as_code_terminates_last_line(self):
		self.assertEqual(text.as_code(["reg y x"]), "reg y x\n")
		self.assertEqual(text.as_code(["a\n", "b"]), "a\nb\n")


class BlockBoundsTest(unittest.TestCase):
	# 0         1         2
	# 0123456789012345678901234
	# a\nMARK\nb\nc\nMARK\nd\n
	markers = [(2, 7), (11, 16)]

	def test_no_markers_is_whole_file(self):
		self.assertEqual(text.block_bounds([], 3, 10), (0, 10))

	def test_first_block(self):
		self.assertEqual(text.block_bounds(self.markers, 0, 18), (0, 2))

	def test_middle_block(self):
		self.assertEqual(text.block_bounds(self.markers, 8, 18), (7, 11))

	def test_last_block_after_final_marker(self):
		self.assertEqual(text.block_bounds(self.markers, 17, 18), (16, 18))

	def test_caret_on_marker_belongs_to_next_block(self):
		self.assertEqual(text.block_bounds(self.markers, 3, 18), (7, 11))


if __name__ == "__main__":
	unittest.main()
