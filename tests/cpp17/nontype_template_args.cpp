// feature: nontype_template_args
// macro: __cpp_nontype_template_args
// standard: cpp17
// category: language
// description: Allow constant evaluation for all non-type template arguments

struct S { int v; constexpr S(int x) : v(x) {} };
template<S s> constexpr int get() { return s.v; }
auto main() -> int { return get<S{42}>() - 42; }
