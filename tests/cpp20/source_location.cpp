// feature: source_location
// macro: __cpp_lib_source_location
// standard: cpp20
// category: library
// description: std::source_location
#include <source_location>
auto main() -> int {
    auto loc = std::source_location::current();
    return loc.line() > 0 ? 0 : 1;
}
