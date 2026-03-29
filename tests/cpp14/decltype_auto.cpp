// feature: decltype_auto
// macro: __cpp_decltype_auto
// standard: cpp14
// category: language
// description: Return type deduction for normal functions

decltype(auto) identity(int x) { return x; }

auto main() -> int {
    return identity(0);
}
