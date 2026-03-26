from compat_check.probe.extractor import parse_probe_output


def test_parse_probe_output_from_strings_section():
    raw = (
        "__cpp_structured_bindings=201606\n"
        "__cpp_concepts=0\n"
        "__cpp_lib_optional=202110\n"
        "__SENTINEL__=-1\n"
    )
    result = parse_probe_output(raw)
    assert result["__cpp_structured_bindings"] == 201606
    assert result["__cpp_concepts"] == 0
    assert result["__cpp_lib_optional"] == 202110
    assert "__SENTINEL__" not in result


def test_parse_probe_output_empty():
    result = parse_probe_output("")
    assert result == {}
