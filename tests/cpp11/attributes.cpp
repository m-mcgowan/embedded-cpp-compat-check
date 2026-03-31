// feature: attributes
// macro: __cpp_attributes
// standard: cpp11
// category: language
// description: Basic attribute syntax [[noreturn]] etc

[[noreturn]] void fatal() { throw 42; }
auto main() -> int { return 0; }
