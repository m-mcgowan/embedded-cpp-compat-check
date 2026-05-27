from compat_check.site.readme import generate_summary_table


def test_generate_summary_table_full_support():
    results = [
        {"platform": "esp32", "standard": "c++17", "feature": "cpp17/optional", "status": "supported"},
        {"platform": "esp32", "standard": "c++17", "feature": "cpp17/variant", "status": "supported"},
    ]
    table = generate_summary_table(results)
    assert "esp32" in table
    assert "**C++17 / 100%**" in table


def test_effective_support_color_emoji():
    """High/mid/low pct gets 🟢/🟡/🔴 prefix in the Effective Support column."""
    # High (100%) → green
    results_high = [
        {"platform": "p", "standard": "c++17", "feature": "f1", "status": "supported"},
    ]
    assert "🟢 **C++17 / 100%**" in generate_summary_table(results_high)

    # Mid (50%) → yellow
    results_mid = [
        {"platform": "p", "standard": "c++17", "feature": "f1", "status": "supported"},
        {"platform": "p", "standard": "c++17", "feature": "f2", "status": "unsupported"},
    ]
    assert "🟡 **C++17 / 50%**" in generate_summary_table(results_mid)

    # Low (0%) → red
    results_low = [
        {"platform": "p", "standard": "c++17", "feature": "f1", "status": "unsupported"},
    ]
    assert "🔴 **C++17 / 0%**" in generate_summary_table(results_low)


def test_generate_summary_table_partial_support():
    results = [
        {"platform": "avr", "standard": "c++17", "feature": "cpp17/optional", "status": "supported"},
        {"platform": "avr", "standard": "c++17", "feature": "cpp17/variant", "status": "unsupported"},
    ]
    table = generate_summary_table(results)
    assert "**C++17 / 50%**" in table


def test_generate_summary_table_no_support():
    results = [
        {"platform": "avr", "standard": "c++20", "feature": "cpp20/concepts", "status": "unsupported"},
    ]
    table = generate_summary_table(results)
    assert "**C++20 / 0%**" in table


def test_peak_standard_breaks_ties_by_highest():
    """When multiple standards tie at the peak %, the highest standard is shown."""
    results = [
        {"platform": "esp32", "standard": "c++11", "feature": "f1", "status": "supported"},
        {"platform": "esp32", "standard": "c++17", "feature": "f1", "status": "supported"},
        {"platform": "esp32", "standard": "c++20", "feature": "f1", "status": "supported"},
    ]
    table = generate_summary_table(results)
    assert "**C++20 / 100%**" in table
    assert "**C++11 / 100%**" not in table
    assert "**C++17 / 100%**" not in table


def test_peak_standard_shows_best_not_latest():
    """If a later standard is worse than an earlier one, the earlier (peak) is shown."""
    results = [
        {"platform": "avr", "standard": "c++11", "feature": "f1", "status": "supported"},
        {"platform": "avr", "standard": "c++11", "feature": "f2", "status": "supported"},
        {"platform": "avr", "standard": "c++17", "feature": "f1", "status": "supported"},
        {"platform": "avr", "standard": "c++17", "feature": "f2", "status": "unsupported"},
    ]
    table = generate_summary_table(results)
    assert "**C++11 / 100%**" in table


def test_recipe_row_labeled_polyfill_and_grouped_with_baseline():
    """avr-uno and avr-uno+recipe produce two rows, the recipe one labeled +polyfill,
    grouped adjacent with baseline above."""
    results = [
        # baseline: low support
        {"platform": "avr-uno", "standard": "c++17", "feature": "f1", "status": "supported"},
        {"platform": "avr-uno", "standard": "c++17", "feature": "f2", "status": "unsupported"},
        # recipe: full support
        {"platform": "avr-uno+recipe", "standard": "c++17", "feature": "f1", "status": "supported"},
        {"platform": "avr-uno+recipe", "standard": "c++17", "feature": "f2", "status": "supported"},
    ]
    table = generate_summary_table(results)
    # baseline row
    assert "| avr-uno |" in table
    assert "**C++17 / 50%**" in table
    # recipe row
    assert "avr-uno +polyfill" in table
    assert "**C++17 / 100%**" in table

    # Recipe row must appear after its baseline row (adjacent grouping)
    baseline_pos = table.index("| avr-uno |")
    recipe_pos = table.index("avr-uno +polyfill")
    assert baseline_pos < recipe_pos


