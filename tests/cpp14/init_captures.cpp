// feature: init_captures
// macro: __cpp_init_captures
// standard: cpp14
// category: language
// description: Lambda init-capture (generalized lambda capture)

auto main() -> int {
    int x = 42;
    auto f = [val = x]() { return val; };
    return f() - 42;
}
