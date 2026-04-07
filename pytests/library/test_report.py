from compat_check.library.report import generate_markdown_report, generate_json_report

RESULTS = [
    {"platform": "avr-uno", "standard": "c++11", "example": "basic", "pass": False, "error": "error: optional not found"},
    {"platform": "avr-uno", "standard": "c++14", "example": "basic", "pass": False, "error": "error: optional not found"},
    {"platform": "avr-uno", "standard": "c++17", "example": "basic", "pass": True, "error": None},
    {"platform": "esp32", "standard": "c++11", "example": "basic", "pass": True, "error": None},
    {"platform": "esp32", "standard": "c++17", "example": "basic", "pass": True, "error": None},
]
LIBRARY = {"name": "test-lib", "version": "1.0.0"}

def test_markdown_report_has_summary():
    md = generate_markdown_report(LIBRARY, RESULTS)
    assert "## Summary" in md
    assert "test-lib" in md
    assert "avr-uno" in md
    assert "esp32" in md

def test_markdown_report_summary_min_standard():
    md = generate_markdown_report(LIBRARY, RESULTS)
    assert "c++17" in md
    assert "c++11" in md

def test_markdown_report_has_detail_table():
    md = generate_markdown_report(LIBRARY, RESULTS)
    assert "## Detail" in md
    assert "PASS" in md
    assert "FAIL" in md

def test_markdown_report_has_failures():
    md = generate_markdown_report(LIBRARY, RESULTS)
    assert "## Failure Details" in md
    assert "optional not found" in md

def test_json_report_structure():
    data = generate_json_report(LIBRARY, RESULTS)
    assert data["library"]["name"] == "test-lib"
    assert "results" in data
    assert "summary" in data
    assert data["summary"]["esp32"]["min_standard"] == "c++11"
    assert data["summary"]["avr-uno"]["min_standard"] == "c++17"
