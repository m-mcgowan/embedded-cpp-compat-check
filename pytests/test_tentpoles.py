from pathlib import Path
import textwrap
from compat_check.tentpoles import (
    Level, Tentpole, TentpoleStatus, load_tentpoles, evaluate, roll_up, headline_std
)


def _write_yaml(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "tiers.yaml"
    p.write_text(textwrap.dedent(content))
    return p


def test_load_tentpoles_minimal(tmp_path):
    path = _write_yaml(tmp_path, """
        cpp17:
          tentpoles:
            - id: optional
              name: std::optional
              required: [__cpp_lib_optional]
        """)
    result = load_tentpoles(path)
    assert "c++17" in result
    tps = result["c++17"]
    assert len(tps) == 1
    assert tps[0] == Tentpole(
        id="optional",
        name="std::optional",
        required=("__cpp_lib_optional",),
        optional=(),
    )


def test_load_tentpoles_with_optional(tmp_path):
    path = _write_yaml(tmp_path, """
        cpp20:
          tentpoles:
            - id: ranges
              name: Ranges
              required: [__cpp_lib_ranges, __cpp_concepts]
              optional: [__cpp_lib_ranges_zip, __cpp_lib_ranges_chunk]
        """)
    result = load_tentpoles(path)
    tps = result["c++20"]
    assert tps[0].required == ("__cpp_lib_ranges", "__cpp_concepts")
    assert tps[0].optional == ("__cpp_lib_ranges_zip", "__cpp_lib_ranges_chunk")


def test_load_tentpoles_normalizes_std_keys(tmp_path):
    """Keys like 'cpp17' become 'c++17' to match the results format."""
    path = _write_yaml(tmp_path, """
        cpp17:
          tentpoles: []
        cpp20:
          tentpoles: []
        cpp26:
          tentpoles: []
        """)
    result = load_tentpoles(path)
    assert set(result.keys()) == {"c++17", "c++20", "c++26"}


def test_load_tentpoles_missing_optional_key(tmp_path):
    """A tentpole with no 'optional' key gets an empty tuple."""
    path = _write_yaml(tmp_path, """
        cpp17:
          tentpoles:
            - id: foo
              name: Foo
              required: [__cpp_foo]
        """)
    tps = load_tentpoles(path)["c++17"]
    assert tps[0].optional == ()


# Helper to build a results dict for a given macro→status mapping
def _results(macro_status: dict[str, str]) -> list[dict]:
    return [
        {"macro": m, "status": s, "feature": f"x/{m}"}
        for m, s in macro_status.items()
    ]


def test_evaluate_complete_no_optional():
    """All required pass, no optional defined → complete."""
    tp = Tentpole(id="x", name="X", required=("__cpp_a",), optional=())
    statuses = evaluate(_results({"__cpp_a": "supported"}), [tp])
    assert statuses[0].level == "complete"
    assert statuses[0].required_pass == 1
    assert statuses[0].failed_required == ()


def test_evaluate_complete_all_optional():
    """All required + all optional pass → complete."""
    tp = Tentpole(
        id="x", name="X",
        required=("__cpp_a",),
        optional=("__cpp_b", "__cpp_c"),
    )
    statuses = evaluate(
        _results({"__cpp_a": "supported", "__cpp_b": "supported", "__cpp_c": "unreported"}),
        [tp],
    )
    assert statuses[0].level == "complete"
    assert statuses[0].optional_pass == 2


def test_evaluate_good_75_percent_optional():
    """All required + exactly 75% of optional → good."""
    tp = Tentpole(
        id="x", name="X",
        required=("__cpp_a",),
        optional=("__cpp_b", "__cpp_c", "__cpp_d", "__cpp_e"),
    )
    statuses = evaluate(
        _results({
            "__cpp_a": "supported",
            "__cpp_b": "supported",
            "__cpp_c": "supported",
            "__cpp_d": "supported",
            "__cpp_e": "unsupported",
        }),
        [tp],
    )
    assert statuses[0].level == "good"
    assert statuses[0].optional_pass == 3


def test_evaluate_partial_below_75():
    """All required, 50% of optional → partial."""
    tp = Tentpole(
        id="x", name="X",
        required=("__cpp_a",),
        optional=("__cpp_b", "__cpp_c"),
    )
    statuses = evaluate(
        _results({"__cpp_a": "supported", "__cpp_b": "supported", "__cpp_c": "unsupported"}),
        [tp],
    )
    assert statuses[0].level == "partial"


def test_evaluate_partial_zero_optional_with_optional_defined():
    """All required, 0/N optional → partial (not unsupported)."""
    tp = Tentpole(
        id="x", name="X",
        required=("__cpp_a",),
        optional=("__cpp_b", "__cpp_c"),
    )
    statuses = evaluate(
        _results({"__cpp_a": "supported", "__cpp_b": "unsupported", "__cpp_c": "unsupported"}),
        [tp],
    )
    assert statuses[0].level == "partial"


def test_evaluate_unsupported_required_fails():
    """Any required macro fails → unsupported."""
    tp = Tentpole(
        id="x", name="X",
        required=("__cpp_a", "__cpp_b"),
        optional=(),
    )
    statuses = evaluate(
        _results({"__cpp_a": "supported", "__cpp_b": "unsupported"}),
        [tp],
    )
    assert statuses[0].level == "unsupported"
    assert statuses[0].failed_required == ("__cpp_b",)


def test_evaluate_macro_missing_from_results_counts_as_fail():
    """A required macro that isn't in results at all is treated as failing."""
    tp = Tentpole(id="x", name="X", required=("__cpp_missing",), optional=())
    statuses = evaluate(_results({}), [tp])
    assert statuses[0].level == "unsupported"
    assert statuses[0].failed_required == ("__cpp_missing",)


def test_evaluate_unreported_counts_as_pass():
    """Status 'unreported' (compiles but no macro) counts as a pass — same as raw %."""
    tp = Tentpole(id="x", name="X", required=("__cpp_a",), optional=())
    statuses = evaluate(_results({"__cpp_a": "unreported"}), [tp])
    assert statuses[0].level == "complete"


def test_evaluate_macro_lies_counts_as_fail():
    """Status 'macro_lies' (macro defined, compile fails) counts as a fail."""
    tp = Tentpole(id="x", name="X", required=("__cpp_a",), optional=())
    statuses = evaluate(_results({"__cpp_a": "macro_lies"}), [tp])
    assert statuses[0].level == "unsupported"


def _status(level: Level, id: str = "x") -> TentpoleStatus:
    """Build a TentpoleStatus with all-zero counts — only level matters here."""
    return TentpoleStatus(
        id=id, name=id.title(), level=level,
        required_pass=0, required_total=0,
        optional_pass=0, optional_total=0,
        failed_required=(),
    )


def test_roll_up_counts_by_level():
    statuses = [
        _status("complete"), _status("complete"), _status("good"),
        _status("partial"), _status("unsupported"), _status("unsupported"),
    ]
    counts = roll_up(statuses)
    assert counts == {"complete": 2, "good": 1, "partial": 1, "unsupported": 2}


def test_roll_up_empty():
    assert roll_up([]) == {"complete": 0, "good": 0, "partial": 0, "unsupported": 0}


def test_headline_std_picks_most_complete():
    rollups = {
        "c++17": {"complete": 8, "good": 0, "partial": 0, "unsupported": 0},
        "c++20": {"complete": 3, "good": 1, "partial": 1, "unsupported": 3},
    }
    assert headline_std(rollups) == "c++17"


def test_headline_std_breaks_tie_by_higher_std():
    """When complete counts tie, prefer the higher standard."""
    rollups = {
        "c++17": {"complete": 8, "good": 0, "partial": 0, "unsupported": 0},
        "c++20": {"complete": 8, "good": 0, "partial": 0, "unsupported": 0},
    }
    assert headline_std(rollups) == "c++20"


def test_headline_std_empty():
    assert headline_std({}) is None


def test_headline_std_all_unsupported():
    """Even if nothing is complete, return the highest std with tentpoles defined."""
    rollups = {
        "c++20": {"complete": 0, "good": 0, "partial": 0, "unsupported": 8},
        "c++23": {"complete": 0, "good": 0, "partial": 0, "unsupported": 6},
    }
    assert headline_std(rollups) == "c++23"
