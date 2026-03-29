// feature: constexpr
// macro: __cpp_constexpr
// standard: cpp11
// category: language
// description: constexpr specifier

constexpr int square(int x) { return x * x; }
static_assert(square(5) == 25, "constexpr failed");

auto main() -> int {
    constexpr int val = square(6);
    return val - 36;
}
