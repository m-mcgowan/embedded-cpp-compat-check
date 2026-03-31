// feature: uncaught_exceptions
// macro: __cpp_lib_uncaught_exceptions
// standard: cpp17
// category: library
// description: std::uncaught_exceptions (plural)

#include <exception>
auto main() -> int { return std::uncaught_exceptions() == 0 ? 0 : 1; }
