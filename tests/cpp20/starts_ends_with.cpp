// feature: starts_ends_with
// macro: __cpp_lib_starts_ends_with
// standard: cpp20
// category: library
// description: string starts_with/ends_with
#include <string>
auto main() -> int {
    std::string s = "hello world";
    return s.starts_with("hello") && s.ends_with("world") ? 0 : 1;
}
