"""Test the README update/verify logic used by the GitHub Action."""

import re


START = "<!-- compat-matrix-start -->"
END = "<!-- compat-matrix-end -->"


def _update_readme(readme: str, report: str) -> str:
    """Inject report between markers (mirrors action/action.yml update step)."""
    return re.sub(
        f"^{re.escape(START)}.*?^{re.escape(END)}",
        f"{START}\n{report}\n{END}",
        readme, flags=re.DOTALL | re.MULTILINE,
    )


def _verify_readme(readme: str, report: str) -> bool:
    """Check if README markers match the report (mirrors action/action.yml verify step)."""
    current = re.search(f"^{re.escape(START)}(.*?)^{re.escape(END)}", readme, re.DOTALL | re.MULTILINE)
    current_text = current.group(1).strip() if current else ""
    return current_text == report.strip()


SAMPLE_REPORT = (
    "| Platform | Min Standard | Examples |\n"
    "|----------|-------------|----------|\n"
    "| stm32    | c++11       | 4/4      |\n"
)

README_WITH_MARKERS = (
    "# My Library\n\n"
    f"{START}\nold content\n{END}\n\n"
    "More text.\n"
)

README_WITHOUT_MARKERS = "# My Library\n\nNo markers here.\n"


class TestReadmeUpdate:

    def test_replaces_content_between_markers(self):
        result = _update_readme(README_WITH_MARKERS, SAMPLE_REPORT)
        assert SAMPLE_REPORT in result
        assert "old content" not in result

    def test_preserves_surrounding_text(self):
        result = _update_readme(README_WITH_MARKERS, SAMPLE_REPORT)
        assert "# My Library" in result
        assert "More text." in result

    def test_markers_preserved(self):
        result = _update_readme(README_WITH_MARKERS, SAMPLE_REPORT)
        assert START in result
        assert END in result

    def test_no_markers_unchanged(self):
        result = _update_readme(README_WITHOUT_MARKERS, SAMPLE_REPORT)
        assert result == README_WITHOUT_MARKERS

    def test_empty_report(self):
        result = _update_readme(README_WITH_MARKERS, "")
        assert "old content" not in result
        assert START in result
        assert END in result

    def test_only_first_marker_pair_replaced(self):
        """If the README has an example showing the markers (a second pair),
        only the first (real) pair should be replaced. The example must stay intact."""
        readme = (
            "# My Library\n\n"
            f"{START}\nold content\n{END}\n\n"
            "## How to use\n\n"
            f"Add `{START}` and `{END}` markers to your README where you want the table.\n"
        )
        result = _update_readme(readme, SAMPLE_REPORT)
        assert "old content" not in result
        assert SAMPLE_REPORT in result
        # The example text must be preserved verbatim — not expanded into a matrix.
        assert f"Add `{START}` and `{END}` markers" in result


class TestReadmeVerify:

    def test_matching_content_passes(self):
        readme = _update_readme(README_WITH_MARKERS, SAMPLE_REPORT)
        assert _verify_readme(readme, SAMPLE_REPORT) is True

    def test_stale_content_fails(self):
        assert _verify_readme(README_WITH_MARKERS, SAMPLE_REPORT) is False

    def test_no_markers_fails(self):
        assert _verify_readme(README_WITHOUT_MARKERS, SAMPLE_REPORT) is False

    def test_whitespace_tolerance(self):
        """Trailing whitespace differences shouldn't cause verify to fail."""
        readme = _update_readme(README_WITH_MARKERS, SAMPLE_REPORT)
        report_with_trailing = SAMPLE_REPORT + "\n\n"
        assert _verify_readme(readme, report_with_trailing) is True

    def test_different_report_fails(self):
        readme = _update_readme(README_WITH_MARKERS, SAMPLE_REPORT)
        different = SAMPLE_REPORT.replace("4/4", "3/4")
        assert _verify_readme(readme, different) is False
