// feature: consteval
// macro: __cpp_consteval
// standard: cpp20
// category: language
// description: Immediate functions (consteval)

consteval int square(int x) { return x * x; }

auto main() -> int {
    constexpr int val = square(5);
    return val - 25;
}
