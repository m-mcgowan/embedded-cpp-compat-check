from compat_check.site.readme import generate_summary_table


def test_generate_summary_table_full_support():
    results = [
        {"platform": "esp32", "standard": "c++17", "feature": "cpp17/optional", "status": "supported"},
        {"platform": "esp32", "standard": "c++17", "feature": "cpp17/variant", "status": "supported"},
    ]
    table = generate_summary_table(results)
    assert "esp32" in table
    assert "**100%**" in table


def test_generate_summary_table_partial_support():
    results = [
        {"platform": "avr", "standard": "c++17", "feature": "cpp17/optional", "status": "supported"},
        {"platform": "avr", "standard": "c++17", "feature": "cpp17/variant", "status": "unsupported"},
    ]
    table = generate_summary_table(results)
    assert "**50%**" in table


def test_generate_summary_table_no_support():
    results = [
        {"platform": "avr", "standard": "c++20", "feature": "cpp20/concepts", "status": "unsupported"},
    ]
    table = generate_summary_table(results)
    assert "**0%**" in table
