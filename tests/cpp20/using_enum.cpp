// feature: using_enum
// macro: __cpp_using_enum
// standard: cpp20
// category: language
// description: using enum declaration

enum class Color { Red, Green, Blue };
auto main() -> int { using enum Color; return static_cast<int>(Green) == 1 ? 0 : 1; }
