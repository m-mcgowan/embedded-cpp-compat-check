from compat_check.pio_plugin.cpp_standard import find_std_flag, replace_std_flag


def test_find_std_flag_gnu11():
    flags = ["-Wall", "-std=gnu++11", "-O2"]
    assert find_std_flag(flags) == "-std=gnu++11"


def test_find_std_flag_none():
    flags = ["-Wall", "-O2"]
    assert find_std_flag(flags) is None


def test_replace_std_flag():
    flags = ["-Wall", "-std=gnu++11", "-O2"]
    result = replace_std_flag(flags, "c++17")
    assert "-std=gnu++17" in result
    assert "-std=gnu++11" not in result


def test_replace_std_flag_no_existing():
    flags = ["-Wall", "-O2"]
    result = replace_std_flag(flags, "c++17")
    assert "-std=gnu++17" in result
