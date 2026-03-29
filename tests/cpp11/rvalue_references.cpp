// feature: rvalue_references
// macro: __cpp_rvalue_references
// standard: cpp11
// category: language
// description: Rvalue references and move semantics

struct Moveable {
    int value;
    Moveable(int v) : value(v) {}
    Moveable(Moveable&& other) : value(other.value) { other.value = 0; }
};

auto main() -> int {
    Moveable a(42);
    Moveable b(static_cast<Moveable&&>(a));
    return b.value - 42;
}
