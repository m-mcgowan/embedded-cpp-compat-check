// feature: exceptions
// macro: __cpp_exceptions
// standard: cpp11
// category: language
// description: Exception handling

auto main() -> int { try { throw 42; } catch (int e) { return e - 42; } return 1; }
