// feature: constinit
// macro: __cpp_constinit
// standard: cpp20
// category: language
// description: constinit specifier

constinit int global_val = 42;

auto main() -> int {
    return global_val - 42;
}
