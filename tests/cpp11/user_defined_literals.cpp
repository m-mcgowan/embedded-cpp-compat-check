// feature: user_defined_literals
// macro: __cpp_user_defined_literals
// standard: cpp11
// category: language
// description: User-defined literals

constexpr long long operator""_km(unsigned long long v) { return v * 1000; }
auto main() -> int { return 5_km == 5000 ? 0 : 1; }