def test_recipe_row_uses_base_platform_meta(tmp_path):
    """A +recipe slug should render using the base platform's name/board from meta."""
    from types import SimpleNamespace
    meta = {
        "avr-uno": SimpleNamespace(name="AVR Arduino Uno", board_family="ATmega328P")
    }
    results = [
        {"platform": "avr-uno+recipe", "standard": "c++17", "feature": "f1", "status": "supported"},
    ]
    table = generate_summary_table(results, platform_meta=meta)
    # Full platform name + +polyfill label + ATmega328P board shown
    assert "AVR Arduino Uno +polyfill" in table
    assert "ATmega328P" in table


from pathlib import Path
import textwrap
import pytest


@pytest.fixture
def tiers_yaml(tmp_path):
    """Minimal tiers.yaml with two tentpoles for c++17."""
    p = tmp_path / "tiers.yaml"
    p.write_text(textwrap.dedent("""
        cpp17:
          tentpoles:
            - id: optional
              name: std::optional
              required: [__cpp_lib_optional]
            - id: variant
              name: std::variant
              required: [__cpp_lib_variant]
        cpp20:
          tentpoles:
            - id: concepts
              name: Concepts
              required: [__cpp_concepts]
        """))
    return p


def test_usable_column_appears_when_tiers_provided(tiers_yaml):
    results = [
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/optional", "macro": "__cpp_lib_optional", "status": "supported"},
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/variant", "macro": "__cpp_lib_variant", "status": "supported"},
    ]
    table = generate_summary_table(results, tiers_path=tiers_yaml)
    assert "Usable C++" in table
    # Two tentpoles both complete: "**C++17: 2✅**"
    assert "**C++17: 2" in table


def test_usable_column_omitted_when_no_tiers():
    results = [
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/optional", "macro": "__cpp_lib_optional", "status": "supported"},
    ]
    table = generate_summary_table(results)
    assert "Usable C++" not in table


def test_usable_column_mixed_status(tiers_yaml):
    """Variant missing → one complete + one unsupported."""
    results = [
        {"platform": "rp2040", "standard": "c++17",
         "feature": "cpp17/optional", "macro": "__cpp_lib_optional", "status": "supported"},
        {"platform": "rp2040", "standard": "c++17",
         "feature": "cpp17/variant", "macro": "__cpp_lib_variant", "status": "unsupported"},
    ]
    table = generate_summary_table(results, tiers_path=tiers_yaml)
    # "**C++17: 1✅ 1❌**"
    assert "1✅" in table
    assert "1❌" in table


def test_usable_column_preview_higher_std(tiers_yaml):
    """When a higher std also has tentpoles, it appears as a non-bold preview."""
    results = [
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/optional", "macro": "__cpp_lib_optional", "status": "supported"},
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/variant", "macro": "__cpp_lib_variant", "status": "supported"},
        {"platform": "esp32", "standard": "c++20",
         "feature": "cpp20/concepts", "macro": "__cpp_concepts", "status": "unsupported"},
    ]
    table = generate_summary_table(results, tiers_path=tiers_yaml)
    # Headline c++17 is bold; c++20 preview appears after " · "
    assert "**C++17:" in table
    assert " · C++20:" in table


def test_usable_column_links_to_platform_std_section(tiers_yaml):
    """When site_url is set, the std prefix in each Usable C++ cell links to that std's section."""
    results = [
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/optional", "macro": "__cpp_lib_optional", "status": "supported"},
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/variant", "macro": "__cpp_lib_variant", "status": "supported"},
        {"platform": "esp32", "standard": "c++20",
         "feature": "cpp20/concepts", "macro": "__cpp_concepts", "status": "unsupported"},
    ]
    table = generate_summary_table(
        results, tiers_path=tiers_yaml,
        site_url="https://example.com/repo",
    )
    # Each std label is wrapped in a markdown link to the platform page's std anchor.
    # The link covers just the std prefix (e.g. "C++17"), not the counts.
    assert "[C++17](https://example.com/repo/esp32/index.html#c++17): 2✅" in table
    assert "[C++20](https://example.com/repo/esp32/index.html#c++20): 1❌" in table


def test_usable_column_omits_links_when_no_site_url(tiers_yaml):
    """Without site_url, the std prefix is plain text — no markdown link."""
    results = [
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/optional", "macro": "__cpp_lib_optional", "status": "supported"},
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/variant", "macro": "__cpp_lib_variant", "status": "supported"},
    ]
    table = generate_summary_table(results, tiers_path=tiers_yaml)
    # No markdown link syntax in the Usable C++ cell
    assert "[C++17:" not in table
