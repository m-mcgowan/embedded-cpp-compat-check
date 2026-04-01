// feature: auto_cast
// macro: __cpp_auto_cast
// standard: cpp23
// category: language
// description: auto(x) decay copy syntax

auto main() -> int { int x = 42; auto y = auto(x); return y - 42; }
