from compat_check.site.readme import generate_summary_table


def test_generate_summary_table_full_support():
    results = [
        {"platform": "esp32", "standard": "c++17", "feature": "cpp17/optional", "status": "supported"},
        {"platform": "esp32", "standard": "c++17", "feature": "cpp17/variant", "status": "supported"},
    ]
    table = generate_summary_table(results)
    assert "esp32" in table
    assert "**C++17 / 100%**" in table


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
