// feature: stacktrace
// macro: __cpp_lib_stacktrace
// standard: cpp23
// category: library
// description: std::stacktrace
#include <stacktrace>
auto main() -> int {
    auto st = std::stacktrace::current();
    return 0;
}
