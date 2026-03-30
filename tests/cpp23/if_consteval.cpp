// feature: if_consteval
// macro: __cpp_if_consteval
// standard: cpp23
// category: language
// description: if consteval

constexpr int f() { if consteval { return 1; } else { return 0; } }
auto main() -> int { constexpr int v = f(); return v == 1 ? 0 : 1; }
