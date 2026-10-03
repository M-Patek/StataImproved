"""Pure text transformations used by the editor commands (no Sublime API)."""

# Every break line inserted by the plugin contains this token; blocks are the
# text between such lines. Kept for compatibility with existing do-files.
BLOCK_MARKER = "piu_sign"


def local_macro(word):
	"""x -> `x'"""
	return "`" + word + "'"


def toggle_global_macro(word):
	"""x -> ${x}, and ${x} -> x."""
	if len(word) >= 3 and word.startswith("${") and word.endswith("}"):
		return word[2:-1]
	return "${" + word + "}"


def toggle_block_comment(text):
	"""x -> /* x */, and /* x */ (or /*x*/) -> x."""
	if len(text) >= 4 and text.startswith("/*") and text.endswith("*/"):
		inner = text[2:-2]
		if inner.startswith(" "):
			inner = inner[1:]
		if inner.endswith(" "):
			inner = inner[:-1]
		return inner
	return "/* " + text + " */"


def block_bounds(marker_lines, pos, size):
	"""Return (begin, end) of the block that contains `pos`.

	`marker_lines` is a sorted list of (begin, end) regions of the break lines,
	`end` including the line's trailing newline. A caret on a break line
	belongs to the block below it.
	"""
	begin, end = 0, size
	for line_begin, line_end in marker_lines:
		if line_begin <= pos:
			begin = line_end
		else:
			end = line_begin
			break
	return begin, max(begin, end)


def as_code(chunks):
	"""Join code chunks into do-file text that Stata executes completely.

	Stata ignores a last line that is not terminated by a newline.
	"""
	return "\n".join(chunk.rstrip("\n") for chunk in chunks) + "\n"
