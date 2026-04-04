// feature: placeholder_variables
// macro: __cpp_placeholder_variables
// standard: cpp26
// category: language
// description: Placeholder variables (unnamed _)

auto main() -> int { auto [_, y] = (struct { int a; int b; }){1, 42}; return y - 42; }
