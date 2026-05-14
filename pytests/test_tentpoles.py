from pathlib import Path
import textwrap
from compat_check.tentpoles import (
    Tentpole, TentpoleStatus, load_tentpoles, evaluate, roll_up, headline_std
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
